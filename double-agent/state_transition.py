from autogen import Agent, GroupChat
from typing import Dict, Any, Optional

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
    # Get the last message in the conversation
    last_message = groupchat.messages[-1]["content"] if groupchat.messages else ""
    last_message_lower = last_message.lower()
    
    # Get references to all agents by name
    agents_by_name = {agent.name: agent for agent in groupchat.agents}
    search_agent = agents_by_name.get("SearchAgent")
    profile_agent = agents_by_name.get("ProfileAgent")
    document_agent = agents_by_name.get("DocumentAgent")
    analysis_agent = agents_by_name.get("AnalysisAgent")
    user_proxy = agents_by_name.get("User")
    
    # If the user asks a question, the search agent should respond first
    if last_speaker.name == "User":
        if "search" in last_message_lower or "find" in last_message_lower or "looking for" in last_message_lower:
            return search_agent
        # If analysis is explicitly requested, go straight to analysis agent
        elif "analyze" in last_message_lower or "analysis" in last_message_lower:
            return analysis_agent
        # Default to search agent for most user queries
        return search_agent
        
    # If search agent just spoke, the profile agent should retrieve detailed information
    elif last_speaker.name == "SearchAgent":
        if "company_number" in last_message_lower or "found" in last_message_lower:
            return profile_agent
        # If no results found, return to user
        return user_proxy
        
    # If profile agent just spoke, the document agent should retrieve relevant documents
    elif last_speaker.name == "ProfileAgent":
        if "document" in last_message_lower or "filing" in last_message_lower:
            return document_agent
        # If no documents mentioned, go straight to analysis
        return analysis_agent
        
    # If document agent just spoke, the analysis agent should analyze the information
    elif last_speaker.name == "DocumentAgent":
        return analysis_agent
        
    # If analysis agent just spoke, go back to the user
    elif last_speaker.name == "AnalysisAgent":
        return user_proxy
        
    # Default back to the user if no other condition is met
    return user_proxy
