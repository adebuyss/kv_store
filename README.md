
This project is a basic key/value store application witch keeps it's data in memory. It contains the program itself - kv_store, as well as test_client, which has endpoints that can be used to exercise basic tests on the kv_store.

This project requires that you have make and docker installed, and your shell user can run docker commands.


**Running the kv_store server:**

```
$ cd ./src/kv_store
$ make docker-build
$ make docker-run
```

At this point, the store should be running on localhost port 8080. You can start using it. Here are some example commands
to run to test:

```
$ curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8080/v1/ -d '{"key": "foo", "value": "bar"}'
$ curl -X GET http://127.0.0.1:8080/v1/foo
$ curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8080/v1/ -d '{"key": "foo", "value": "bar2"}'  <- this should fail, we only  allow overwrites with PUT
$ curl -X PUT -H "Content-Type: application/json" http://127.0.0.1:8080/v1/foo -d '{"value": "bar2"}'
```

**Running the test server:**

(starting from the project root)

THESE COMMANDS WILL NOT WORK WITHOUT A RUNNING kv_store SERVER

```
$ cd ./src/test_client
$ make docker-build
$ make docker-run
```

Once the test_client server is running (port 8081), you can run it's test endpoints:

```
$ curl -X GET http://127.0.0.1:8081/test_overwrite
$ curl -X GET http://127.0.0.1:8081/test_delete
```

This will give you a basic status of the tests run. For a better view of the api calls made, you can view container logs by running:

```
$ make logs
```

**Cleanup:**

To remove the project from docker, you can run the following commands. Order is important.

First, in test_client

```
$ make docker-clean
```

Next in kv_store

```
$ make docker-unnet   (This will execute docker-clean and also remove the bridge network the containers use for communication)
```

**Errata:**

There are various make targets that help with manipulating docker containers here is a below is a non-exaustive description of each:

```
install: Used within docker and will also install pip requirements locally. Requires a python3.8 virtual environment active
run: Used within docker and will also run kv_store locally. Requires a python3.8 virtual environment active
docker-build: builds a docker image for the server
docker-run: Runs the docker container for the server
docker-stop: Stops the container
docker-remove: Stops and removes the container so the image can be rebuilt
docker-clean: Removes the container and image
docker-net: Creates the bridge network the conatiners use
docker-unnet: Removes the docker container and images, and removes the bridge network. Note test_client must already be cleaned.
```

Test client has most of the same commands, minus the network ones. It also has 'logs', which will print the conatiner logs.
