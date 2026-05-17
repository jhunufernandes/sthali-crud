# sthali-crud

FastAPI CRUD framework built on `sthali-db` and `sthali-core`. Auto-generates RESTful API routes for any SQLAlchemy model + Pydantic schema triplet.

## Project Structure

```
src/sthali_crud/
├── __init__.py         # SthaliCRUD app class, lifespan context manager
├── config.py           # ConfigSchema (crudmodels.database_uri), get_app_context, get_context_processors
├── dependencies.py     # PaginateParameters, paginate_parameters dependency alias
└── routers/
    ├── __init__.py     # Base router class (shared logic: handle_result, handle_list_result)
    └── api.py          # API router — full REST CRUD (POST/GET/PUT/PATCH/DELETE)
```

## Key Concepts

- **`SthaliCRUD`** — Main application class. Takes a config, `definitions_type` list, optional extended routers, and optional dependencies dict. For each `(Model, (Create, Read, Update))` tuple, it creates an `API` router and any extended routers (e.g., `VIEWS`). Stores metadata in `app.extra["crudmodels"]`.
- **`Base`** (routers) — Abstract base class for all routers. Holds `db_session`, model, and schemas. `handle_result()` converts ORM objects to schemas (raises 404 if None). `handle_list_result()` validates a list, collecting errors.
- **`API`** (routers/api.py) — Concrete CRUD router. `prefix = "/api/v1"`. Dynamically generates endpoint closures via `_make_*_endpoint()` methods. Uses `replace_type_hint()` to inject the correct schema type into FastAPI's OpenAPI introspection.
- **`PaginateParameters`** — Pydantic model for `skip`/`limit` query params. Injected via `Depends(PaginateParameters)`.
- **`lifespan`** — FastAPI lifespan context manager. DB connection test is currently commented out.

## Route Pattern

For a model with `__tablename__ = "projects"`:
- `POST /api/v1/projects/` → create
- `GET /api/v1/projects/{resource_id}/` → read
- `PUT /api/v1/projects/{resource_id}/` → update (full)
- `PATCH /api/v1/projects/{resource_id}/` → update (partial)
- `DELETE /api/v1/projects/{resource_id}/` → delete
- `GET /api/v1/projects/` → read many

## Config Schema (YAML)

```yaml
crudmodels:
  database_uri: "sqlite+aiosqlite:///app.db"
  dependencies: []  # optional list of dependency names
```

## Dependency Chain

`sthali-core`, `sthali-db` → `sthali-crud`

## Python Version

Requires Python >= 3.10.

## Known Issues / TODOs

- `SthaliCRUD.__init__` `config` parameter is untyped — should be `Config` from `sthali_core`.
- `register_api_router` uses `*args`/`**kwargs` with no annotations.
- `_make_delete_endpoint` calls `await session.delete(resource_id)` — this is wrong; should call `session.get()` first, then `session.delete(obj)`.
- `_make_read_many_endpoint` ignores `paginate_parameters` (skip/limit not applied to query).
- `lifespan` has commented-out DB test logic — should be restored.
- `dependencies["api_key"]` access in `register_api_router` will `KeyError` if no `api_key` dependency is set.
- No tests exist.

## Testing

```bash
cd /home/jhunu/sth/sthali-crud
/home/jhunu/sth/.venv/bin/python -m pytest tests/ -v
```

## Linting

```bash
/home/jhunu/sth/.venv/bin/ruff check src/
```

## Key Rules for AI

- Extended routers (like `VIEWS`) receive the `API` instance as an extra positional arg — the `register_api_router` method passes `*args` and `**kwargs` to the router constructor.
- `replace_type_hint` mutates `__annotations__` directly — needed because FastAPI reads annotations for OpenAPI schema generation, and the inner closure functions use generic `SchemaType`.
- Do not remove `# type: ignore` comments without verifying mypy passes — the SQLAlchemy TypeVar generics cause false positives.
