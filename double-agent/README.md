# LemnlAgent

A project for building and managing LLM agents using the AG2 multiagent framework.

## Overview

This project implements a multi-agent system with two specialized agents:
1. **Conversational Agent**: Handles general conversation and information provision
2. **Tool-Calling Agent**: Specializes in running bash scripts and executing technical tasks

The agents can work together in a group chat to solve complex problems that require both conversation and technical execution.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- OpenAI API key
- AutoGen (AG2) framework

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/lemnlagent.git
   cd lemnlagent
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your OpenAI API key in the `OAI_CONFIG_LIST` file:
   ```json
   [
     {
       "model": "gpt-4o",
       "api_key": "your-openai-api-key-here"
     }
   ]
   ```

## Usage

Run the main script to start the multi-agent system:

```bash
python src/main.py
```

The system will initialize both agents and start a conversation where you can interact with them. The tool agent can run bash scripts on your behalf.

### Sample Bash Script

A sample bash script is provided in `src/sample_script.sh` that displays system information. You can ask the tool agent to run this script during your conversation.

## Project Structure

```
lemnlagent/
├── OAI_CONFIG_LIST      # Configuration for OpenAI API
├── README.md            # This file
├── requirements.txt     # Project dependencies
└── src/
    ├── main.py         # Main application with agent definitions
    └── sample_script.sh # Sample bash script for demonstration
```

## Customization

You can customize the agents by modifying their system messages in `src/main.py`. Add more tools to the tool agent or enhance the conversational capabilities as needed.
