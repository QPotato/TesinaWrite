#
#   Makefile
#
# Los bucles while son porque biber quiere que corras pdflatex -> biber -> pdflatex
# para agarrar bien las referencias.
#
# Por el mismo motivo necesitamos hacer clean antes de buildear.

MAINTEX = Tesis
SLIDES = Slides/defensa
CARTA = carta
CP = cp
GHC = ghc
RM = rm -f
LATEX = latex
PDFLATEX = pdflatex
LHS = lhs2TeX
BIB = biber
LHSPAR = --poly
LHSFILES = $(MAINTEX)
EXT = *.nav *.snm *.ptb *.blg *.log *.aux *.lof *.lot *.bit *.idx *.glo *.bbl *.ilg *.toc *.out *.ind *~ *.ml* *.mt* *.th* *.bmt *.xyc *.bcf *.run.xml *.dot *.ptc
PAG =
NUM =

default: pdflatex

carta:
	$(PDFLATEX) $(CARTA).tex -halt-on-error

slides: clean
	$(PDFLATEX) $(SLIDES).tex -halt-on-error
	@latex_count=100 ; \
	while egrep -s 'Rerun (LaTeX|to get)' $(SLIDES).log && [ $$latex_count -gt 0 ] ;\
	    do \
	      echo "Rerunning latex...." ;\
	      $(PDFLATEX) $(SLIDES).tex -halt-on-error ;\
		  sleep 0.5;\
	      latex_count=`expr $$latex_count - 1` ;\
	    done

all: dvi ps pdf slides carta

dvi: clean
	$(LATEX) $(MAINTEX).tex
	$(BIB) $(MAINTEX)
	@latex_count=5 ; \
	while egrep -s 'rerun (LaTeX|to get cross-references right)' $(MAINTEX).log && [ $$latex_count -gt 0 ] ;\
	    do \
	      echo "Rerunning latex...." ;\
	      $(LATEX) $(MAINTEX).tex ;\
	      latex_count=`expr $$latex_count - 1` ;\
	    done

ps: dvi
	dvips -f $(MAINTEX).dvi > $(MAINTEX).ps

pdflatex: clean
	$(PDFLATEX) $(MAINTEX).tex -halt-on-error
	$(BIB) $(MAINTEX)
	@latex_count=100 ; \
	while egrep -s 'rerun (LaTeX|to get cross-references right)' $(MAINTEX).log && [ $$latex_count -gt 0 ] ;\
	    do \
	      echo "Rerunning latex...." ;\
	      $(PDFLATEX) $(MAINTEX).tex -halt-on-error ;\
		  sleep 0.5;\
	      latex_count=`expr $$latex_count - 1` ;\
	    done

clean:
	$(RM) $(EXT)


clean-all: clean
	$(RM) *.dvi
	$(RM) *.ps
	$(RM) *.pdf

tar: clean
	alias NOMBRE="basename `pwd`";\
	tar -cvjf `NOMBRE`.tar.bz2\
	        --exclude "*.bz2"\
	        --exclude "*.dvi"\
		--exclude "*.tar.bz2"\
	        ../`NOMBRE`/ ;\
	unalias NOMBRE

help:
	@echo "    make dvi"
	@echo "    make all           -- dvi ps pdf slides carta"
	@echo "    make ps"
	@echo "    make pdflatex      -- default"
	@echo "    make clean"
	@echo "    make clean-all"
	@echo "    make tar"
	@echo "    make slides"

