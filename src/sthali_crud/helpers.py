"""General functions and classes.
"""
from .types import Model


class ModelClass:
    """Model base class.
    """
    _model: Model

    @property
    def model(self) -> Model:
        """Model property

        Returns:
            Model: Model.
        """
        return self._model

    @classmethod
    def replace_model(cls, model: Model) -> None:
        """Replace model property.

        Args:
            model (Model): New model.
        """
        cls._model = model
