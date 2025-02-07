from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

# Load LLM inference endpoints from an env variable or a file
# See https://docs.ag2.ai/docs/FAQ#set-your-api-endpoints
# and OAI_CONFIG_LIST_sample


def main():
    config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")
    # You can also set config_list directly as a list, for example, config_list = [{'model': 'gpt-4o', 'api_key': '<your OpenAI API key here>'},]
    assistant = AssistantAgent("assistant", llm_config={"config_list": config_list})
    user_proxy = UserProxyAgent(
        "user_proxy", code_execution_config={"work_dir": "coding", "use_docker": False}
    )  # IMPORTANT: set to True to run code in docker, recommended
    user_proxy.initiate_chat(
        assistant, message="Plot a chart of NVDA and TESLA stock price change YTD."
    )


if __name__ == "__main__":
    main()
