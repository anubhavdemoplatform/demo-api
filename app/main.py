from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Demo API", version="0.1.0")


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float


items: dict[int, Item] = {}
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
