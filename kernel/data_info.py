from pydantic import BaseModel


class DataInfo(BaseModel):
    model_category: str
