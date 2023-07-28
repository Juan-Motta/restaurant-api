from datetime import datetime

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import PydanticValueError

from app.main import app


class ApiError(ValueError):
    code: int = 400

    def __init__(self, message: str, code: int = 400):
        super().__init__(message)
        self.code = code


class ValidationError(PydanticValueError):
    msg_template = "Validation error"

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)


@app.exception_handler(ApiError)
async def custom_error_handler(request: Request, exc: ApiError):
    return JSONResponse(
        status_code=exc.code,
        content={
            "code": exc.code,
            "success": False,
            "message": str(exc),
            "time_stamp": datetime.now().strftime("%y-%m-%d %H:%M:%S"),
        },
    )


@app.exception_handler(RequestValidationError)
async def custom_error_handler(request: Request, exc: RequestValidationError):
    print(exc.errors())
    errors = [error.get("ctx") for error in exc.errors()]
    return JSONResponse(
        status_code=400,
        content={
            "code": 400,
            "success": False,
            "errors": errors,
            "time_stamp": datetime.now().strftime("%y-%m-%d %H:%M:%S"),
        },
    )
