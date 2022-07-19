## Product aggregator microservice BE Async version

This app was created based on requirements from company Applifting. Main goal was to create a REST API JSON Python microservice which allows users to browse a product catalog and which automatically updates prices from the oﬀer service (provided by Applifting). 

This is second iteration of app with async functionality enabled. Currently working on test suite
### Stack
- Python 3.10
- FastAPI
- SQLModel
- PostgreSQL
### Deployment
Application was deployed in form of Docker image to Heroku. App is accessible on this link
```javascript
https://applifting-product-aggregator.herokuapp.com/docs
```
### How to run locally
1. Pull the "async" branch from repository
```javascript
https://github.com/kalindan/applifting-be-task.git
```
2. Run following command to build and run containers of app and postgres db
```javascript
docker-compose up --build
```
3. Go to your browser and type following
```javascript
localhost:8080/docs
```
4. You should see SwaggerUI with all application endpoints ready to be tested
![Main screen](/docs/main_screen.png?raw=true)

### Product aggregator API
| Endpoints        | HTTP method | Description                |
|------------------|-------------|----------------------------|
| /login           |POST         | Login admin                |
| /products        |POST         | Create new product         |
| /products        |GET          | Get all products           |
| /products/{id}   |GET          | Get selected product       |
| /products/{id}   |PATCH        | Update product description |
| /products/{id}   |DELETE       | Delete selected product    |

### User workflow
Application divides between two user roles:
- Admin: After successful authentication, JWT token is generated. Token can be used to gain authorization for creation/update/deletion of products in database.
  - default username: admin
  - default password: admin
  - default token expiration time: 5 mins
![JWT Token](/docs/jwt_token.png?raw=true)
- General customer: Can get list of products and specific product with its actual offers.
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
- [ ] Write basic tests with pytest 
- [X] Push your code into a public repo on GitHub
- [X] Add a README with information on how to start and use your service 
- [X] JSON REST API simple authentication (eq.: access-token) 
- [X] Consider adding some reasonable error handling to the API layer
- [X] Provide a working Dockerﬁle and docker-compose.yml for your application for easy testing 
- [X] Use reasonable dependency management
- [X] Deploy your application to Heroku
