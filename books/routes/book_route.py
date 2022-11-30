import json
import boto3
import botocore

client = boto3.resource("dynamodb", region_name='us-east-1')


def find_all_books(title, author):
    table = client.Table('books')

    filter_expression = []
    expression_values = {}

    if title is not None:
        filter_expression.append('contains(title, :title)')
        expression_values[':title'] = title
    if author is not None:
        filter_expression.append('contains(author, :author)')
        expression_values[':author'] = author

    if title is not None or author is not None:
        response = table.scan(
            FilterExpression=' and '.join(filter_expression),
            ExpressionAttributeValues=expression_values
        )
    else:
        response = table.scan()

    data = response['Items']
    return 200, data


def find_book(book_id):
    table = client.Table('books')
    response = table.get_item(Key={
        'id': book_id
    })

    if 'Item' not in response:
        return 404, {}

    data = response['Item']
    return 200, data


def create_book(body):
    try:
        table = client.Table('books')
        table.put_item(
            Item={
                'id': body['id'],
                'title': body['title'],
                'author': body['author']
            },
            ConditionExpression='attribute_not_exists(id)'
        )
        return 201, body

    except KeyError as e:
        return 400, f'Field {e} is required'

    except botocore.exceptions.ClientError as x:
        error_code = x.response.get("Error", {}).get("Code")
        if error_code == "ConditionalCheckFailedException":
            return 409, f'Id already exists'
        else:
            return 400, f'ClientError: {x}'


def update_book(book_id, body):
    try:
        table = client.Table('books')
        response = table.update_item(
            Key={
                'id': book_id
            },
            UpdateExpression='SET title = :new_title, author = :new_author',
            ExpressionAttributeValues={
                ':new_title': body['title'],
                ':new_author': body['author'],
            },
            ConditionExpression='attribute_exists(id)',
            ReturnValues="UPDATED_NEW"
        )
        return 200, response['Attributes']

    except KeyError as e:
        return 400, f'Field {e} is required'

    except botocore.exceptions.ClientError as x:
        error_code = x.response.get("Error", {}).get("Code")
        if error_code == "ConditionalCheckFailedException":
            return 404, f'Book not found'
        else:
            return 400, f'ClientError: {x}'


def delete_book(book_id):
    try:
        table = client.Table('books')
        table.delete_item(
            Key={
                'id': book_id
            },
            ConditionExpression='attribute_exists(id)',
        )
        return 204, {}

    except botocore.exceptions.ClientError as x:
        error_code = x.response.get("Error", {}).get("Code")
        if error_code == "ConditionalCheckFailedException":
            return 404, f'Book not found'
        else:
            return 400, f'ClientError: {x}'


def book_router(event, route_key):
    # FIND ALL BOOKS
    if route_key == 'GET /books':
        if 'queryStringParameters' in event:
            title = event['queryStringParameters'].get('title')
            author = event['queryStringParameters'].get('author')
        else:
            title = None
            author = None
        return find_all_books(title, author)

    # FIND BOOK
    elif route_key == 'GET /books/{id}':
        book_id = event['pathParameters']['id']
        return find_book(book_id)

    # CREATE BOOK
    elif route_key == 'POST /books':
        body = json.loads(event['body'])
        return create_book(body)

    # UPDATE BOOK
    elif route_key == 'PUT /books/{id}':
        book_id = event['pathParameters']['id']
        body = json.loads(event['body'])
        return update_book(book_id, body)

    # DELETE BOOK
    elif route_key == 'DELETE /books/{id}':
        book_id = event['pathParameters']['id']
        return delete_book(book_id)

    # ENDPOINT NOT FOUND
    else:
        return 404, {}

