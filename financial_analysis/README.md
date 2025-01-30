# Financial Analysis Multi-Task Demo

This project demonstrates a sophisticated financial analysis system using AutoGen's multi-task async chat capabilities. The system coordinates multiple AI agents to analyze stock performance, investigate market trends, and generate comprehensive reports.

## Features

- Real-time stock data retrieval and analysis
- Multi-agent coordination for complex financial tasks
- Automated report generation with market insights
- Task dependency management and context sharing

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the demo:
```bash
python main.py
```

The system will:
1. Fetch current stock prices and performance metrics
2. Analyze market trends and factors
3. Generate visualizations
4. Produce a comprehensive report

## Implementation Details

The project uses AutoGen's `initiate_chats` interface to coordinate multiple specialized agents:
- Financial Assistant: Handles data retrieval and analysis
- Research Assistant: Investigates market trends
- Report Writer: Generates final analysis reports

Tasks are executed with proper dependencies, ensuring that analysis and reporting build upon previous findings.
