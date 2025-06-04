from autogen import config_list_from_json, AssistantAgent, UserProxyAgent, LLMConfig
from autogen import GroupChat, GroupChatManager
from autogen.agents.experimental import DeepResearchAgent
from autogen.tools.experimental.google import GoogleCredentialsLocalProvider, GoogleDriveToolkit
import os
import datetime
import argparse


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


def authenticate_google_drive():
    """Authenticate with Google Drive and return credentials"""
    # Define paths for Google Drive authentication
    client_secret_file = "./credentials.json"
    token_file = "./token.json"
    
    # Set up provider for Google Drive authentication
    provider = GoogleCredentialsLocalProvider(
        client_secret_file=client_secret_file,
        scopes=GoogleDriveToolkit.recommended_scopes(),
        token_file=token_file,
    )
    
    # Get credentials (this will initiate OAuth flow if needed)
    credentials = provider.get_credentials()
    return credentials


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Deep Research Agent')
    parser.add_argument('--use-fake', action='store_true', help='Use fake research agent instead of the real one')
    parser.add_argument('--use-gdrive', action='store_true', help='Include Google Drive agent in the conversation')
    args = parser.parse_args()
    
    # Get the configuration for LLM models
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
        system_message="""You are a fake research agent.You don't have anything else to do but always return a made-up report about the topic you are researching. 
        As if you are the DeepResearchAgent.
        When asked for MRR projection return this data:
        Month 1: $25,000
        Month 2: $28,550
        Month 3: $32,635
        Month 4: $37,306
        Month 5: $42,620
        Month 6: $48,641
        Month 7: $55,442
        Month 8: $63,105
        Month 9: $71,718
        Month 10: $81,384
        Month 11: $92,214
        Month 12: $104,328
        """,
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
    
    # Agent 3: Data Handler Agent
    data_handler_agent = AssistantAgent(
        name="DataHandlerAgent",
        system_message="""You are a specialized data handler agent focused solely on data persistence.
        Your ONLY job is to receive data and save it correctly as text files. When you receive content:
        1. DO NOT summarize or analyze the content
        2. DO NOT engage in discussions about the content
        3. IMMEDIATELY save the received content using EITHER:
           a) The save_research_to_file function OR
           b) Direct Python code execution when more complex saving operations are needed
        4. Confirm the exact filepath where the data was saved
        5. Keep your responses extremely brief and focused on the file-saving operation
        
        When saving files, ensure they follow consistent naming patterns and always have .txt extensions.
        If you receive JSON data, format it properly before saving.
        If you receive tabular data, ensure it's aligned in columns with proper spacing.
        
        You can execute Python code directly when needed. For example:
        ```python
        import os
        import json
        from datetime import datetime
        
        # Format the data
        formatted_data = json.dumps(data, indent=2)
        
        # Generate a filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'data_{timestamp}.txt'
        
        # Create output directory if needed
        os.makedirs('data_output', exist_ok=True)
        
        # Save the file
        filepath = os.path.join('data_output', filename)
        with open(filepath, 'w') as f:
            f.write(formatted_data)
        
        print(f'Data saved to {filepath}')
        ```
        
        ALWAYS USE YOUR CODE EXECUTION CAPABILITIES when complex data formatting or specialized file handling is required.""",
        llm_config={"config_list": config_list},
        code_execution_config={
            "last_n_messages": 3,  # Consider last 3 messages for code generation
            "work_dir": "research_results",  # Use the same directory as save_research_to_file
            "use_docker": False,  # No need for Docker
        },
    )
    
    # Register the save_research_to_file function with the echo agent
    echo_agent.register_function(
        function_map={
            "save_research_to_file": save_research_to_file
        }
    )

    # Register the save_research_to_file function with the data handler agent
    data_handler_agent.register_function(
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

    # Register the save_research_to_file function with the user proxy and echoagent for testing
    for agent_obj in [user_proxy, echo_agent]:
        agent_obj.register_function(
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

    
    # Create group chat based on command-line argument
    if args.use_fake:
        print("Using FakeResearchAgent for testing...")
        research_agent = fake_agent
    else:
        print("Using DeepResearchAgent for real research...")
        research_agent = agent
    
    # Register the delegate_research_task function with all agents
    for agent_obj in [user_proxy, research_agent, echo_agent, data_handler_agent]:
        agent_obj.register_function(
            function_map={
                "delegate_research_task": delegate_research_task
            }
        )
        
    gdrive_agent = None
    if args.use_gdrive:
        try:
            # Get Google Drive credentials
            credentials = authenticate_google_drive()
            
            # Create directory for downloads
            os.makedirs("ag2_drive_downloads", exist_ok=True)
            
            # Create Google Drive agent
            gdrive_agent = AssistantAgent(
                name="GoogleDriveAgent", 
                llm_config={"config_list": config_list},
                system_message="""You are an agent that helps users access their Google Drive files.
                You can list files, download documents, search for specific files, and perform other Google Drive operations.
                When asked to get files, first list the available files to show the user what's available.
                Then offer to download specific files based on their selection or requirements.
                Always use the provided Google Drive API functions and only report actual results from these function calls.
                """
            )
            
            # Create and register Google Drive toolkit
            google_drive_toolkit = GoogleDriveToolkit(
                credentials=credentials,
                download_folder="ag2_drive_downloads",
            )
            
            # Register toolkit with the agent and user proxy for execution
            google_drive_toolkit.register_for_execution(user_proxy)
            google_drive_toolkit.register_for_llm(gdrive_agent)
            
            print("Google Drive agent initialized successfully")
        except Exception as e:
            print(f"Error initializing Google Drive agent: {e}")
            print("Continuing without Google Drive agent...")
    
    # Create a group chat and manager
    groupchat_agents = [user_proxy, echo_agent, research_agent, data_handler_agent]
    
    # Add Google Drive agent to the group chat if available
    if gdrive_agent:
        groupchat_agents.append(gdrive_agent)
        
    group_chat = GroupChat(
        agents=groupchat_agents, 
        messages=[], 
        max_round=50,
        speaker_selection_method="round_robin",
        allow_repeat_speaker=False,
    )
    group_chat_manager = GroupChatManager(groupchat=group_chat, llm_config={"config_list": config_list})

    # Start the conversation
    user_proxy.initiate_chat(
        group_chat_manager,
        message="What would you like to research deeply"
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
