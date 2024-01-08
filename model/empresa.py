from typing import Optional
from pydantic import BaseModel

class Empresa(BaseModel):
    documento: Optional[str]