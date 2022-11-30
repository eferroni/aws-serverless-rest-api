
# Project - REST API with Serverless AWS Services:

A simple books public CRUD API created with API Gateway, AWS Lambda and DynamoDB.

Steps:
1. Create a DynamoDB table named `books`.
2. Create an AWS Lambda Function based on this repo (same folders).
3. Create an API Gateway.
4. Add the permissions bellow to the created Lambda IAM Role:
    1. AmazonDynamoDBFullAccess.
    2. CloudWatchLogsFullAccess.

## Rest API Routes:

Here are routes I already created:

### Books

|`/books`|||
|-|-|-|
|**Method**|**Route**|**Description**|
|GET|`/books/:id`|get one book|
|GET|`/books`|get all books|
|DELETE|`/books/:id`|delete one book|
|PUT|`/books/:id`|update one book|
|POST|`/books`|create one book|

## Postman Collection:
AWS_Serverless_REST_API.postman_collection.json

### To do:
- implement versioning
- dettach the logic from the functions - create usecases, dtos, entities and repositories
- implement authentication
- create a SAML file
