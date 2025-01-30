from contextlib import asynccontextmanager
from logging import getLogger
from pathlib import Path
from typing import Annotated

import autogen
from autogen.agentchat.realtime_agent import RealtimeAgent, WebSocketAudioAdapter
from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .todo_utils import format_todo_str, get_data, save_data
import time

realtime_config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    file_location=Path(__file__).parent.parent,
    filter_dict={
        "tags": [
            "gemini-realtime"
        ],  # Use the tag of the model configuration defined in the OAI_CONFIG_LIST
    },
)

realtime_llm_config = {
    "timeout": 600,
    "config_list": realtime_config_list,
    "temperature": 0.8,
}

app = FastAPI()


@asynccontextmanager
async def lifespan(*args, **kwargs):
    print(
        "Application started. Please visit http://localhost:5050/start-chat to start voice chat."
    )
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/", response_class=JSONResponse)
async def index_page() -> dict[str, str]:
    return {"message": "WebSocket Audio Stream Server is running!"}


website_files_path = Path(__file__).parent / "website_files"

app.mount(
    "/static", StaticFiles(directory=website_files_path / "static"), name="static"
)

templates = Jinja2Templates(directory=website_files_path / "templates")


@app.get("/start-chat/", response_class=HTMLResponse)
async def start_chat(request: Request) -> HTMLResponse:
    """Endpoint to return the HTML page for audio chat."""
    port = request.url.port
    return templates.TemplateResponse("chat.html", {"request": request, "port": port})


@app.get("/todos")
def get_todos():
    data = get_data()
    return data


@app.websocket("/media-stream")
async def handle_media_stream(websocket: WebSocket) -> None:
    """Handle WebSocket connections providing audio stream and OpenAI."""
    await websocket.accept()

    logger = getLogger("uvicorn.error")

    audio_adapter = WebSocketAudioAdapter(websocket, logger=logger)

    system_message = """You are an AI voice assistant powered by AG2 and the OpenAI Realtime API.
You will help user manage todos. You can add, modify, and delete todos.

- When the user say something like "I need to do ...", call the add_todo function to add a new todo.
- When the user say something like "I have done ...", check if the todo is in the list and mark it as done using `modify_todo`. If not found, the assistant will add a new todo and mark it as done using `add_todo`.
- Help user modify or delete a todo as needed with `modify_todo` and `delete_todo` functions. Understand what todo the user is referring and get the correct todo.
- The task id should be assigned automatically by you, each task should have a unique id. The id starts from 1. You don't need to tell the user about task id.
"""
    system_message += "\nCurrent date and time: " + time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime()
    )
    data = get_data()
    if len(data) > 0:
        system_message += f"\n\nTodos from previous session:\n{format_todo_str(data)}"
    else:
        system_message += "\n\nNo todos from previous session."

    realtime_agent = RealtimeAgent(
        name="Weather Bot",
        system_message=system_message,
        llm_config=realtime_llm_config,
        audio_adapter=audio_adapter,
        logger=logger,
    )

    @realtime_agent.register_realtime_function(  # type: ignore [misc]
        name="add_todo", description="Add a todo"
    )
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

    @realtime_agent.register_realtime_function(  # type: ignore [misc]
        name="modify_todo", description="Modify a todo"
    )
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

    @realtime_agent.register_realtime_function(  # type: ignore [misc]
        name="delete_todo", description="Delete a todo"
    )
    def delete_todo(
        id: Annotated[int, "task id"],
        task: Annotated[str, "task description"],
        status: Annotated[str, "task status, either done or open"],
    ):
        logger.info(f"Deleting todo with id {id}, task {task}")
        data = get_data()

        is_todo_found = False
        new_data = []
        for todo in data:
            if todo["id"] == id:
                is_todo_found = True
            else:
                new_data.append(todo)

        data = new_data
        save_data(data)
        if is_todo_found:
            msg = f"Todo with id {id} deleted.\n" + format_todo_str(data)
        else:
            msg = f"Todo with id {id} not found. Nothing changed.\n" + format_todo_str(
                data
            )
        logger.info(f"Msg from delete: {msg}")
        return msg

    await realtime_agent.run()
