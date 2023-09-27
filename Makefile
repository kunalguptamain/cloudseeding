
help: # show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#' Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

run-local: # runs flask locally
	flask run

run-public: # makes server publicly available
	flask run --host=0.0.0.0

# setup: # set up tools needed to run
# 	python3 -m venv .venv
# 	pip3 install Flask 

# Windows
# .venv\Scripts\activate

# Linux/Mac
# source .venv/bin/activate
