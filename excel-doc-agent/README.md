# Excel-Doc Agent

This project demonstrates an AutoGen-based multi-agent system that can analyze Excel files, create visualizations, and execute code using AG2's GroupChat and GroupChatManager.

## Features

- Excel file reading and analysis using pandas
- Data visualization with matplotlib and seaborn
- Code execution in Jupyter notebooks
- Multi-agent collaboration between:
  - A conversational assistant agent (coordinator)
  - A data analyst agent (specialized in Excel data analysis)
  - A visualizer agent (specialized in creating visualizations)
  - A code summarizer agent (integrates code snippets)
  - A code executor agent (executes Python code)
  - A user proxy agent (handles user interactions and function execution)

## Installation

### Option 1: Automated Setup (Recommended)

Run the setup script to create a virtual environment and install all dependencies:

```bash
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -U autogen-agentchat
   pip install -r requirements.txt
   ```

## Configuration

1. Create an `OAI_CONFIG_LIST` file with your OpenAI API key:
   ```json
   [
     {
       "model": "gpt-4o",
       "api_key": "your-api-key"
     }
   ]
   ```

2. Place Excel files you want to analyze in the `workspace` directory.

## Usage

1. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

2. Run the main script:
   ```bash
   python main.py
   ```

3. Follow the prompts to interact with the agents. You can:
   - Ask the assistant to analyze Excel files
   - Request data analysis from the data analyst agent
   - Get visualizations from the visualizer agent
   - Execute code with the code executor agent
   - Get integrated code summaries from the code summarizer agent

## Example Commands

- "Read and analyze the Excel file 'sales_data.xlsx'"
- "Create a bar chart visualization of monthly sales"
- "Compare the data in 'sales_2024.xlsx' and 'sales_2023.xlsx'"
- "Execute this code to analyze the sales data"
- "Summarize all the code we've used for this analysis"

## Project Structure

- `main.py`: Main script with agent definitions and Excel processing functions
- `requirements.txt`: Python dependencies
- `setup.sh`: Automated setup script
- `workspace/`: Directory for Excel files and output files
- `workspace/jupyter_output/`: Directory for Jupyter notebook outputs

## Dependencies

- autogen-agentchat: For multi-agent system
- pandas: For Excel file processing
- openpyxl: For Excel file support
- xlrd: For older Excel file formats
- matplotlib & seaborn: For data visualization
- jupyter, nbformat, nbclient: For code execution in Jupyter notebooks
