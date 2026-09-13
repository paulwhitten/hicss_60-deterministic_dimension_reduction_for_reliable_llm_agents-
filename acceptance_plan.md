# HICSS-60 acceptance plan

This is a staged, priority based plan for the final version of the accepted
HICSS-60 paper, submission ID 12509, Deterministic-Dimension Reduction for
Reliable LLM Agents. It is a plan only. It makes no manuscript changes. It maps
each reviewer suggestion to a location in hiccs_submission.tex, an effort level, a
priority, and whether it needs new data.

## Status and deadlines

- Accepted to HICSS-60 with no mandatory revisions. Reviewer suggestions are
  optional.
- Final manuscript due September 22. The submission system opens September 12,
  6pm Hawaii time, at hicss-submissions.org.
- At least one author must register by October 1.
- The minitrack chair for autonomous edge computing indicated this was the
  highest rated paper in the track. This is favorable context, it does not change
  the required edits.

## Reviewed submission baseline

The version the reviewers saw is the PDF at
draft_submission/paper_0dfa788d-7bda-4747-bbbf-39b6b254d762.pdf. In the hiccs
repo it corresponds to commit 00f9522, titled draft submission, dated 2026-06-16.
This was confirmed by matching the PDF text to that commit, the PDF carries the
distinctive wording introduced in that commit, deterministic-dimension reduction,
cross-model comparison, IGLU transfer, and A preprint of this work presents, and
it carries the old ablation numbers.

Important. The reviewed PDF reports the old, confounded ablation figures, 50.7
percentage points with a without-decomposition accuracy of 43.8 percent. The
reviewers did not see the corrected 28.7 percentage points and 65.9 percent.

Changes since the reviewed submission. There is exactly one commit after the
reviewed draft, 40c861e, and the working tree has no uncommitted edits to the
tracked manuscript files. That commit makes two changes.

- Wanted. The 2.5-D ablation correction, 50.7 to 28.7 and 43.8 to 65.9 percent in
  all four places. This is the integrity fix and should stay.
- To verify. A one line references.bib URL edit for the Nemotron model, from
  nvidia/Nemotron-3-Super-120B-A12B-NVFP4 to
  nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-NVFP4. Confirm the corrected URL
  resolves before submission. This ties to the reference audit flag on
  nemotron2024.

So the concern about unwanted post-review changes is limited. The only prose
change is the wanted ablation correction, and the only other change is a single
citation URL to verify.

## Scope constraint from the acceptance letter

The letter permits adding author information but says no other major changes. So
the plan treats claim moderation, limitation wording, and citations as in scope
minor edits, and treats new experiments or new sections as out of scope for this
camera ready. Items that need new runs are recorded as follow-on work for the
second and third papers rather than this manuscript.

## Stage 0 critical, P0, highest priority, ablation attribution correction

Status, completed. The manuscript shows 28.7 pp and 65.9 percent throughout,
verified against the final NAECON paper. This item is done.

This is the single highest priority item because it is a correctness fix to a
headline result, not an optional improvement. Correcting an error is permitted
even under the no major changes rule, since it is accurate reporting of an
existing ablation, not new work.

Background. In the NAECON work, the initial ablation of the 2.5-D decomposition
was confounded. The few-shot examples and other prompts still used two
dimensional coordinates even in the condition that was meant to remove the 2.5-D
decomposition. So the ablated condition was not a clean removal, and part of the
measured gain was an artifact of the prompt format rather than the 2.5-D
decomposition itself. The old figures were a 50.7 percentage point contribution
with a without-decomposition accuracy of 43.8 percent.

Correction. When the prompts and few-shot examples were changed to use full 3D
coordinates in the condition where the 2.5-D decomposition is removed, the
contribution attributed to the 2.5-D decomposition dropped to 28.7 percentage
points, with a without-decomposition accuracy of 65.9 percent.

Evidence it is already applied. The hiccs repo commit 40c861e, titled update for
fixed 2.5d ablation, ensuring samples and refinements are in 3D, replaced 50.7
with 28.7 and 43.8 percent with 65.9 percent in all four places, the Findings
text, the ablation table row, a commented summary line, and the Design
Implications text. A search of the current manuscript found no residual 50.7,
43.8, or 81.9 values, and the abstract states the effect qualitatively with no
number. Both current NAECON copies under dist/naecon2026 also report 28.7
percentage points and 65.9 percent.

Confirmation checklist before submission.
- Confirm the manuscript at head still shows 28.7 pp and 65.9 percent in the
  Findings text and the ablation table.
- Confirm no stale 50.7, 43.8, or 81.9 values remain anywhere, including any
  figure, caption, or design implication.
- Confirm the HICSS numbers match the final NAECON paper exactly, not only the
  current draft copies.

## Stage 0, P0, camera ready must fixes, required

These are required to de-anonymize and to meet the format rules. One was flagged
by a reviewer.

1. Author block. Completed. Paul Whitten, Sharath Chander Reddy Baddam, and
   Li-Jen Chen are listed with the Rockwell Automation affiliation and emails, and
   the paper compiles. City and ORCID are commented out per author request.
2. Restore the self-citation. Completed. The NAECON 2026 conference citation,
   entry 11674959 in references.bib, an IEEE published paper not a preprint, now
   replaces the Citation omitted for blind review placeholder, and the earlier
   preprint wording was updated to an earlier conference paper. Review 3 point 6
   is addressed.
3. De-anonymize repository references. Completed. The stale double-blind header
   comments were updated to the final camera-ready wording, and a body search
   found no anonymized reference, the repository citations route through the bib
   entries that already carry the public URLs.
