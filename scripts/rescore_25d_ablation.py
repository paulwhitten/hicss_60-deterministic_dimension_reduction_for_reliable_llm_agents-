#!/usr/bin/env python3
"""
Rescore of the 2.5-D ablation: replace the model's generated height with the
deterministic occupancy value and re-score, decomposing the 28.7 pp ablation gap
into a verification component (fixing heights) and a removal component (the
schema's effect on the horizontal plan).

Data, relative to the repository root:
  Schema B, model generates full 3D:   dist/logs/ablation/no-2.5d-decomp/run{1..7}
  Schema A, full 2.5-D system baseline: dist/logs/20260401_* (gpt-4o-mini, n=12)

Method. For each round in the 3D ablation, reconstruct the model's built
structure from conversation.log (the [BUILD] submission, or the executor
placements plus the [START_STRUCTURE] blocks when the build failed closed), then
re-stack each column by occupancy (order by the model's height, reassign heights
50, 150, 250, ...) and compare to the target. R_B is the resulting accuracy.

Validation gates:
  A. verbatim accuracy from the reconstruction reproduces the known 65.893%.
  B. reconstructed model matches the console.log "got" ground truth on rounds
     where it is present.
  C. start-structure plus executor placements matches the [BUILD] submission.

Run:  python3 hiccs/scripts/rescore_25d_ablation.py
"""
import re
import os
import glob
import statistics
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ABL = os.path.join(ROOT, "dist", "logs", "ablation", "no-2.5d-decomp")
BASE = os.path.join(ROOT, "dist", "logs")

PLACED = re.compile(r"placed (\w+) at \((-?\d+),(-?\d+),(-?\d+)\) \[(\w+)\]")
BUILD = re.compile(r"green_agent:rita: \[BUILD\](;(.*))?$")


def parse_struct(s):
    out = set()
    for tok in (s or "").strip().split(";"):
        p = tok.strip().split(",")
        if len(p) == 4:
            try:
                out.add((p[0].strip(), int(p[1]), int(p[2]), int(p[3])))
            except ValueError:
                pass
    return out


def restack(blocks):
    # per column, order by (model height, placement index), reassign 50,150,250,...
    cols = defaultdict(list)
    for i, (c, x, y, z) in enumerate(blocks):
        cols[(x, z)].append((y, i, c))
    out = set()
    for (x, z), lst in cols.items():
        lst.sort(key=lambda t: (t[0], t[1]))
        for k, (y, i, c) in enumerate(lst):
            out.add((c, x, 50 + 100 * k, z))
    return frozenset(out)


def full_system_accuracy():
    # Schema A baseline. Each round is double-logged, so total lines equal 320.
    accs = []
    for d in sorted(glob.glob(os.path.join(BASE, "20260401_*"))):
        cl = os.path.join(d, "console.log")
        if not os.path.isfile(cl):
            continue
        t = open(cl, encoding="utf-8", errors="replace").read()
        c = len(re.findall(r"Correct structure built", t))
        ic = len(re.findall(r"Incorrect structure", t))
        if c + ic == 320:
            accs.append(c // 2 / 160 * 100)
    return statistics.mean(accs), statistics.stdev(accs), len(accs)


def conv_segments(run):
    segs, cur = [], []
    for line in open(os.path.join(run, "conversation.log"), encoding="utf-8", errors="replace"):
        cur.append(line.rstrip("\n"))
        if "User input: Feedback:" in line:
            segs.append(cur)
            cur = []
    return segs


def console_feedback(run):
    return [l for l in open(os.path.join(run, "console.log"), encoding="utf-8", errors="replace")
            if "User input: Feedback:" in l]


def reconstruct(seg):
    start = set()
    for l in seg:
        if "[START_STRUCTURE]" in l:
            start = parse_struct(l.split("[START_STRUCTURE]", 1)[1])
            break
    bs = None
    for l in seg:
        m = BUILD.search(l)
        if m:
            bs = m.group(2)
    last = -1
    for i, l in enumerate(seg):
        if "Final steps after all fixes" in l:
            last = i
    pls = []
    for l in (seg[last + 1:] if last >= 0 else seg):
        m = PLACED.search(l)
        if m:
            pls.append((m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))))
    build = list(parse_struct(bs)) if bs else None
    model_place = list(start) + [(p[0], p[1], p[2], p[3]) for p in pls]
    return build, pls, model_place


def main():
    base_mean, base_sd, base_n = full_system_accuracy()
    verbs, rbs = [], []
    gB_ok = gB_tot = gC_ok = gC_tot = 0
    for run in sorted(glob.glob(os.path.join(ABL, "run*"))):
        segs = conv_segments(run)
        cfb = console_feedback(run)
        assert len(segs) == 160, (run, len(segs))
        correct = fixed = 0
        for idx, seg in enumerate(segs):
            fb = [l for l in seg if "User input: Feedback:" in l][-1]
            build, pls, model_place = reconstruct(seg)
            if build is not None and pls:
                gC_tot += 1
                gC_ok += (frozenset(model_place) == frozenset(build))
            c = cfb[idx] if idx < len(cfb) else ""
            if "Expected:" in c and ", but got:" in c:
                got = parse_struct(c.split("Expected:", 1)[1].split(", but got:", 1)[1].split("| Round")[0])
                if got:
                    gB_tot += 1
                    m = frozenset(build) if build is not None else frozenset(model_place)
                    gB_ok += (m == frozenset(got))
            if "Correct structure built" in fb:
                correct += 1
                continue
            if "Expected:" not in fb:
                continue
            tgt = frozenset(parse_struct(fb.split("Expected:", 1)[1].split(", but got:", 1)[0]))
            if not tgt:
                continue
            model = build if build is not None else model_place
            if restack(model) == tgt:
                fixed += 1
        verbs.append(correct / 160 * 100)
        rbs.append((correct + fixed) / 160 * 100)
    mv, mr = statistics.mean(verbs), statistics.mean(rbs)
    print("Schema A full system (n=%d):   %.3f%%  sd %.3f" % (base_n, base_mean, base_sd))
    print("Schema B verbatim    (n=7):   %.3f%%  sd %.3f" % (mv, statistics.stdev(verbs)))
    print("Schema B R_B         (n=7):   %.3f%%  sd %.3f" % (mr, statistics.stdev(rbs)))
    print()
    print("Decomposition of the %.2f pp gap:" % (base_mean - mv))
    print("  verification (height fix) = %.2f pp" % (mr - mv))
    print("  removal      (schema)     = %.2f pp" % (base_mean - mr))
    print()
    print("Gate A verbatim == 65.893: %s (%.3f)" % ("PASS" if abs(mv - 65.893) < 0.01 else "FAIL", mv))
    print("Gate B model == console got: %d/%d" % (gB_ok, gB_tot))
    print("Gate C start+placements == BUILD: %d/%d" % (gC_ok, gC_tot))


if __name__ == "__main__":
    main()
