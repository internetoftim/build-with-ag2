import json
from typing import Annotated


def format_todo_str(data):
    todo_str = "Current todos:\n"
    for i, todo in enumerate(data):
        todo_str += f"{i + 1}. {todo['task']} ({todo['status']})\n"
    return todo_str


def get_data():
    try:
        with open("todo.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []
    return data


def save_data(data):
    with open("todo.json", "w") as f:
        json.dump(data, f, indent=4)


def add_todo(
    id: Annotated[int, "task id"],
    task: Annotated[str, "task description"],
    status: Annotated[str, "task status, either done or open"],
):
    # if exist, load the data
    # if not exist, create empty list
    data = get_data()

    data.append(
        {
            "id": id,
            "task": task,
            "status": status,
        }
    )

    save_data(data)

    return f"Todo with id {id} added.\n" + format_todo_str(data)


def modify_todo(
    id: Annotated[int, "task id"],
    task: Annotated[str, "task description"],
    status: Annotated[str, "task status, either done or open"],
):
    data = get_data()
    is_todo_found = False
    for todo in data:
        if todo["id"] == id:
            todo["task"] = task
            todo["status"] = status
            is_todo_found = True
            break

    if not is_todo_found:
        msg = f"Todo with id {id} not found."
        add_msg = add_todo(id, task, status)
        return msg + "\n" + add_msg

    save_data(data)
    return f"Todo with id {id} updated.\n" + format_todo_str(data)


def delete_todo(id: Annotated[int, "task id"]):
    data = get_data()

    is_todo_found = False
    new_data = []
    for todo in data:
        if todo["id"] == id:
            is_todo_found = True
        else:
            new_data.append(todo)

    save_data(data)
    if is_todo_found:
        return f"Todo with id {id} deleted.\n" + format_todo_str(data)
    return f"Todo with id {id} not found. Nothing changed.\n" + format_todo_str(data)
