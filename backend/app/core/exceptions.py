<<<<<<< HEAD

=======
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

<<<<<<< HEAD
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"code": 422, "message": str(exc.errors()), "data": None})
=======

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for e in exc.errors():
        errors.append({"field": ".".join(str(loc) for loc in e["loc"]), "message": e["msg"]})
    return JSONResponse(status_code=422, content={"code": 422, "message": "请求参数校验失败", "data": {"errors": errors}})

>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(status_code=exc.status_code, content={"code": exc.status_code, "message": exc.detail, "data": None})

<<<<<<< HEAD
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"code": 500, "message": "Internal Server Error", "data": None})
=======

async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"code": 500, "message": "服务器内部错误", "data": None})
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
