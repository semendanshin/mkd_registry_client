from pydantic import BaseModel, ConfigDict, Field


class OrderCallbackInput(BaseModel):
    price: int
