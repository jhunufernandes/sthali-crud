import datetime
import typing

import fastapi
import fastapi.templating


def app_context(request: fastapi.Request) -> dict[str, typing.Any]:
    return {
        "year": datetime.datetime.now(tz=datetime.timezone.utc).year,
        "app_name": "Sthali Auth",
        "git_revision": request.app.extra.get("git_revision", ""),
    }


templates = fastapi.templating.Jinja2Templates("src/sthali_crud/templates", context_processors=[app_context])
