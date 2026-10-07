PYTHON ?= python

.PHONY: update report
update:
	$(PYTHON) scripts/11_run_pipeline.py