4. Formatting and references pass. References, completed. The audit-confirmed
   fixes are applied and rebuilt, SayCan reordered to the published Ichter-first
   order, Hevner pages corrected to 75-105, the Dziri URL fixed, and the NAECON
   title acronyms brace-protected so 2.5-D and LLM render capitalized. Remaining,
   confirm no header, footer, or page numbers, letter size 8.5 by 11, and that the
   paper stays within the 10-page limit, per the Final Format Specifications.

## Stage 1, P1, cheap high value text edits, no new data

These address multiple reviewers, are text only, and stay within the no major
changes rule.

1. Moderate the generalization claim. Reviews 1 and 4. The passage The design
   principle is domain-general. Any physically or logically constrained domain at
   hicss_submission.tex line 742 runs ahead of the evidence, which is one primary
   domain plus one transfer benchmark. Reframe as a conjecture supported by BWIM
   and IGLU, and add one sentence on where the deterministic versus reasoning
   boundary blurs in more complex tasks, which is Review 4 point.
2. Condition the dominance claim on its assumption. Review 1. The contribution
   text says the executor strictly dominates for any positive error rate at
   hicss_submission.tex line 110, and the joint generation assumption is flagged
   but not tested at lines 246 and 416. Reword to dominates conditional on the
   stated assumptions, and make the conditional explicit where the claim first
   appears.
3. Make the model tuning confound more prominent. Reviews 1 and 2. The prompts and
   enrichment were tuned for GPT-4o-mini and GPT-4o ran untuned, so the comparison
   cannot separate architecture from prompt optimization. State this limitation
   more prominently in the limitations discussion. This mirrors the tuning
   confound discipline recorded for the coding determinism work.

## Stage 2, P2, moderate edits, no new experiments

These are more than a sentence but still need no new runs.

1. Generalize the cost comparison. Review 2. Keep the concrete example and add a
   unitless or normalized version so the cost result does not depend on one
   implementation.
2. Ground the taxonomy in literature. Review 2. Add citations for the three
   category taxonomy, geometric constraints, procedural knowledge constraints, and
   workflow state management constraints, near hicss_submission.tex line 746.
3. Release implementation details. Review 1. Prompts and the adaptive enrichment
   rules are not in the manuscript. Point to the public repo, or add a short
   supplementary appendix, so others can build on the work.
4. Add a domain extension paragraph. Review 4. Briefly discuss how the approach
   extends to other domains and where the deterministic versus reasoning line
   becomes unclear. This can share text with Stage 1 item 1.

## Stage 3, P3, stretch, needs new runs, likely defer

These would strengthen the paper but need new experiments and risk exceeding the
no major changes rule. Recommend deferring to the follow-on papers unless there is
time and chair approval.

1. Both models tuned comparison. Reviews 1 and 2. Run a GPT-4o pipeline tuned to a
   similar degree as the GPT-4o-mini pipeline, so the comparison separates
   architecture from prompt optimization. Needs new runs, unlikely to fit before
   September 22.
2. Empirical test of the dominance assumption. Review 1. Test whether generating
   deterministic and free dimensions jointly helps the free dimension predictions.
   Needs new runs. If not done, Stage 1 item 2 conditional framing is the fallback.

## Recommended cut line

For the September 22 camera ready, complete Stage 0 and Stage 1, and complete
Stage 2 as time allows. Treat Stage 3 as follow-on work for the second and third
papers, which already plan matched comparisons and additional models.

## Venue strategy note

The question of whether this belonged at a machine learning venue such as NeurIPS
or ICLR is recorded here as strategy, it does not affect the accepted HICSS paper.

- HICSS is a fit for a design science framing where the design principle is the
  contribution, which is how this paper is written, and it is now accepted and top
  of its track. That is a concrete result in hand.
- NeurIPS and ICLR main tracks apply a different and more adversarial empirical
  bar. The tuning confound and the single primary domain would likely draw sharper
  criticism, and those venues expect matched baselines, ablations, significance
  testing, more domains, and positioning against the agent, tool use, and
  neurosymbolic literature.
- A reasonable path is to keep HICSS for this paper, and aim the follow-on papers
  at a stronger venue only after adding the rigor those venues expect. NeurIPS or
  ICLR workshops on agentic or neurosymbolic or embodied AI, and venues such as
  COLM or a systems venue for the edge results, are lower risk targets for
  visibility.

## Assumptions

- The acceptance letter phrase no other major changes permits claim moderation,
  limitation wording, and citations, and discourages new experiments and new
  sections. Stage 3 is treated accordingly.
- The preprint to restore at line 95 is the NAECON 2026 paper under dist/naecon2026
  and the repository is github.com/ltl-uva/build_what_i_mean. Verify the exact
  citation before inserting it.
- Line numbers refer to the current hiccs/hicss_submission.tex and may shift as
  edits are applied.

## References

- Manuscript, hiccs/hicss_submission.tex.
- Reviewed submission PDF,
  draft_submission/paper_0dfa788d-7bda-4747-bbbf-39b6b254d762.pdf, corresponds to
  hiccs repo commit 00f9522, draft submission, 2026-06-16.
- Reference verification note, the bibtex audit,
  [hicss-bibtex-verification.md](../.copilot-tracking/research/subagents/2026-08-20/hicss-bibtex-verification.md).
  Compare the HICSS references and the corrected 2.5-D ablation numbers against
  the final NAECON paper before submission.
- Final NAECON paper, dist/naecon2026.
- Bibliography, hiccs/references.bib.
- Acceptance and reviews, hiccs/hicss_acceptance_and_review.txt.
- Coding determinism confound discipline,
  llm_coding_determinism/second-paper/confound-analysis.md.
