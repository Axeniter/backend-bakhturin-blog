import time
from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from .schemas import PostResponse, PostCreate, PostUpdate
from src.routers import posts_router, comments_router
from src.database import engine
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()

app = FastAPI(title="Blog", lifespan=lifespan)
app.include_router(posts_router)
app.include_router(comments_router)

# logs
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    elapsed_ms = (time.time() - start) * 1000
    print(f"{request.method} {request.url.path} {response.status_code} {elapsed_ms:.1f}ms")
    return response

# exceptions 
@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    err = exc.errors()[0]
    loc = err["loc"]
    field = str(loc[-1]) if loc else "unknown"
    return JSONResponse(status_code=400, content={"error": err["msg"], "field": field})

