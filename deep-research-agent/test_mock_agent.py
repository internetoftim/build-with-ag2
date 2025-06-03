"""
Simple test script for the MockDeepResearchAgent.
"""

import os
from datetime import datetime
from mock_research_agent import MockDeepResearchAgent

def create_output_dir():
    """Create an output directory for research results if it doesn't exist."""
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_results")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def save_research_to_file(content, filename=None, directory=None):
    """Save research content to a text file."""
    if directory is None:
        directory = create_output_dir()
    
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_research_{timestamp}.txt"
    
    # Ensure the filename has a .txt extension
    if not filename.endswith('.txt'):
        filename += '.txt'
        
    filepath = os.path.join(directory, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\nResearch saved to: {filepath}")
    return filepath

def test_mock_agent():
    """Test the MockDeepResearchAgent directly."""
    print("\n===== Testing MockDeepResearchAgent =====\n")
    
    # Create output directory
    output_dir = create_output_dir()
    
    # Ask for a research topic
    query = input("Enter a research topic (or press Enter for default 'Databricks funding'): ") or "Databricks funding"
    
    # Create mock agent
    agent = MockDeepResearchAgent(name="MockResearcher", llm_config={"model": "gpt-4"})
    
    # Run the agent
    print(f"\nResearching: {query}...")
    result = agent.run(
        message=f"Research {query}",
        max_turns=3,
        user_input=False
    )
    
    # Process the result
    result.process()
    
    # Print results
    print("\n----- Research Results -----")
    print(f"Query: {query}")
    print(f"Simulated cost: ${result.cost}")
    print("\n--- Summary ---")
    print(result.summary)
    
    # Format and save the research
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_content = f"# Mock Research: {query}\n\n## Generated on: {timestamp}\n\n{result.summary}"
    
    # Save to file
    filename = f"mock_research_{query.replace(' ', '_').lower()[:20]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = save_research_to_file(formatted_content, filename, output_dir)
    
    print("\n===== Test Completed =====\n")
    
    return result, filepath

if __name__ == "__main__":
    test_mock_agent()
