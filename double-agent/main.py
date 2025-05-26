import os
import sys
from typing import Dict, Any, List, Tuple, Callable, Optional

from autogen import AssistantAgent, UserProxyAgent, config_list_from_json, Agent, GroupChat, GroupChatManager

# Configuration for API endpoints
def get_config_list():
    """Get the configuration for LLM models"""
    # You can replace this with a direct config if you have API keys
    # Example: return [{"model": "gpt-4o", "api_key": "your-api-key"}]
    try:
        config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")
        return config_list
    except Exception as e:
        print(f"Error loading config: {e}")
        # Fallback to empty config, you'll need to provide API key later
        return []

# Tool for running bash scripts
def bash_tool():
    """Create a tool for running bash scripts"""
    return {
        "type": "function",  # Required type field for OpenAI API
        "function": {
            "name": "run_bash_script",
            "description": "Run a bash script and return the output",
            "parameters": {
                "type": "object",
                "properties": {
                    "script": {
                        "type": "string",
                        "description": "The bash script to run",
                    },
                },
                "required": ["script"],
            },
        }
    }

# Function to execute bash script
def run_bash_script(script: str) -> Dict[str, Any]:
    """Execute a bash script and return the results"""
    import subprocess
    try:
        result = subprocess.run(
            ["bash", "-c", script], 
            capture_output=True, 
            text=True, 
            check=False
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode
        }
    except Exception as e:
        return {"error": str(e), "return_code": 1}


# Define a state transition function to select the next speaker based on the conversation context
def state_transition(
    last_speaker: Agent,
    groupchat: GroupChat
) -> Agent:
    """
    Determine which agent should speak next based on the conversation context.
    
    Args:
        last_speaker: The agent who sent the last message
        groupchat: The group chat instance
    
    Returns:
        The next agent to speak
    """
    # Get references to the agents by name
    conversation_agent = None
    tool_agent = None
    user_proxy = None
    
    # Find agents by their names
    for agent in groupchat.agents:
        if agent.name == "conversational_agent":
            conversation_agent = agent
        elif agent.name == "tool_agent":
            tool_agent = agent
        elif agent.name == "user_proxy":
            user_proxy = agent
    
    # Get all messages in the group chat
    messages = groupchat.messages
    
    # If no messages yet, start with conversation agent
    if not messages:
        return conversation_agent
    
    # Get the last message content
    last_content = ""
    if messages:
        last_content = messages[-1]["content"].lower()
    
    # Check if the last speaker was the user_proxy
    if last_speaker.name == "user_proxy":
        # If the message mentions bash, script, run, execute, or command, select the tool agent
        if any(keyword in last_content for keyword in ["bash", "script", "run", "execute", "command"]):
            return tool_agent
        else:
            # Otherwise, select the conversational agent
            return conversation_agent
    
    # If the last message was from the conversational agent and mentions needing technical help
    elif last_speaker.name == "conversational_agent" and any(keyword in last_content for keyword in ["technical", "script", "command", "bash", "execute"]):
        return tool_agent
    
    # If the last message was from the tool agent, let the user respond
    elif last_speaker.name == "tool_agent":
        return user_proxy
    
    # Default: let the user respond
    return user_proxy


def main():
    # Get the configuration for LLM models
    config_list = get_config_list()
    
    # Create the conversational agent
    conversational_agent = AssistantAgent(
        name="conversational_agent",
        system_message="""You are a helpful conversational agent. Your role is to engage in friendly, 
        informative conversation with the user. You should be polite, helpful, and provide 
        accurate information when possible. If you don't know something, it's okay to say so.
        You can also collaborate with the tool_agent when technical tasks need to be performed.
        
        If the user asks about running commands or scripts, politely defer to the tool_agent 
        who specializes in running bash scripts.""",
        llm_config={"config_list": config_list}
    )
    
    # Create the tool-calling agent that can run bash scripts
    tool_agent = AssistantAgent(
        name="tool_agent",
        system_message="""You are a tool-calling agent specialized in running bash scripts. 
        Your primary role is to help users execute technical tasks by running appropriate 
        bash commands. Be cautious with potentially destructive commands and always 
        consider security implications. Provide clear explanations of what the commands 
        do before running them. You can collaborate with the conversational_agent when 
        needed.
        
        You have access to a function called 'run_bash_script' that can execute bash commands.
        When asked to run a command, use this function to execute it securely.""",
        llm_config={
            "config_list": config_list,
            "tools": [bash_tool()]
        }
    )
    
    # Register function for bash script execution
    tool_agent.register_function({
        "run_bash_script": run_bash_script
    })
    
    # Create a user proxy agent with code execution capability
    user_proxy = UserProxyAgent(
        name="user_proxy",
        human_input_mode="ALWAYS",
        code_execution_config={
            "work_dir": "workspace",
            "use_docker": False  # Set to True if you want to use Docker for code execution
        }
    )
    
    # Start the conversation with a user message
    user_message = "Hello! I'd like to work with both a conversational agent and a tool agent that can run bash scripts."
    
    # Create a group chat with intelligent agent selection
    group_chat = GroupChat(
        agents=[conversational_agent, tool_agent, user_proxy],
        messages=[],
        max_round=50,
        speaker_selection_method=state_transition  # Use our custom state transition function
    )
    
    # Create a group chat manager with no additional LLM for speaker selection
    manager = GroupChatManager(groupchat=group_chat, llm_config=None)
    
    # Start the chat with initial message
    chat_result = user_proxy.initiate_chat(
        manager,
        message=user_message
    )
    
    # Return the chat result for potential post-processing
    return chat_result


if __name__ == "__main__":
    main()
