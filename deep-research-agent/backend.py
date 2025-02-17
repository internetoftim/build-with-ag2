from fastapi import FastAPI, Request
from autogen.agents.experimental import DeepResearchAgent
from autogen import config_list_from_json
import nest_asyncio
import io
import contextlib


nest_asyncio.apply()

app = FastAPI()


def run_agent(user_query):
    """Runs the agent synchronously and returns the final JSON result."""
    # Load config
    config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")

    # Initialize DeepResearchAgent
    agent = DeepResearchAgent(
        name="DeepResearchAgent",
        llm_config={"config_list": config_list},
    )

    # Run the agent (synchronous call)
    final_result = agent.run(
        message=user_query,
        tools=agent.tools,
        max_turns=2,
        user_input=False,
        summary_method="reflection_with_llm",
    )

    return final_result


@app.post("/chat")
async def chat(request: Request):
    """API Endpoint that returns only the final result as JSON."""
    data = await request.json()
    user_query = data.get("message", "")

    # Capture stdout without modifying the function
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        final_result = run_agent(user_query)

    captured_output = buffer.getvalue()

    results = {
        "final_result": final_result,
        "captured_output": captured_output,
    }
    return results
