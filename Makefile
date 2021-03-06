func_name = authenticator

build_psql:
	docker build -t pgsql_builder . 
	docker run -d -i -t pgsql_builder bash 
	$(eval CONTAINER := $(shell docker ps -lq))
	docker cp $(CONTAINER):/usr/src/psycopg2-2.7b2/build/lib.linux-x86_64-3.6/psycopg2 psycopg2
	docker rm -f $(CONTAINER)

build_zip:
	zip -r9 code.zip psycopg2; zip -g code.zip auth.py

update_code:
	aws lambda update-function-code --function-name $(func_name) --zip-file fileb://code.zip
