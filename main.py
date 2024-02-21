import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from API.routes import programme

app: FastAPI = FastAPI()
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(programme.programmeRouter)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
