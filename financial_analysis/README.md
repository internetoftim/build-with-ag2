# Financial Analysis Multi-Task Demo

This project demonstrates AutoGen's multi-task async chat capabilities through a financial analysis use case. The system coordinates multiple AI agents to analyze market data, investigate trends, and generate comprehensive reports.

## Features
- Multi-agent task coordination
- Sequential task execution with context sharing
- Automated report generation

## Configuration

Before running the demo, you need to set up your OpenAI API configuration:

1. Create a file named `OAI_CONFIG_LIST` in the project root
2. Configure your OpenAI API settings following the [AutoGen configuration guide](https://docs.ag2.ai/getting-started#configuration)

## Usage
```bash
pip install -r requirements.txt
python main.py
```

## Implementation Details
The project uses AutoGen's `a_initiate_chats` interface to coordinate specialized agents:
- Financial Assistant: Analyzes market data
- Research Assistant: Investigates market trends
- Report Writer: Generates final analysis reports

Tasks are executed with proper dependencies, ensuring that analysis and reporting build upon previous findings.

For more information about multi-task async chats in AutoGen, see the [documentation](https://docs.ag2.ai/notebooks/agentchat_multi_task_async_chats).
