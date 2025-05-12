from fastapi import FastAPI
from app.database import engine,Base
from app.routers import post,user,auth,vote
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="My FastAPI Project",
    description="A production-ready backend API with JWT Auth, PostgreSQL, and modular routers.",
    version="1.0.0"
)
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "https://www.google.com",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router,prefix="/v1")
app.include_router(user.router,prefix="/v1")
app.include_router(auth.router,prefix="/v1")
app.include_router(vote.router,prefix="/v1")

@app.get("/")
def root():
    return {"message": "FastAPI is working !!!"}



