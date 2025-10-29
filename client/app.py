from fastapi import FastAPI, Request, HTTPException

from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pathlib import Path


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/static-index", response_class=JSONResponse)
async def static_index():
    static_dir = Path("static/assets").resolve()
    if not static_dir.exists():
        raise HTTPException(status_code=404, detail="Static folder not found")

    data = {}
    #rglob("*") means recursive glob every file and folder inside static_dir
    for path in static_dir.rglob("*"):
        if path.is_file():
            name = path.stem  # filename without extension
            rel_path = path.relative_to(static_dir).as_posix()
            #add to dictionary mapped to its name
            data[name] = f"/static/assets/{rel_path}"

    return data


@app.get("/game", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("game.html", {"request": request, "title":"Welcome!"})