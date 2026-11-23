from fastapi import FastAPI, HTTPException

app = FastAPI()

# Simple list to store tasks in memory
tasks = []
next_id = 1


# 1. Root endpoint
@app.get("/")
def home():
    return {"version": "1.0", "endpoints": ["/tasks"]}


# 2. Health check
@app.get("/health")
def health():
    return {"status": "ok"}


# 3. Create a task (POST)
@app.post("/tasks", status_code=201)
def create_task(task: dict):
    global next_id

    # Check if 'title' is missing or empty
    if not task.get("title"):
        raise HTTPException(status_code=400, detail="Title is required")

    new_task = {
        "id": next_id,
        "title": task["title"],
        "completed": task.get("completed", False)
    }
    tasks.append(new_task)
    next_id += 1
    return new_task


# 4. Get all tasks (GET)
@app.get("/tasks")
def get_tasks():
    return tasks


# 5. Get one task by ID (GET)
@app.get("/tasks/{task_id}")
def get_one_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


# 6. Update a task (PUT)
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_data: dict):
    for task in tasks:
        if task["id"] == task_id:
            if "title" in updated_data:
                task["title"] = updated_data["title"]
            if "completed" in updated_data:
                task["completed"] = updated_data["completed"]
            return task
    raise HTTPException(status_code=404, detail="Task not found")


# 7. Delete a task (DELETE)
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")