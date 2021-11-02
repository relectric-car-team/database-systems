# Data API
Python API to handle storing and retrieving data from a database.
API is built with FastAPI, connected to MongoDB.
The API and DB each run in their own Docker container.


# Getting Started
## Linux/Mac
This guide assumes you have Docker installed previously.
The commands used assume that Docker has sufficient permission to run the commands without the use of `sudo`.


### Initial Setup
These commands need to be run only once.
`relectric` can be substituted for any alternative name you choose, but will also need to be substituted in later commands.

First we create a network that our containers will use to connect:
```
docker network create relectric
```

Then we create a local volume to persist the data from the database:
```
docker volume create relectric
```


### Building the images
Images will need to be built after any change to the Dockerfile.
The names can again be substituted if desired.

To build the API image, simply run:
```
docker build -f Python.Dockerfile -t relectric-api .
```

And the DB image:
```
docker build -f Mongo.Dockerfile -t relectric-db .
```


### Running the containers
Containers will need to be run after building the images or after being stopped.
If you changed the names above, remember to use the changed names in these commands.

The DB should run before the API:
```
docker run --net=relectric -v relectric:/var/lib/mongodb relectric-db
```

Then the API can be run:
```
docker run --net=relectric -p 8000:8000 relectric-api
```

`8000:8000` can be substituted with `x:8000`, where `x` is the local port you want to connect to the API with.


### Connecting to the API
The API will now be available at `localhost:8000` or an alternative port as described above.
To view the auto-docs, navigate to `localhost:8000/docs` where you can view and test the routes directly.