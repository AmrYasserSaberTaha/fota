import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from API.routes import programme
from starlette.responses import RedirectResponse

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


@app.get("/", include_in_schema=False)
async def redirect_docs():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, host='localhost', port=int(os.environ.get('PORT', 8000)))
