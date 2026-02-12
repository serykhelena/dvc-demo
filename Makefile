# ===================================================================
# Development. Start Work
# ===================================================================

#* Installation
.PHONY: project-init
project-init: install-packages dvc-local-init dvc-remote-init

.PHONY: install-packages
install-packages:
	uv sync

.PHONY: dvc-local-init
dvc-local-init:
	@if [ ! -d ".dvc" ]; then \
		echo "Initializing DVC..."; \
		uv run dvc init; \
		uv run dvc install; \
	else \
		echo "DVC already initialized"; \
	fi

.PHONY: dvc-remote-init
dvc-remote-init:
	uv run python scripts/init_dvc.py

#* Cleaning
.PHONY: pycache-remove
pycache-remove:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf
	find . | grep -E "(.ipynb_checkpoints$$)" | xargs rm -rf

.PHONY: build-remove
build-remove:
	rm -rf build/

.PHONY: clean-all
clean-all: pycache-remove build-remove
