# Fastapi rate limit example using token

This example, demonstrates how to apply rate limiting to a Fastapi project, based on the information from a JWT token.
It uses three external libraries: 

* [limits](https://limits.readthedocs.io/en/stable/installation.html) for managing rate limitation
* [FastAPI-Azure-Auth](https://intility.github.io/fastapi-azure-auth/installation/) for Azure AD authentication and getting valid access token
* [coredis](https://coredis.readthedocs.io/en/stable/) for using asynchronous Redis

It's connected to an Azure AD and authenticates users via OpenID Connect.

**Stack:**

* `Python 3.9.7+`
* `Fastapi 0.75.2+`
* `limits 2.6.1`
* `coredis 3.4.3`
* `FastAPI-Azure-Auth 3.3.0+`
* `Pytest 7.1.2+`

#### More about `FastAPI-Azure-Auth`

It's a small library which simplifies the connection between a FastAPI application with Azure AD authentication
After adding the library and setting the configuration for it, an `Authorize` button will show up in Swagger UI,
and you need to authenticate yourself before using the API endpoints. For more info, check [its documentations](https://intility.github.io/fastapi-azure-auth/).

It adds a `user` object to the `request` object of Fastapi which then you can extract user info from it.

```python
# e.g: Getting user's email from the token
email = request.state.user.claims["preferred_username"]
```

## How does it work

`Limits` is a library to help implement rate limiting. Since it hasn't been written for any specific python framework, I've made it suitable for `Fastapi` by creating a wrapper around it.

```python
from limits.aio.strategies import MovingWindowRateLimiter
from limits.storage import storage_from_string
from limits import parse

redis = storage_from_string(
    f"async+redis://{REDIS_HOST}:{REDIS_PORT}"
)

moving_window = MovingWindowRateLimiter(redis)
def handle_rate_limit(limitation_item: str):
    """
    This is used as a decorator for API routers to implement rate limitation
    :param limitation_item: limitation value (e.g: "2/minute", "10/day")
    :return: response
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, request: Request, **kwargs):
            email = request.state.user.claims["preferred_username"]
            is_allowed = await moving_window.hit(parse(limitation_item), email)
            if not is_allowed:
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={"message": "Maximum requests per time exceeded!"},
                )
            return await func(*args, request, **kwargs)

        return wrapper

    return decorator
```

Then you can use `handle_rate_limit` as decorator for your endpoints like this:

```python
@app.get("/")
@handle_rate_limit("2/minute")
async def homepage(request: Request):
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"message": "Hello There!"}
    )
```
__Notice__: the route decorator must be above the limit decorator

### Getting started

For simplifying the running the project, use the `Makefile` which is included in the project root folder:

**Running `docker-compose up --build`:**
```shell
make docker/build
```

**Installing requirements**
```shell
make requirements
```

**Run the unit tests**
```shell
make test
```

**Run the project locally**
```shell
make run
```

### Running the tests

The unit tests are written using `pytest`. To run them, simply run this command:
 
```shell
make test
```

### Project configuration
The project configuration can be found in the following module:
```
src/core/config.py
```
### How to test Azure AD authentication?
To test Azure AD authentication in local, you need to create an Azure tenant using your personal account and then 
register apps in you tenant. You can then use the Application client ID and Tenant ID to test the authentication 
with your personal microsoft account.

For more information about how to register apps in Azure, check out [this tutorial](https://intility.github.io/fastapi-azure-auth/single-tenant/azure_setup/).

### Environment variables
To run the project, you'll need to create a file called `.env` in the project root and write these variables in it:
```text
REDIS_HOST=redis
REDIS_PORT=6379
APP_CLIENT_ID=<YOUR_APP_CLIENT_ID>
TENANT_ID=<YOUR_TENANT_ID>
OPENAPI_CLIENT_ID=<YOUR_OPENAPI_CLIENT_ID>
```

To get your `APP_CLIENT_ID`, `TENANT_ID` and `OPENAPI_CLIENT_ID` refer to the section about __How to test Azure AD authentication?__