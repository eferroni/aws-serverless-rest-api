
def health():
    data = "Hello from AWS REST API :)"
    return 200, data


def health_router(event, route_key):
    if route_key == 'GET /health':
        return health()
