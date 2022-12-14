#!/usr/bin/env python
import os

import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from payloads import BuildSTLRequest
from worker import add_build_request, get_progress

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/stl")
async def build_stl(request: BuildSTLRequest) -> dict:
    add_build_request(request)
    return {"hello": "world"}


@app.get("/stls")
async def get_stls() -> dict:
    stls =[]
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filenames = os.listdir(f"{dir_path}/../stls")
    filenames.sort()
    for filename in filenames:
        if filename.endswith(".stl"):
            stls.append({
                "name": filename,
                "triangles": 69,
                "filesize": os.path.getsize(os.path.join(f"{dir_path}/../stls/", filename)),
                "status": "done",
                "url": f"https://terraintostlapi.oram.ca/static/{filename}",
            })
    return {
        "stls": stls,
        "in_progress": get_progress(),
    }


app.mount("/static", StaticFiles(directory="../stls/"), name="stls")


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

