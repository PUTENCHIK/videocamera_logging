from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse


app = FastAPI()


@app.get("/")
async def root():
    return {'message': "Hello on Videocamera Logging!"}


@app.get("/{any}")
async def other(any: str):
    raise Exception("No such page")


@app.exception_handler(Exception)
async def exception_handler(request: Request, ex: Exception):
    return JSONResponse(
        status_code=404,
        content=str(ex)
    )
