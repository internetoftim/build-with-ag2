"""
Mock implementation of the DeepResearchAgent for testing purposes.
This module provides a drop-in replacement that simulates research functionality
without making actual API calls.
"""

import time
import random
from typing import Dict, List, Any, Optional, Union

class MockResearchResult:
    """Mock result object that mimics DeepResearchAgent's result."""
    def __init__(self, query: str):
        self.query = query
        self.summary = self._generate_mock_summary(query)
        self.cost = round(random.uniform(0.1, 1.5), 3)
        self.chat_history = self._generate_mock_chat_history()
        self.used_tools = self._generate_mock_used_tools()
        
    def _generate_mock_summary(self, query: str) -> str:
        """Generate a mock research summary based on the query."""
        # Dictionary of mock responses for different topics
        topics = {
            "databricks": "Databricks is a data analytics company founded in 2013 by the creators of Apache Spark. "
                         "It has raised over $3.5 billion in funding, with recent rounds including a $1.6 billion Series H "
                         "in August 2021 at a $38 billion valuation, led by Morgan Stanley. The company's most recent "
                         "funding was a $500 million Series I in September 2023, valuing the company at $43 billion. "
                         "Key investors include Andreessen Horowitz, BlackRock, and T. Rowe Price.",
                         
            "openai": "OpenAI is an AI research company founded in 2015 by Sam Altman, Elon Musk, and others. "
                     "The company has raised significant funding, including a $1 billion investment from Microsoft "
                     "in 2019, followed by a reported $10 billion investment in January 2023, valuing the company "
                     "at around $29 billion. They're known for developing GPT models, DALL-E, and other AI systems.",
                     
            "graphcore": "Graphcore is a UK-based semiconductor company that develops Intelligence Processing Units (IPUs) "
                        "designed specifically for artificial intelligence applications. Founded in 2016 by Nigel Toon "
                        "and Simon Knowles, the company has raised over $750 million across multiple funding rounds. "
                        "Notable investments include a $222 million Series E round in December 2020, led by Ontario "
                        "Teachers' Pension Plan Board, with participation from existing investors including Baillie Gifford.",
                        
            "default": "Based on my research, this topic involves several key aspects worth noting. There have been "
                      "significant developments in recent years, with major stakeholders contributing to its growth. "
                      "The historical context shows an evolution from early concepts to current implementations, "
                      "with funding and support increasing over time as value and potential have been demonstrated."
        }
        
        # Determine which topic the query is about
        query_lower = query.lower()
        for key, response in topics.items():
            if key in query_lower:
                return response
        
        # Return default response if no specific topic is matched
        return topics["default"]
    
    def _generate_mock_chat_history(self) -> List[Dict[str, str]]:
        """Generate a mock chat history."""
        return [
            {"role": "user", "content": f"Research {self.query}"},
            {"role": "assistant", "content": "I'll research this topic for you."},
            {"role": "assistant", "content": "Searching for relevant information..."},
            {"role": "assistant", "content": f"Here's what I found about {self.query}: {self.summary}"}
        ]
    
    def _generate_mock_used_tools(self) -> List[Dict[str, Any]]:
        """Generate a list of mock tools that were 'used' during the research."""
        return [
            {
                "name": "web_search",
                "input": {"query": self.query},
                "output": "Found 15 relevant results"
            },
            {
                "name": "read_webpage",
                "input": {"url": f"https://example.com/article-about-{self.query.replace(' ', '-')}"},
                "output": "Retrieved content from webpage"
            },
            {
                "name": "summarize_text",
                "input": {"text": "Long text about the research topic..."},
                "output": "Summarized text"
            }
        ]
    
    def process(self) -> None:
        """Mock the process method."""
        # Simulate processing time
        time.sleep(0.5)
        print(f"[MockResearchAgent] Processing research results for: {self.query}")


class MockDeepResearchAgent:
    """Mock implementation of DeepResearchAgent for testing."""
    
    def __init__(self, name: str, llm_config: Optional[Dict[str, Any]] = None):
        """Initialize the mock agent."""
        self.name = name
        self.llm_config = llm_config or {}
        self.tools = self._get_mock_tools()
        print(f"[MockResearchAgent] Initialized with name: {name}")
    
    def _get_mock_tools(self) -> List[Dict[str, Any]]:
        """Return a list of mock tool definitions."""
        return [
            {
                "name": "web_search",
                "description": "Search the web for information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query"
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "read_webpage",
                "description": "Read content from a webpage",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "URL of the webpage to read"
                        }
                    },
                    "required": ["url"]
                }
            },
            {
                "name": "summarize_text",
                "description": "Summarize a piece of text",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "The text to summarize"
                        }
                    },
                    "required": ["text"]
                }
            }
        ]
    
    def run(
        self, 
        message: str, 
        tools: Optional[List[Dict[str, Any]]] = None,
        max_turns: int = 5,
        user_input: bool = False,
        summary_method: str = "reflection_with_llm"
    ) -> MockResearchResult:
        """Mock the run method of DeepResearchAgent."""
        print(f"[MockResearchAgent] Running research on: {message}")
        print(f"[MockResearchAgent] Max turns: {max_turns}")
        print(f"[MockResearchAgent] Summary method: {summary_method}")
        
        # Simulate thinking time based on complexity of the query
        thinking_time = 1 + (len(message) * 0.01)
        thinking_time = min(thinking_time, 3)  # Cap at 3 seconds
        print(f"[MockResearchAgent] Thinking... (simulated delay: {thinking_time:.1f}s)")
        time.sleep(thinking_time)
        
        # Extract the actual query from the message
        query = message
        if "research" in message.lower():
            query = message.lower().replace("research", "").strip()
        
        # Generate and return a mock result
        return MockResearchResult(query)


# Example usage
if __name__ == "__main__":
    # Create a mock agent
    agent = MockDeepResearchAgent(name="MockResearcher", llm_config={"model": "gpt-4"})
    
    # Run a mock research query
    result = agent.run(
        message="Research the funding history of Databricks",
        max_turns=3,
        user_input=False
    )
    
    # Process and display the results
    result.process()
    print("\nResearch Summary:")
    print(result.summary)
    print(f"\nSimulated cost: ${result.cost}")
