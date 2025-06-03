from autogen import config_list_from_json, AssistantAgent, UserProxyAgent
from autogen import GroupChat, GroupChatManager
from autogen.agents.experimental import DeepResearchAgent
import os
import datetime


def generate_filename(query):
    """Generate a filename based on the research query."""
    # Clean the query to create a filename-friendly string
    clean_query = query.replace(' ', '_').lower()
    clean_query = ''.join(c for c in clean_query if c.isalnum() or c == '_')
    
    # Add timestamp for uniqueness
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    return f"research_{clean_query}_{timestamp}.txt"


def save_research_to_file(content, filename=None, directory="research_results"):
    """Save research content to a text file."""
    # Create directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    
    # Generate filename if not provided
    if not filename:
        filename = generate_filename("research")
    
    # Ensure filename has .txt extension
    if not filename.endswith('.txt'):
        filename += '.txt'
    
    # Full path for the output file
    filepath = os.path.join(directory, filename)
    
    # Write content to the file
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print(f"\nResearch saved to: {filepath}")
    return filepath


def main():
    config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")
    # You can also set config_list directly as a list, for example, config_list = [{'model': 'gpt-4o', 'api_key': '<your OpenAI API key here>'},]

# Agent 1: DeepResearch Agent 

    agent = DeepResearchAgent(
        name="DeepResearchAgent",
        llm_config={"config_list": config_list},
    )
# Fake Reserach Agent for testing
    fake_agent = AssistantAgent(
        name="FakeResearchAgent",
        system_message="""You are a fake research agent.You don't have anything else to do but always return a made-up report about the topic you are researching. As if you are the DeepResearchAgent""",
        llm_config={"config_list": config_list},
    )


    # Agent 2: Echo Agent
    echo_agent = AssistantAgent(
        name="EchoAgent",
        system_message="""You are an assistant that echoes and summarizes research results.
        When you receive research content from the DeepResearchAgent or FakeResearchAgent, your job is to:
        1. Confirm receipt of the research
        2. Summarize the key points in bullet form
        3. Save the research to a file using the save_research_to_file function
        4. Ask if the user would like more details on any specific aspect
        Your role is currently a placeholder for future expansion, so keep your responses concise.""",
        llm_config={"config_list": config_list},
    )
    
    # Register the save_research_to_file function with the echo agent
    echo_agent.register_function(
        function_map={
            "save_research_to_file": save_research_to_file
        }
    )

    # Agent 3: User Proxy
    user_proxy = UserProxyAgent(
        name="User",
        human_input_mode="ALWAYS",
        code_execution_config={"work_dir": ".", "use_docker": False},
    )

    # Register the save_research_to_file function with the user proxy for testing
    user_proxy.register_function(
        function_map={
            "save_research_to_file": save_research_to_file
        }
    )
    
    # Define a custom function for the DeepResearchAgent to call
    def delegate_research_task(task):
        """Delegate research task to the DeepResearchAgent and return the result."""
        print(f"\n[System] Processing research task: {task}")
        result = agent.run(
            message=task,
            tools=agent.tools,
            max_turns=2,
            user_input=False,
            summary_method="reflection_with_llm",
        )
        result.process()
        return result.summary
    
    # Register the delegate_research_task function with all agents
    for agent_obj in [user_proxy, agent, echo_agent]:
        agent_obj.register_function(
            function_map={
                "delegate_research_task": delegate_research_task
            }
        )
    
    # Create group chat
    group_chat = GroupChat(
        agents=[ agent,echo_agent, user_proxy], #real deep research agent
        # agents=[ fake_agent,echo_agent, user_proxy],
        messages=[],
        max_round=50,
        speaker_selection_method="auto",
    )

    # Create group chat manager
    group_chat_manager = GroupChatManager(groupchat=group_chat, llm_config={"config_list": config_list})

    # Start the conversation
    user_proxy.initiate_chat(
        group_chat_manager,
        message="What would you like to research deeply",
    )

    # first_message = input("What would you like to research deeply?: ")

    # result = agent.run(
    #     message=first_message,
    #     tools=agent.tools,
    #     max_turns=2,
    #     user_input=False,
    #     summary_method="reflection_with_llm",
    # )

    # print("#### DEEP RESEARCH RESULT ####")
    # result.process()
    # print(result.summary)


if __name__ == "__main__":
    main()
