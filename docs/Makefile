# Minimal makefile for Sphinx documentation

SPHINXOPTS  ?=
SPHINXBUILD ?= python3 -m sphinx
SPHINXPROJ   = ncio
SOURCEDIR    = source
BUILDDIR     = build

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# https://www.docslikecode.com/articles/github-pages-python-sphinx/
# https://github.com/annegentle/create-demo
github:
	@make html
	@rsync -arv --delete ./build/html/ ./html/

# Catch-all target: route all unknown targets to Sphinx using the
# "make mode" option. $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
