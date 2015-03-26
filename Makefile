# Some automation to submit to a journal (e.g. Elsevier).
# It detects the main latex file and eps files used.
# Author: @balkian
# TODO: Only import the tex files used in the main file, and their images.

LATEX=$(basename $(shell grep -l '\\begin{document' *.tex))
LETTER=letter
COVER=cover
HIGHLIGHTS=highlights

HTML_OUT=$(LETTER).html
AUX_DIR=.aux

.PHONY: all cover clean highlights latex letter zip

default: latex

all: $(LATEX).pdf $(LETTER).pdf $(COVER).pdf $(HIGHLIGHTS).pdf | zip

$(AUX_DIR):
	@mkdir -p $(AUX_DIR)

$(LETTER).pdf: $(LETTER).md | $(AUX_DIR)
	@pandoc -s -H style.html $(LETTER).md -o $(HTML_OUT)
	@wkhtmltopdf $(HTML_OUT) $(LETTER).pdf
	@echo Letter generated: $(LETTER)

$(LATEX).pdf: *.tex | $(AUX_DIR)
# An alternative to doing three passes is using latexmk
	@pdflatex -interaction=batchmode -output-directory=$(AUX_DIR) $(LATEX) >/dev/null
# openout_any=a -> write to a folder (AUX_DIR)
# TEXMFOUTPUT -> find the aux files in that folder
	@openout_any=a TEXMFOUTPUT="$(AUX_DIR)/" bibtex $(AUX_DIR)/$(LATEX) >/dev/null
	@pdflatex -interaction=batchmode -output-directory=$(AUX_DIR) $(LATEX) >/dev/null
	@pdflatex -interaction=batchmode -output-directory=$(AUX_DIR) $(LATEX)
	@mv $(AUX_DIR)/$(LATEX).pdf .
	@echo "Finished"

$(HIGHLIGHTS).pdf: $(HIGHLIGHTS).md
	pandoc $(HIGHLIGHTS).md -o (HIGHLIGHTS).pdf

$(COVER).pdf: $(COVER).md
	pandoc $(COVER).md -o $(COVER).pdf

$(PAPER).zip: $(LATEX).pdf $(LETTER).pdf
	@zip $(LATEX).zip *.tex  $(LETTER).pdf $(COVER).pdf $(HIGHLIGHTS).pdf $(LATEX).pdf
	@for r in `sed -n 's/.*bibliography{\(.*\)}.*/\1/p' *.tex`; do \
		zip $().zip  $$r.bib; \
	done
	@for i in `sed -n 's/.*includegraphics{\(.*\)}.*/\1/p' *.tex`; do \
		zip $(LATEX).zip  figures/$$i.eps; \
	done

clean:
	@-rm -rf $(AUX_DIR)
	@-rm -f $(HTML_OUT)

clean_all: clean
	@rm -f $(LATEX).zip
	@rm -f $(LATEX).pdf
	@rm -f $(REVIEW).pdf
	@rm -f $(COVER).pdf
	@rm -f $(HIGHLIGHTS).pdf

view: $(LATEX).pdf
	xdg-open $(LATEX).pdf

cover: $(COVER).pdf
highlights: $(HIGHLIGHTS).pdf
latex: $(LATEX).pdf
letter: $(LETTER).pdf
zip: $(PAPER).zip