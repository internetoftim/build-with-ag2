from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
from autogen import GroupChat, GroupChatManager
import pandas as pd
import os
import re
from pathlib import Path

def read_excel_file(file_path):
    """
    Read an Excel file and return its contents as a pandas DataFrame.
    
    Args:
        file_path (str): Path to the Excel file
        
    Returns:
        pd.DataFrame: DataFrame containing the Excel data
    """
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        return f"Error reading Excel file: {str(e)}"


def create_visualization_code(df_name, plot_type, x_column=None, y_column=None, title="Visualization", output_file="visualization.png"):
    """
    Generate code for creating a visualization from a DataFrame.
    
    Args:
        df_name (str): Name of the DataFrame variable
        plot_type (str): Type of plot to create (bar, line, scatter, histogram, boxplot, heatmap)
        x_column (str): Column to use for x-axis
        y_column (str): Column to use for y-axis
        title (str): Title for the plot
        output_file (str): Output file path
        
    Returns:
        str: Python code to create the visualization
    """
    code = f"""import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 6))

"""
    
    if plot_type.lower() == "bar":
        code += f"sns.barplot(x='{x_column}', y='{y_column}', data={df_name})"
    elif plot_type.lower() == "line":
        code += f"sns.lineplot(x='{x_column}', y='{y_column}', data={df_name})"
    elif plot_type.lower() == "scatter":
        code += f"sns.scatterplot(x='{x_column}', y='{y_column}', data={df_name})"
    elif plot_type.lower() == "histogram":
        code += f"sns.histplot({df_name}['{x_column}'])"
    elif plot_type.lower() == "boxplot":
        code += f"sns.boxplot(x='{x_column}', y='{y_column}', data={df_name})"
    elif plot_type.lower() == "heatmap":
        code += f"sns.heatmap({df_name}.corr(), annot=True, cmap='coolwarm')"
    else:
        return f"Unsupported plot type: {plot_type}"
    
    code += f"""
plt.title('{title}')
plt.tight_layout()
plt.savefig('{output_file}')
plt.show()
"""
    
    return code

def save_dataframe_to_file(df, output_file="excel_data.txt"):
    """
    Save a DataFrame to a text file for easier viewing.
    
    Args:
        df (pd.DataFrame): DataFrame to save
        output_file (str): Output file path
    
    Returns:
        str: Path to the saved file
    """
    try:
        with open(output_file, "w") as f:
            f.write(str(df))
        return f"Data saved to {output_file}"
    except Exception as e:
        return f"Error saving data to file: {str(e)}"

def select_next_speaker(last_speaker, groupchat):
    """Custom state transition function for the group chat.
    
    This function determines which agent should speak next based on the conversation context.
    
    Args:
        last_speaker: The agent who spoke last
        groupchat: The GroupChat instance
        
    Returns:
        The next agent to speak
    """
    # Get the last message if there are messages
    messages = groupchat.messages
    if not messages:
        # If no messages yet, return None to use default selection
        return None
        
    last_message = messages[-1]["content"]
    last_speaker_name = messages[-1]["name"]
    
    # Extract all agents from the group chat
    all_agents = groupchat.agents
    agent_names = [agent.name for agent in all_agents]
    
    # Get the user proxy agent
    user_proxy = None
    for agent in all_agents:
        if isinstance(agent, UserProxyAgent):
            user_proxy = agent
            break
    
    # Get the specialized agents
    data_analyst = None
    assistant = None
    visualizer = None
    for agent in all_agents:
        if agent.name == "DataAnalyst":
            data_analyst = agent
        elif agent.name == "assistant":
            assistant = agent
        elif agent.name == "Visualizer":
            visualizer = agent
    
    # If the last message is from the user, the assistant should respond first
    if last_speaker_name == user_proxy.name:
        return assistant
    
    # If the message mentions Excel analysis or data analysis, the data analyst should respond
    excel_patterns = ["excel", "data analysis", "analyze", "dataframe", "pandas", "statistics"]
    if any(pattern in last_message.lower() for pattern in excel_patterns) and last_speaker_name != data_analyst.name:
        return data_analyst
        
    # If the message mentions visualization, the visualizer should respond
    viz_patterns = ["visualization", "plot", "chart", "graph", "figure", "bar chart", "line plot", "scatter plot", "histogram"]
    if any(pattern in last_message.lower() for pattern in viz_patterns) and last_speaker_name != visualizer.name:
        return visualizer
        
    # If the message mentions code execution or running code, the code executor should respond
    code_patterns = ["execute", "run", "code", "jupyter", "notebook", "script"]
    if any(pattern in last_message.lower() for pattern in code_patterns) and last_speaker_name != "Code_Executor":
        for agent in all_agents:
            if agent.name == "Code_Executor":
                return agent
    
    # If the message mentions summarizing or integrating code, the code summarizer should respond
    summary_patterns = ["summarize", "integrate", "combine", "full code", "complete code", "summary"]
    if any(pattern in last_message.lower() for pattern in summary_patterns) and last_speaker_name != "Code_Summarizer":
        for agent in all_agents:
            if agent.name == "Code_Summarizer":
                return agent
    
    # If the data analyst or visualizer just spoke, the assistant should interpret the results
    if last_speaker_name in [data_analyst.name, visualizer.name]:
        return assistant
    
    # Default to auto selection if no specific rule applies
    return None


