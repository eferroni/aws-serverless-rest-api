import json
from health.routes.health_route import health_router
from books.routes.book_route import book_router


def build_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body)
    }


def lambda_handler(event, context):
    route_key = event['routeKey']
    path = route_key.split()[-1]

    # HEALTH
    if path == '/health':
        status_code, data = health_router(event, route_key)

    # BOOKS
    elif path in ['/books', '/books/{id}']:
        status_code, data = book_router(event, route_key)

    # ENDPOINT NOT FOUND
    else:
        status_code, data = 404, {}

    return build_response(status_code, data)

