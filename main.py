from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from app.routers.enrollments import router as enrollments_router
from app.routers import auth
from app.routers.courses import router as courses_router
from app.core.logger import logger
import asyncio
from app.routers.uploads import router as uploads_router

app = FastAPI()

app.include_router(auth.router)
app.include_router(courses_router)
app.include_router(enrollments_router)
app.include_router(uploads_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "path": str(request.url)}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc} at {request.url}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "path": str(request.url)}
    )


@app.get("/", tags=["system"])
def home():
    return {"message": "Hello Backend"}


@app.get("/async-demo")
async def async_demo():

    await asyncio.sleep(5)

    return {
        "message": "Finished after 5 seconds"
    }