from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.database import init_db
from routers import conversations

app = FastAPI()

@app.on_event("startup")
async def startup():
    init_db()
    
# Registro router
app.include_router(conversations.router, prefix="/conversations", tags=["Conversations"])

# Root endpoint
@app.get("/")
def root():
    return {"message": "Bienvenido al backend de conversaciones"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)