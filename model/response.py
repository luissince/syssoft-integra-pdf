from pydantic import BaseModel

class Valor(BaseModel):
    value: str | int


def response_Valor(valor: str | int ) -> dict:

    obj = Valor(value = valor)

    return obj.__dict__


class CustomError(BaseModel):
    code: int       # codigo http 400, 500, etc.
    message: str    

def response_Custom_Error(message: str, code: int = 500) -> dict:

    obj = CustomError(
        code = code,
        message = message
    )

    # return obj.dict()
    return obj.__dict__