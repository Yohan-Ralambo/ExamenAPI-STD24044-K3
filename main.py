from fastapi import FastAPI, requests
from starlette.requests import Request
from starlette.responses import JSONResponse, FileResponse
app = FastAPI()


@app.post("/welcome")
def welcome_user(request: app):
    return {f"Bienvenue {request.name}"}


