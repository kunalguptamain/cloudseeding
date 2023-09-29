REQ_DIR = .

help: # show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#' Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

run-local: # runs flask locally
	flask run

run-public: # makes server publicly available
	flask run --host=0.0.0.0

dev-env: # creates a virtual environment and installs requirements for development
	pip install -r $(REQ_DIR)/requirements.txt

# Windows
# .venv\Scripts\activate

# Linux/Mac
# source .venv/bin/activate
