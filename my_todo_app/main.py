from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
import json
import os

app = FastAPI()

# 폰트적용을 위한 정적 파일
app.mount("/static", StaticFiles(directory="static"), name="static")

# To-Do 항목 모델
class TodoItem(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    important: bool

# JSON 파일 경로
TODO_FILE = "todo.json"

# JSON 파일에서 To-Do 항목 로드
def load_todos():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, "r") as file:
            return json.load(file)
    return []

# JSON 파일에 To-Do 항목 저장
def save_todos(todos):
    with open(TODO_FILE, "w") as file:
        json.dump(todos, file, indent=4)

# To-Do 목록 조회
@app.get("/todos", response_model=list[TodoItem])
def get_todos():
    return load_todos()

# 신규 To-Do 항목 추가
@app.post("/todos", response_model=TodoItem)
def create_todo(todo: TodoItem):
    todos = load_todos()

    # 새로운 id 1부터 할당
    next_id = max([t["id"] for t in todos], default=0) + 1
    new_todo = todo.model_dump()
    new_todo["id"] = next_id 

    todos.append(new_todo)
    save_todos(todos)
    return todo

# To-Do 항목 삭제
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    todos = load_todos()
    filtered_todos = [todo for todo in todos if todo["id"] != todo_id]

    if len(filtered_todos) == len(todos):
        raise HTTPException(status_code=404, detail="To-Do not found")

    save_todos(filtered_todos)
    return {"message": "To-Do deleted successfully"}

# HTML 파일 서빙
@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("templates/index.html", "r") as file:
        content = file.read()
    return HTMLResponse(content=content)
    