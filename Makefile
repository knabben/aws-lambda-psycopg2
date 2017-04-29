build_psql:
	docker build -t pgsql_builder . 
	docker run -d -i -t pgsql_builder bash 
	$(eval CONTAINER := $(shell docker ps -lq))
	docker cp $(CONTAINER):/usr/src/psycopg2-2.7b2/build/lib.linux-x86_64-3.6/psycopg2 build
	docker rm -f $(CONTAINER)

