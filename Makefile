# Self-Documented Makefile see https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html

.DEFAULT_GOAL := help

LOCAL_DEV_HONCHO_PROCESS := celery flower

.PHONY: help
# Put it first so that "make" without argument is like "make help".
help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-32s-\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: redis-install
redis-install:
	@brew info redis || brew install redis
	@ln -sfv /usr/local/opt/redis/*.plist ~/Library/LaunchAgents

.PHONY: install
install:
	@pip install -e .'[development]' -r requirements.txt

.PHONY: start-celery
start-celery:
	@pip freeze | grep -i 'celery' || $(MAKE) install
	@celery -A celery_task worker --loglevel=info

.PHONY: start-celery-beat
start-celery-beat:
	@celery -A celery_task beat --loglevel=info

.PHONY: start-flower
start-flower:
	@celery flower -A celery_task flower


# --------------------------------------------------
# ------------ Honcho Commands ---------------------
# --------------------------------------------------
.PHONY: run-honcho
run-honcho:
	@honcho -f Procfile start $(LOCAL_DEV_HONCHO_PROCESS)
