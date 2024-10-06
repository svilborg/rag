SHELL := /bin/bash

.PHONY: build
build:
	docker-compose up --build

.PHONY: bash
bash:
	docker exec -it rag-app bash

.PHONY: import
import:
	docker exec -it rag-app python3 import.py

.PHONY: ask
ask:
	docker exec -it rag-app python3 ask.py "$(q)"

.PHONY: summarize
summarize:
	docker exec -it rag-app python3 summarize.py "$(q)"
