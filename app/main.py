import subprocess

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI(title="Demo API", version="0.1.0")

API_SECRET = "sk-demo-secret-key-12345"


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float


class UserNote(BaseModel):
    author: str
    content: str


items: dict[int, Item] = {}
notes: list[dict] = []
_next_id: int = 1


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/items")
def list_items():
    return [{"id": k, **v.model_dump()} for k, v in items.items()]


@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, **items[item_id].model_dump()}


@app.post("/items", status_code=201)
def create_item(item: Item):
    global _next_id
    items[_next_id] = item
    result = {"id": _next_id, **item.model_dump()}
    _next_id += 1
    return result


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]


@app.get("/items/search")
def search_items(q: str = Query(...)):
    results = []
    for k, v in items.items():
        if q.lower() in v.name.lower() or (v.description and q.lower() in v.description.lower()):
            results.append({"id": k, **v.model_dump()})
    return results


@app.post("/notes")
def create_note(note: UserNote):
    notes.append({"author": note.author, "content": note.content})
    return {"status": "saved", "total": len(notes)}


@app.get("/notes/export")
def export_notes(fmt: str = Query("txt")):
    result = subprocess.run(
        f"echo {fmt} export complete",
        shell=True, capture_output=True, text=True,
    )
    return {"output": result.stdout, "notes": notes}


@app.get("/debug/env")
def debug_env():
    return {"secret": API_SECRET, "item_count": len(items)}
