# Todo Management with RealtimeAgent

- This project used the template from this [example project](https://github.com/ag2ai/realtime-agent-over-websockets) by [Tvrtko](https://github.com/sternakt) and [Mark](https://github.com/marklysze).
- Todo management is added by [yiranwu0](https://github.com/yiranwu0)

From AG2 realtime agent example project, we build a todo management assistant that can be interacted through voice.

## Description

By starting the app, you can directly speak to the assistant to manage your todo list. The assistant will help you add, remove, and modify your todos. A local `todo.json` file will be created to save the todos.

### **Key Features**

- **WebSocket Audio Streaming**: Direct real-time audio streaming between the browser and server.
- **FastAPI Integration**: A lightweight Python backend for handling WebSocket traffic.
- **Resume chat**: The todos are saved in a local file and can be loaded when the server restarts.
- **Realtime Web Interface**: A simple web interface to show the todos and will be updated in real-time by the assistant.

## AG2 Features

This project demonstrates the following AG2 features:

- [Realtime Agent](https://docs.ag2.ai/docs/topics/realtime-agent)

## TAGS

TAGS: todo management, realtime agent, voice interaction, websocket streaming, fastapi, realtime updates, task automation

## Installation

### 1. Start by cloning the repository:

```bash
git clone https://github.com/ag2ai/build-with-ag2.git
cd manage-todos-with-realtime-agent
```

### 2. Then, install the required dependencies:

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

You need to obtain API keys from OpenAI or Gemini to use the realtime API. Sign up for OpenAI [here](https://platform.openai.com/), and Gemini [here](https://ai.google.dev/gemini-api/docs/api-key).
Then, create a `OAI_CONFIG_LIST` file based on the provided `OAI_CONFIG_LIST_sample`:

```bash
cp OAI_CONFIG_LIST_sample OAI_CONFIG_LIST
```

#### To use OpenAI Realtime API

1. In the OAI_CONFIG_LIST file, update the `api_key` to your OpenAI API key for the configuration with the tag "gpt-4o-mini-realtime"

#### To use Gemini Live API

1. In the OAI_CONFIG_LIST file, update the `api_key` to your Gemini API key for the configuration with the tag "gemini-realtime"
2. In main.py update [filter_dict tag] to "gemini-realtime".

## Run the code

Run the application with Uvicorn:

```bash
uvicorn main:app --port 5050
```

With the server running, open the client application in your browser by navigating to [http://localhost:5050/start-chat/](http://localhost:5050/start-chat/). Speak into your microphone, and the AI assistant will respond in real time.

## Contact

For more information or any questions, please refer to the documentation or reach out to us!

- Realtime Agent Blog: https://docs.ag2.ai/blog/2025-01-29-RealtimeAgent-with-gemini/index
- AG2 Documentation: https://docs.ag2.ai/docs/Home
- AG2 GitHub: https://github.com/ag2ai/ag2
- Discord: https://discord.gg/pAbnFJrkgZ

## **License**

This project is licensed under the [Apache 2.0 License](LICENSE).