def extract_python_code(content):
    """Extract Python code from markdown code blocks."""
    if "```python" in content:
        code = content.split("```python")[1].split("```")[0].strip()
        return code
    elif "```" in content:
        code = content.split("```")[1].split("```")[0].strip()
        return code
    return None

def save_code_to_file(code, filename="extracted_code.py"):
    """Save extracted code to a file."""
    filepath = os.path.join("workspace", filename)
    with open(filepath, "w") as f:
        f.write(code)
    return f"Code saved to {filepath}"

def main():
    # Load LLM inference endpoints
    config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")
    
    # Create the assistant agent (conversation coordinator)
    assistant = AssistantAgent(
        name="assistant", 
        llm_config={"config_list": config_list},
        system_message="""You are the conversation coordinator who helps users with Excel data analysis tasks.
        Your role is to understand the user's requests and coordinate with the DataAnalyst agent to fulfill them.
        You should explain the analysis process and results in user-friendly terms.
        
        When a user asks for Excel analysis, delegate the technical work to the DataAnalyst agent.
        Focus on making the insights accessible and actionable for the user."""
    )
    
    # Create the data analyst agent (specialized in Excel analysis)
    data_analyst = AssistantAgent(
        name="DataAnalyst",
        llm_config={"config_list": config_list},
        system_message="""You are an expert data analyst specializing in Excel data analysis.
        Your role is to perform technical analysis on Excel data and provide insights.
        
        You can use the following functions:
        - read_excel_file: To read Excel files into pandas DataFrames
        - save_dataframe_to_file: To save processed data to text files
        
        When analyzing data:
        1. First understand what data is available in the Excel file
        2. Perform appropriate statistical analysis based on the data type
        3. Generate insights about trends, patterns, and anomalies
        4. Suggest visualizations that would help understand the data better
        5. Provide code examples when appropriate
        
        Be thorough and precise in your analysis. Use pandas functions effectively.
        When visualization is needed, defer to the Visualizer agent."""
    )
    
    # Create the visualization agent
    visualizer = AssistantAgent(
        name="Visualizer",
        llm_config={"config_list": config_list},
        system_message="""You are a data visualization expert specializing in creating insightful visualizations from Excel data.
        Your role is to create effective visualizations that communicate insights clearly.
        
        You can use the following functions:
        - read_excel_file: To read Excel files into pandas DataFrames
        - create_visualization_code: To generate code for creating visualizations
        
        When creating visualizations:
        1. Choose the appropriate chart type based on the data and the insight to be communicated
        2. Select relevant columns for the x and y axes
        3. Use appropriate color schemes and styling
        4. Add clear titles and labels
        5. Explain why you chose a particular visualization and what insights it reveals
        
        Common visualization types and when to use them:
        - Bar charts: For comparing categories
        - Line plots: For showing trends over time
        - Scatter plots: For showing relationships between variables
        - Histograms: For showing distributions
        - Box plots: For showing statistical summaries
        - Heatmaps: For showing correlations between variables
        
        Instead of directly creating visualizations, you should generate Python code that the Code_Executor can run.
        Always provide complete code examples that can be executed by the Code_Executor agent."""
    )
    
    # Create the user proxy agent with the ability to execute code
    user_proxy = UserProxyAgent(
        name="user_proxy",
        human_input_mode="TERMINATE",  # Set to "ALWAYS" if you want to review and approve all code execution
        code_execution_config={
            "work_dir": "workspace",
            "use_docker": False,  # Set to True for safer code execution
        }
    )
    
    # Register the Excel-related functions with the user proxy and specialized agents
    for agent in [user_proxy, data_analyst]:
        agent.register_function(
            function_map={
                "read_excel_file": read_excel_file,
                "save_dataframe_to_file": save_dataframe_to_file,
            }
        )
        
    # Register visualization functions with the visualizer agent
    for agent in [user_proxy, visualizer]:
        agent.register_function(
            function_map={
                "read_excel_file": read_excel_file,
                "create_visualization_code": create_visualization_code,
            }
        )
    
    # Create the Code_Summarizer agent
    code_summarizer = AssistantAgent(
        name="Code_Summarizer",
        llm_config={"config_list": config_list},
        system_message="""You are the code summarizer. Given an Excel data analysis task and previous code snippets, 
        please integrate all error-free code into a single code snippet.
        Please also provide a brief summary of the data exploration, data processing, and analysis steps.
        You should give the full code to reproduce the data exploration, data processing, and analysis steps, 
        and show the results with different metrics and visualizations."""
    )
    
    # Register code extraction functions with the user proxy and code summarizer
    for agent in [user_proxy, code_summarizer]:
        agent.register_function(
            function_map={
                "extract_python_code": extract_python_code,
                "save_code_to_file": save_code_to_file,
            }
        )
    
    # Create the workspace directory if it doesn't exist
    os.makedirs("workspace", exist_ok=True)
    
    # Set up directories for code execution
    output_dir = Path("workspace/jupyter_output")
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Create the Code_Executor agent
    code_executor = UserProxyAgent(
        name="Code_Executor",
        system_message="Executor. Execute the code written by the analysts and report the result.",
        human_input_mode="NEVER",
        code_execution_config={
            "work_dir": "workspace",
            "use_docker": False,
            "last_n_messages": 3,  # Consider the last 3 messages for code execution
        }
    )
    
    # Create a group chat with all agents
    group_chat = GroupChat(
        agents=[assistant, data_analyst, visualizer, code_summarizer, code_executor, user_proxy],
        messages=[],
        max_round=50,
        speaker_selection_method=select_next_speaker,  # Use custom speaker selection
    )
    
    # Create a group chat manager
    group_chat_manager = GroupChatManager(groupchat=group_chat, llm_config={"config_list": config_list})
    
    # Start the conversation
    chat_result = user_proxy.initiate_chat(
        group_chat_manager,
        message="""I need help analyzing Excel files, creating visualizations, and executing code. 
        I can provide Excel files for you to analyze.
        Please guide me through the process of analyzing data, creating insightful visualizations, and executing code in Jupyter notebooks.
        You can also summarize the analysis and provide integrated code when needed.
        Then answer this question, how much are the sales per category in September Q3 of 2024."""
    )
    
    # Extract and save code from the conversation if available
    for message in reversed(chat_result.chat_history):
        if message["role"] == "Code_Summarizer":
            content = message["content"]
            code = extract_python_code(content)
            if code:
                save_code_to_file(code, "excel_analysis_summary.py")
                print("\nCode summary extracted and saved to workspace/excel_analysis_summary.py")
                break

if __name__ == "__main__":
    main()
