### How to run locally
1. Pull the repository
2. Run following command to build and run containers of app and postgres db
```javascript
docker-compose up --build
```
3. Go to your browser and type following
```javascript
localhost:8080/docs
```
![This is an image](/docs/main_screen.png?raw=true)

### Product aggregator API
| Endpoints        | HTTP method | Description                |
|------------------|-------------|----------------------------|
| /login           |POST         | Login admin                |
| /products        |POST         | Create new product         |
| /products        |GET          | Get all products           |
| /products/{id}   |GET          | Get selected product       |
| /products/{id}   |PATCH        | Update product description |
| /products/{id}   |DELETE       | Delete selected product    |

### Requirements 
- [X] Provide an API to create, update and delete a product 
- [X] Periodically query the provided microservice for oﬀers/shops with products 
- [X] Provide an API to get product oﬀers
- [X] Data models:
  - [X] Product - id, name, description
  - [X] Offer - id, price, items_in_stock
- [X] Use an SQL database as an internal database
- [X] Request an access token from the oﬀers microservice
- [X] Provide this token for all calls to the Oﬀers microservice. 
- [X] Once a new Product is created, call the Oﬀers microservice to register it
- [X] Create a background (job) service which periodically calls the Oﬀers 
- [X] Create a read-only API for product oﬀers
- [X] Base URL for the Oﬀers MS should be conﬁgurable via an environment variable
- [X] Write basic tests with pytest 
- [X] Push your code into a public repo on GitHub
- [X] Add a README with information on how to start and use your service 
- [X] JSON REST API simple authentication (eq.: access-token) 
- [X] Consider adding some reasonable error handling to the API layer
- [X] Provide a working Dockerﬁle and docker-compose.yml for your application for easy testing 
- [X] Use reasonable dependency management
- [X] Deploy your application to Heroku