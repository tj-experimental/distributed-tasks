from redis import StrictRedis

# create a connection to the localhost Redis server instance, by
# default it runs on port 6379
StrictRedis(host='localhost', port=6379, db=0)
