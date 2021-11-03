# Data API
Python API to handle storing and retrieving data from a database.
API is built with FastAPI, connected to MongoDB.
The API and DB each run in their own Docker container.


# Getting Started
## Linux/Mac
This guide assumes you have Docker installed previously.
The commands used assume that Docker has sufficient permission to run the commands without the use of `sudo`.
The commands assume your terminal is in the project root directory.


### Building and running the containers
Docker compose will handle everything as described in `docker-compose.yml`.

These commands should be run after any changes in order to apply the changes.

Before the containers can run, we must build the images:
```
docker compose build
```

Then we can start the containers:
```
docker compose up -d
```


### Connecting to the API
The API will now be available at `localhost:8000`
To view the auto-docs, navigate to `localhost:8000/docs` where you can view and test the routes directly.


### Stopping the containers
To stop the containers you can run:
```
docker compose down
```