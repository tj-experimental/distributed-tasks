
redis-install:
	@brew info redis || brew install redis
	@ln -sfv /usr/local/opt/redis/*.plist ~/Library/LaunchAgents

install:
	@pip install -e .'[development]'
	@pip-sync

start-celery:
	@pip freeze | grep -i 'celery' || @$(MAKE) install
	@celery -A celery_task worker --loglevel=info

start-celery-beat:
	@celery -A celery_task beat --loglevel=info
