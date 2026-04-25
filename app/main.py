import uvicorn
from fastapi import FastAPI

from app.api_router.router import router as api_router

app = FastAPI(title="crypto API")
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
