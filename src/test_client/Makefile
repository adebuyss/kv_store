
ifeq ($(PORT),)
PORT := 8081
endif

ifeq ($(STORE_PORT),)
STORE_PORT := 8080
endif

ifeq ($(STORE_CONTAINER),)
STORE_CONTAINER := kv_store
endif

ifeq ($(CONTAINER),)
CONTAINER := test_kv_store
endif

.PHONY: install run docker-clean docker-run docker-build docker-remove docker-stop logs

run:
	python3 app.py

docker-run:
	docker run -dp ${PORT}:8081 -e STORE_CONTAINER=${STORE_CONTAINER} -e STORE_PORT=${STORE_PORT} --net ${STORE_CONTAINER}_net --name ${CONTAINER} --hostname ${CONTAINER} ${CONTAINER}

docker-stop:
	docker stop $(CONTAINER)

logs:
	docker logs $(CONTAINER)

install:
	pip install -r requirements.txt

docker-clean:
	-docker stop `docker ps -a | grep "\ $(CONTAINER)$$" | awk '{print $$1}'`
	-docker rm `docker ps -a | grep "\ $(CONTAINER)$$" | awk '{print $$1}'`
	-docker rmi `docker images | grep "^$(CONTAINER)" | awk '{print $$3}'` --force

docker-remove:
	-docker stop `docker ps -a | grep "\ $(CONTAINER)$$" | awk '{print $$1}'`
	-docker rm `docker ps -a | grep "\ $(CONTAINER)$$" | awk '{print $$1}'`


docker-build:
	docker build . -t ${CONTAINER} --no-cache
