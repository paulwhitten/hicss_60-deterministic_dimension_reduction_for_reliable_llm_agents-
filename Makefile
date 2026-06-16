MAIN = hicss_submission

.PHONY: all clean

all: $(MAIN).pdf

# TEXINPUTS includes template/ so LaTeX finds hicss.sty
$(MAIN).pdf: $(MAIN).tex references.bib hicss-packages.tex
	TEXINPUTS=.:template//: pdflatex $(MAIN)
	TEXINPUTS=.:template//: biber $(MAIN)
	TEXINPUTS=.:template//: pdflatex $(MAIN)
	TEXINPUTS=.:template//: pdflatex $(MAIN)

clean:
	rm -f $(MAIN).aux $(MAIN).bbl $(MAIN).bcf $(MAIN).blg \
	      $(MAIN).log $(MAIN).out $(MAIN).run.xml $(MAIN).pdf
