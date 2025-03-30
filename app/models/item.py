from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
  name: str
  description: Optional[str] = None
  price: float
  tax: Optional[float] = None

class ItemCreate(ItemBase):
  pass

class ItemUpdate(ItemBase):
  name: Optional[str] = None
  price: Optional[float] = None

class Item(ItemBase):
  id: int

  class Config:
    orm_mode = True
    # This allows the model to work with ORM objects
    # and convert them to Pydantic models
    # without needing to define the fields explicitly.
    # It also allows the model to work with dicts
    # and convert them to Pydantic models