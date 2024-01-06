EXAMPLE_SPEC = {
    "resources": [
        {
            "db": {"engine": "Default", "path": ""},
            "name": "samples",
            "fields": [
                {
                    "name": "str",
                    "type": str,
                },
                {
                    "name": "str or none",
                    "type": str | None,
                },
                {
                    "name": "str default 'str'",
                    "type": str,
                    "default_value": "str",
                },
                {
                    "name": "str or none default 'str'",
                    "type": str | None,
                    "default_value": "str",
                },
                {
                    "name": "str or none default 'none'",
                    "type": str | None,
                    "default_value": None,
                    "has_default": True,
                },
                {
                    "name": "int",
                    "type": int,
                },
                {
                    "name": "float",
                    "type": float,
                },
                {
                    "name": "bool",
                    "type": bool,
                },
                {
                    "name": "list",
                    "type": list,
                },
                {
                    "name": "dict",
                    "type": dict,
                },
            ],
        }
    ]
}
