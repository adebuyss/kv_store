
ifeq ($(PORT),)
PORT := 8080
endif

ifeq ($(CONTAINER),)
CONTAINER := kv_store
endif

.PHONY: install run docker-clean docker-run docker-build docker-remove docker-stop docker-net docker-unnet

run:
	python3 app.py

docker-net:
	-docker network create ${CONTAINER}_net

docker-unnet: docker-clean
	-docker network rm ${CONTAINER}_net

docker-run: docker-net
	docker run -dp ${PORT}:8080 --net ${CONTAINER}_net  --name ${CONTAINER} --hostname ${CONTAINER} ${CONTAINER}

docker-stop:
	docker stop $(CONTAINER)

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
