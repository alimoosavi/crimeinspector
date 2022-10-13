Crime Inspector Project

The main purpose of this project is to visualize crimes that has been occurred in Chicago on map.

To run the project , you just need to have docker-compose installed on your machine:

````
       docker-compose build
       docker-compose up
````

For the first run , you also need to create crimes database in postgres container.
To do this try to exec to db container after composing up the containers and run the commands below:

````
    psql --username postgres
    create database crimes;
````
The project consists of 4 main components:

- crime-inspector:
This service is a django backend server on port 8000.
  
- streamlit-dashboard: this dashboard visualizes criminal data in Chicago using streamlit on port 8502.

- db: postgres service to store data.
- redis: redis service to cache data.

Also in crime-inspector service we have a django management command which
runs a synchronizer job to fetch criminal data from google big query
and populate the postgres database. The aim of this job is to work in background. When the dashboard calls backend api service ,
the backend service doesn't interface google big query service , it just needs to
query the postgres database. This solution to persist the data may not be good for all data applications
but in our project because of the size of our target dataset , it works fine to have a synchronizer job.

- To run this management command to fetch data chunk by chunk from google big query ,
  run the command below into bash of crime-inspector container:
  
````
    python3 manage.py sync_crimes
````

This command takes a while to be completed.