from fastapi import Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class Valor(BaseModel):
    value: str | int


class CustomError(BaseModel):
    code: int       # codigo http 400, 500, etc.
    message: str


def response_custom_pdf(data: bytes, file_name: str) -> Response:
    response = Response(content=data, media_type='application/pdf')
    response.headers['Content-Disposition'] = f'inline; filename={file_name}'
    return response


def response_custom_error(message: str, code: int = 500) -> dict:
    obj = CustomError(
        code=code,
        message=message
    )
    return JSONResponse(content=obj.__dict__, status_code=code)
