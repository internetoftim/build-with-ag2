import os
import autogen
from autogen import Agent, AssistantAgent, config_list_from_json, GroupChat, GroupChatManager, UserProxyAgent
from typing import Dict, Any
from dotenv import load_dotenv
from state_transition import state_transition

# Load environment variables
load_dotenv()

# Configuration for API endpoints
def get_config_list():
    """Get the configuration for LLM models"""
    try:
        config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")
        return config_list
    except Exception as e:
        print(f"Error loading config: {e}")
        # Fallback configuration
        return [
    {
        "model": "gpt-4-turbo",
        "api_key": os.environ.get("OPENAI_API_KEY"),
    }
]

# Get the configuration
config_list = get_config_list()

# Mock Companies House API functions
def mock_search_company(query: str) -> Dict[str, Any]:
    """Search for a company in Companies House by name or number."""
    companies = {
        "apple": {"company_number": "12345", "name": "Apple Ltd", "status": "active"},
        "microsoft": {"company_number": "67890", "name": "Microsoft UK Ltd", "status": "active"},
        "12345": {"company_number": "12345", "name": "Apple Ltd", "status": "active"},
    }
    # Simulate a search
    query = query.lower()
    if query in companies:
        return {"status": "success", "results": [companies[query]]}
    else:
        return {"status": "success", "results": []}

def mock_get_company_profile(company_number: str) -> Dict[str, Any]:
    """Get detailed profile for a company by its number."""
    profiles = {
        "12345": {
            "company_number": "12345",
            "name": "Apple Ltd",
            "registered_office_address": {
                "address_line_1": "1 Infinite Loop",
                "locality": "Cupertino",
                "country": "United Kingdom",
                "postal_code": "AB12 3CD"
            },
            "date_of_creation": "2010-01-01",
            "type": "private-limited-company",
            "status": "active"
        },
        "67890": {
            "company_number": "67890",
            "name": "Microsoft UK Ltd",
            "registered_office_address": {
                "address_line_1": "Microsoft Campus",
                "locality": "Reading",
                "country": "United Kingdom",
                "postal_code": "RG1 2XY"
            },
            "date_of_creation": "2005-05-15",
            "type": "private-limited-company",
            "status": "active"
        }
    }
    if company_number in profiles:
        return {"status": "success", "data": profiles[company_number]}
    else:
        return {"status": "error", "message": "Company not found"}

def mock_get_filing_history(company_number: str) -> Dict[str, Any]:
    """Get filing history for a company."""
    filings = {
        "12345": [
            {
                "transaction_id": "MzAwMDExNjU4OWFkaXF6a2N4",
                "date": "2023-12-01",
                "description": "Annual accounts",
                "type": "AA",
                "links": {"document_metadata": "/document/abc123"}
            },
            {
                "transaction_id": "MzEyMzExNjU4OWFkaXF6a2N4",
                "date": "2023-06-15",
                "description": "Confirmation statement",
                "type": "CS",
                "links": {"document_metadata": "/document/def456"}
            }
        ],
        "67890": [
            {
                "transaction_id": "NzEyMzExNjU4OWFkaXF6a2N4",
                "date": "2023-11-10",
                "description": "Annual accounts",
                "type": "AA",
                "links": {"document_metadata": "/document/ghi789"}
            }
        ]
    }
    if company_number in filings:
        return {"status": "success", "items": filings[company_number]}
    else:
        return {"status": "success", "items": []}

def mock_get_document(document_id: str) -> Dict[str, Any]:
    """Get a document by its ID."""
    documents = {
        "/document/abc123": {
            "document_id": "abc123",
            "content": "Annual accounts for Apple Ltd showing revenue of £1.2B and profit of £300M for fiscal year 2023."
        },
        "/document/def456": {
            "document_id": "def456",
            "content": "Confirmation statement for Apple Ltd confirming registered office and officers."
        },
        "/document/ghi789": {
            "document_id": "ghi789",
            "content": "Annual accounts for Microsoft UK Ltd showing revenue of £950M and profit of £220M for fiscal year 2023."
        }
    }
    if document_id in documents:
        return {"status": "success", "data": documents[document_id]}
    else:
        return {"status": "error", "message": "Document not found"}

def mock_save_to_database(data: Dict[str, Any]) -> Dict[str, Any]:
    """Save data to a mock database."""
    # In a real implementation, this would save to a database
    print(f"Saving to database: {data}")
    return {"status": "success", "message": "Data saved successfully", "id": "db-12345"}

# Define function schemas for Companies House API tools
search_company_schema = {
    "type": "function",
    "function": {
        "name": "search_company",
        "description": "Search for a company in Companies House by name or number",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Company name or number to search for"
                }
            },
            "required": ["query"]
        }
    }
}

get_company_profile_schema = {
    "type": "function",
    "function": {
        "name": "get_company_profile",
        "description": "Get detailed profile for a company by its number",
        "parameters": {
            "type": "object",
            "properties": {
                "company_number": {
                    "type": "string",
                    "description": "The company number"
                }
            },
            "required": ["company_number"]
        }
    }
}

