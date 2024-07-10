import typing
import pydantic


DefaultValue = typing.Any
DefaultFactory = typing.Callable | None


@pydantic.dataclasses.dataclass
class Default:
    default_value: DefaultValue = None
    default_factory: DefaultFactory = None

    @staticmethod
    def check_default(v):
        breakpoint()
        assert v, "default should not be empty"
        return v


@pydantic.dataclasses.dataclass
class FieldDefinition:
    name: str
    type: typing.Any
    default: typing.Annotated[Default | None, pydantic.BeforeValidator(Default.check_default)] = None


print(FieldDefinition(**{
    "name": "name",
    "type": str,
    "default": {
        "default_value": None,
        "default_factory": list,
    },
}))
