from typing import List, Type
from pydantic import BaseModel

def convert_to_pydantic_list(sqlalchemy_objects: List, pydantic_model: Type[BaseModel]) -> List[BaseModel]:
    return [pydantic_model.from_orm(obj) for obj in sqlalchemy_objects]