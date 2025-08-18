### `SthaliCRUD`

```
A class to initialize and configure a FastAPI application with CRUD operations for specified resources.

    Attributes:
        app (fastapi.FastAPI): The FastAPI application instance.

    Args:
        app_spec (AppSpecification): The specification of the application, including title, description, summary,
            version, dependencies, and resources.
        lifespan (collections.abc.Callable[..., typing.Any]): The lifespan of the application.
            Defaults to default_lifespan.
    
```

