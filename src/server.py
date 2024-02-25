import os
import json
from fastapi import FastAPI, Path, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE_FOLDER="factmanga"
hidden_path = os.path.join(os.getcwd(), BASE_FOLDER)
templates = Jinja2Templates(directory="templates")

app = FastAPI()

# Utils
def get_all_contents(abs_folder_path):
    contents = []
    
    for item in os.listdir(abs_folder_path):
        item_path = os.path.join(abs_folder_path, item)
        item_data = {"name": item, 'path': item_path.split(hidden_path)[1]}

        if os.path.isfile(item_path):
            item_data["type"] = "file"
        else:
            item_data["type"] = "folder"
            sub_contents = get_all_contents(item_path) 
            item_data["contents"] = sub_contents 

        contents.append(item_data)
    return contents
  
@app.get("/folders/{folder_path}")
async def get_folder_structure(folder_path: str):
  abs_folder_path = os.path.join(hidden_path, folder_path.strip("/"))  # Ensure absolute path

  if not os.path.exists(abs_folder_path):
      return {"error": "Folder not found"}

  contents = get_all_contents(abs_folder_path)
  return {"folder_path": folder_path, "contents": contents}

@app.get("/")
def read_root(request: Request):
  return templates.TemplateResponse("./index.html",{"request":request})
    
@app.get("/read/{manga_name}")
def get_manga(manga_name: str, request: Request):
  abs_folder_path = os.path.join(hidden_path, manga_name.strip("/"))  # Ensure absolute path

  if not os.path.exists(abs_folder_path):
      return {"error": "Folder not found"}

  contents = get_all_contents(abs_folder_path)
  return templates.TemplateResponse("./manga.html", {"context": json.dumps(contents), "request": request})

  
app.mount("/static", StaticFiles(directory='factmanga'), name="static")



