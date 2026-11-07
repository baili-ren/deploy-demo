from fastapi import FastAPI

from backend.routes import router

app = FastAPI(title='留言板 API')
app.include_router(router)
