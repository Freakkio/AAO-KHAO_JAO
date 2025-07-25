from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Ensure this line is present
from app.api.v1.api import api_router
from app.core.config import settings

print(f"--- SERVER STARTING: Algorithm is '{settings.ALGORITHM}' ---")


app = FastAPI(title="Food Ordering API")

# --- CORS Middleware Configuration START ---
origins = [
    "http://localhost:3000", # The address of your frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- CORS Middleware Configuration END ---

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Food Ordering API"}