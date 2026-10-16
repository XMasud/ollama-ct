from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def root():
    return "<h1>Hello World</h1>"


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
