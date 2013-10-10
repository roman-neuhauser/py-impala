# vim: ts=8

PYTHON=		python2
RST2HTML=	rst2html

check:
	$(PYTHON) tests/impalatest.py

clean:
	$(RM) README.html $(tests.html)

dist:
	$(PYTHON) setup.py sdist

tests.html = \
	tests/index.html \
	$(addsuffix .html,$(basename $(wildcard tests/*.t)))

html: README.html tests-html

tests-html: $(tests.html)

%.html: %.rst
	$(RST2HTML) $< $@

tests/%.html: tests/%.t
	$(RST2HTML) $< $@

.PHONY: check
.PHONY: clean
.PHONY: dist
.PHONY: html
.PHONY: tests-html
