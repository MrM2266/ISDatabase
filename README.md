# ISDatabase
Database backend for university site. Project is based on SQLalchemy and graphQL.

- to start the app use following command:
uvicorn main:app --reload

- after application startup you can access the graphQL UI on ip given by uvicorn - remember to add /gql (example: http://127.0.0.1:8000/gql)
- by default after every startup the app creates some random database (not all tables are populated with data)
