from fastapi import FastAPI
from .routers import summary, user, auth
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def root():
    return {"message": "Welcome on my api!!!!"}

app.include_router(summary.router)
app.include_router(user.router)
app.include_router(auth.router)