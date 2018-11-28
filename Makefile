
redis-install:
	@brew info redis || brew install redis
	@ln -sfv /usr/local/opt/redis/*.plist ~/Library/LaunchAgents

install:
	@pip install -e .'[development]'
	@pip-sync
