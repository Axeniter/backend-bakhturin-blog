import time
from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from schemas import PostResponse, PostCreate, PostUpdate

app = FastAPI(title="Blog")

# db
posts = []
next_id = 1

def get_next_id() -> int:
    global next_id
    current = next_id
    next_id += 1
    return current

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

# endpoints
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/posts", status_code=201, response_model=PostResponse)
def create_post(data: PostCreate):
    post = {"id": get_next_id(), **data.model_dump()}
    posts.append(post)
    return post

@app.get("/api/posts", response_model=list[PostResponse])
def get_posts(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    author: str | None = None,
):
    items = posts
    if author is not None:
        items = [p for p in items if p["author"] == author]
    return items[offset: offset + limit]

@app.get("/api/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int):
    for p in posts:
        if p["id"] == post_id:
            return p
    raise HTTPException(status_code=404, detail="Post not found")

@app.patch("/api/posts/{post_id}", response_model=PostResponse)
def update_post(post_id: int, data: PostUpdate):
    for i, p in enumerate(posts):
        if p["id"] == post_id:
            p.update(data.model_dump(exclude_unset=True))
            return p
    raise HTTPException(status_code=404, detail="Post not found")

@app.delete("/api/posts/{post_id}", status_code=204)
def delete_post(post_id: int):
    for i, p in enumerate(posts):
        if p["id"] == post_id:
            posts.pop(i)
            return None
    raise HTTPException(status_code=404, detail="Post not found")
