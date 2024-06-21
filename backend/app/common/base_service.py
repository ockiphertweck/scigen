from pydantic import BaseModel
from typing import Any


class BaseService:
    def validate_data(self, data: BaseModel):
        """
        Validate the data using Pydantic's BaseModel.
        """
        return data.model_dump()

    def perform_action(self, data: Any):
        """
        A placeholder method to be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses should implement this method")
