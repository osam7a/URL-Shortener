import database
import shortuuid
from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

meta = [
    {
        "name": "New",
        "description": "Add a new URL To our database"
    },
    {
        "name": "Redirect",
        "description": "Gets your link from our database and redirects you to it"
    }
]

app = FastAPI(
    title="Shoort URL Shortener",
    description="Shorten any URL Using our REST API",
    version="0.0.1 beta", 
    docs_url="/",
    openapi_tags=meta
    )

@app.get("/")
async def main():
    """
    Documentation
    """
    return RedirectResponse(url="/docs", status_code=200)

@app.get("/new", tags=["New"])
async def new(link: str, custom_name: Union[str, None] = None):
    """
    Add a short link to our database
    """
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
        if len(custom_name) > 20:
            raise HTTPException(status_code=400, detail="Custom name must be less than 20 characters")
        if database.checkIfShortExists(custom_name):
            raise HTTPException(status_code=400, detail="Custom name already exists")
        database.addLink(link, custom_name)
        return {
            "status": "success",
            "link": link,
            "short_link": "shoort.ml/" + custom_name
        }


@app.get("/{short}", tags=["Redirect"])
async def redir(short: str):
    if database.checkIfShortExists(short):
        link = database.getLink(short)
        if not link.startswith("https://") or not link.startswith("http://"):
            link = "http://" + link
        return RedirectResponse(link, status_code=200)
    else:
        raise HTTPException(status_code=404, detail="We do not have such page!")
