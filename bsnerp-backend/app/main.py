from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg

from .routers import auth, clients, projects, tasks, finance, servers, credentials, notifications, dashboard, settings

app = FastAPI(
    title="BSN ERP System",
    description="نظام إدارة موارد المؤسسة الشامل",
    version="1.0.0"
)

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(auth.router, prefix="/api")
app.include_router(clients.router, prefix="/api")
app.include_router(projects.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")
app.include_router(finance.router, prefix="/api")
app.include_router(servers.router, prefix="/api")
app.include_router(credentials.router, prefix="/api")
app.include_router(notifications.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(settings.router, prefix="/api")

@app.get("/api/healthz")
async def healthz():
    return {"status": "ok", "message": "BSN ERP System is running"}

@app.get("/")
async def root():
    return {"message": "مرحباً بك في نظام BSN ERP", "version": "1.0.0"}
