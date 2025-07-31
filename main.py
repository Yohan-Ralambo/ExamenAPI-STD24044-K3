import base64
from typing import List
from fastapi import FastAPI, Header
from fastapi.openapi.utils import status_code_ranges
from pip._internal.utils import datetime
from pydantic import BaseModel
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response, FileResponse, PlainTextResponse

app = FastAPI()

@app.get("/ping")
def ping():
    return  FileResponse ("pong")

@app.get("/home")
def welcome():
    with open("welcome.html", "r", encoding="utf-8") as file:
        return Response(content="Welcome home!", status_code=200, media_type="text/html")

@app.get("/{full_path:path}")
def catch_all(full_path: str):
    with open("error.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content, status_code=404, media_type="text/html")


@app.post("/posts")
class PostModel(BaseModel):
    author: str
    title: str
    content: str
    creation_datetime: datetime

events_store: List[PostModel] = []

def serialized_stored_events():
    events_converted = []
    for event in events_store:
        events_converted.append(event.model_dump())
    return events_converted

@app.get("/posts")
def list_events():
    return {"posts": serialized_stored_events()}

@app.get("/posts")
def show():
    return Response(content= events_store, status_code=200)

@app.post('/posts')
def create_event(events: List[BaseModel]):
    for event in events:
        events_store.append(event)
    return {"posts" : serialized_stored_events()}



@app.get("/ping/auth", response_class=PlainTextResponse)
async def ping_auth(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authentication required", headers={"Content-Type": "text/plain"})

    if not authorization.startswith("Basic "):
        raise HTTPException(status_code=401, detail="Invalid authentication scheme", headers={"Content-Type": "text/plain"})

    base64_credentials = authorization.split(" ")[1]
    try:
        credentials = base64.b64decode(base64_credentials).decode("ascii")
        username, password = credentials.split(":")
        if username == "admin" and password == "123456":
            return "pong"
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials", headers={"Content-Type": "text/plain"})
    except:
        raise HTTPException(status_code=401, detail="Invalid credentials format", headers={"Content-Type": "text/plain"})
