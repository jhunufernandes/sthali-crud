"""{...}."""
import json
import typing
import pathib

import yaml


class Types:
    any = typing.Any
    none = None
    bool = bool
    true = True
    false = False
    str = str
    int = int
    float = float
    list = list
    dict = dict


class ConfigException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def get_type(type_str: str) -> typing.Any:
    """Get the type based on the given type string.

    Args:
        type_str (str): The type string.

    Returns:
        typing.Any: The corresponding type.

    Raises:
        ConfigException: If the type string is invalid.
    """
    type_str = type_str.strip().lower()
    try:
        return getattr(Types, type_str)
    except AttributeError as exception:
        raise ConfigException("Invalid type") from exception


def load_and_parse_spec_file(spec_file_path: str) -> dict[str, typing.Any]:
    spec_dict = load_spec_file(pathlib.Path(spec_file_path))

    for resource in spec_dict["resources"]:
        for field in resource["fields"]:
            if isinstance(field["type"], str):
                field["type"] = get_type(field["type"])
            elif isinstance(field["type"], list):
                types_list = tuple(get_type(type) for type in field["type"])
                field["type"] = typing.Union[types_list]  # type: ignore
            else:
                raise ConfigException("Invalid field type")
            if "has_default" in field:
                field["has_default"] = get_type(field["has_default"])
    return spec_dict


def load_spec_file(spec_file_path: pathib.Path) -> dict[str, typing.Any]:
    spec_file_extension = spec_file_path.suffix.strip(".")
    if spec_file_extension not in ("yaml", "yml", "json"):
        raise ConfigException("Invalid file extension")

    with open(spec_file_path, "r", encoding="utf-8") as spec_file:
        return json.load(spec_file) if spec_file_extension == "json" else yaml.safe_load(spec_file)
