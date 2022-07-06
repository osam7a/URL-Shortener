import database
import shortuuid
from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.get("/")
async def main():
    return {
        "HELLOE EE": "E TST "
    }

@app.get("/new")
async def new(link: str, custom_name: Union[str, None] = None):
    if not custom_name:
        _ = shortuuid.ShortUUID(alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        uuid = _.random(length=6)
        database.addLink(link, uuid)
        return {
            "status": "success",
            "link": link,
            "short_link": "shoort.ml/" + uuid
        }
    else:
        if len(custom_name) > 10:
            raise HTTPException(status_code=400, detail="Custom name must be less than 10 characters")
        if database.checkIfShortExists(custom_name):
            raise HTTPException(status_code=400, detail="Custom name already exists")
        database.addLink(link, custom_name)
        return {
            "status": "success",
            "link": link,
            "short_link": "shoort.ml/" + custom_name
        }

@app.get("/{short}")
async def redir(short: str):
    if database.checkIfShortExists(short):
        link = database.getLink(short)
        if not link.startswith("https://") or not link.startswith("http://"):
            link = "http://" + link
        return RedirectResponse(link)
    else:
        raise HTTPException(status_code=404, detail="We do not have such page!")