get_filing_history_schema = {
    "type": "function",
    "function": {
        "name": "get_filing_history",
        "description": "Get filing history for a company",
        "parameters": {
            "type": "object",
            "properties": {
                "company_number": {
                    "type": "string",
                    "description": "The company number"
                }
            },
            "required": ["company_number"]
        }
    }
}

get_document_schema = {
    "type": "function",
    "function": {
        "name": "get_document",
        "description": "Get a document by its ID",
        "parameters": {
            "type": "object",
            "properties": {
                "document_id": {
                    "type": "string",
                    "description": "The document ID"
                }
            },
            "required": ["document_id"]
        }
    }
}

save_to_database_schema = {
    "type": "function",
    "function": {
        "name": "save_to_database",
        "description": "Save data to a database",
        "parameters": {
            "type": "object",
            "properties": {
                "data": {
                    "type": "object",
                    "description": "Data to save to the database"
                }
            },
            "required": ["data"]
        }
    }
}

# Define agents

# User Proxy Agent - This represents the human user
user_proxy = UserProxyAgent(
    name="User",
    system_message="You are a user interested in retrieving and analyzing company information from Companies House.",
    human_input_mode="NEVER",
    code_execution_config={
        "work_dir": "workspace",
        "use_docker": False,
    }
)

# Search Agent - Specializes in searching for companies
search_agent = AssistantAgent(
    name="SearchAgent",
    system_message="""You are a search specialist that helps find companies in the Companies House registry. 
    When asked to find information about a company, you search for it using the search_company function.
    You always respond with clear, structured information about the search results.
    You NEVER make up information and always use the provided tools.""",
    llm_config={"config_list": config_list}
)

# Profile Agent - Specializes in retrieving company profiles
profile_agent = AssistantAgent(
    name="ProfileAgent",
    system_message="""You are a company profile specialist that retrieves detailed information about companies.
    When given a company number, you use the get_company_profile function to fetch the company's details.
    You also use get_filing_history to retrieve the company's filing history when relevant.
    You always provide clear, structured responses based on the data you retrieve.""",
    llm_config={"config_list": config_list}
)

# Document Agent - Specializes in retrieving and processing documents
document_agent = AssistantAgent(
    name="DocumentAgent",
    system_message="""You are a document specialist that retrieves and processes documents from Companies House.
    When given a document ID, you use the get_document function to fetch the document's contents.
    You always provide clear summaries of the documents you retrieve.""",
    llm_config={"config_list": config_list}
)

# Analysis Agent - Specializes in analyzing company data
analysis_agent = AssistantAgent(
    name="AnalysisAgent",
    system_message="""You are a financial analysis specialist that analyzes company information.
    You examine company profiles, filing histories, and documents to extract valuable insights.
    You always provide clear, actionable analysis based on the data you receive.
    When you complete your analysis, you prepare the data for storage using the save_to_database function.""",
    llm_config={"config_list": config_list}
)

# Register functions with appropriate agents
search_agent.register_function({"search_company": mock_search_company})
profile_agent.register_function({
    "get_company_profile": mock_get_company_profile,
    "get_filing_history": mock_get_filing_history
})
document_agent.register_function({"get_document": mock_get_document})
analysis_agent.register_function({"save_to_database": mock_save_to_database})

# State transition function is now imported from state_transition.py

# Create a group chat with all agents
groupchat = GroupChat(
    agents=[user_proxy, search_agent, profile_agent, document_agent, analysis_agent],
    messages=[],
    max_round=12,
    speaker_selection_method=state_transition
)

# Create a group chat manager
manager = GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})

# Run the system
def main():
    # Start the conversation and automatically run the workflow
    # First, search for the company
    print("\nAutomatically running the Companies House multi-agent workflow:\n")
    result = mock_search_company("apple")
    print(f"1. Search result: {result}")
    
    # Get company profile and filing history
    company_number = result["results"][0]["company_number"]
    profile = mock_get_company_profile(company_number)
    filings = mock_get_filing_history(company_number)
    print(f"2. Company profile: {profile}")
    print(f"3. Filing history: {filings}")
    
    # Get document details
    document_id = filings["items"][0]["links"]["document_metadata"]
    document = mock_get_document(document_id)
    print(f"4. Document content: {document}")
    
    # Analyze and save to database
    analysis_data = {
        "company_name": profile["data"]["name"],
        "company_number": company_number,
        "status": profile["data"]["status"],
        "incorporation_date": profile["data"]["date_of_creation"],
        "latest_filing": filings["items"][0]["description"],
        "financial_summary": document["data"]["content"]
    }
    save_result = mock_save_to_database(analysis_data)
    print(f"5. Database save result: {save_result}")
    
    print("\nWorkflow complete! This demonstrates the full Companies House agent workflow.\n")
    print("In a real implementation, these functions would interact with the actual Companies House API.\n")
    
    # You could also initiate the chat-based workflow:
    # user_proxy.initiate_chat(
    #     manager,
    #     message="I need information about Apple Ltd. Can you search for it and analyze their latest financial data?"
    # )

if __name__ == "__main__":
    main()
