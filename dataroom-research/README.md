# DataRoom Research: AG2 DeepResearchAgent + GoogleDriveToolkit

- Created by [internetoftim](https://github.com/internetoftim)
- Last revision: 06/06/2025

DataRoom Research is an advanced multi-agent research system that combines the capabilities of DeepResearchAgent with GoogleDriveToolkit, built on the AG2 framework. It enhances OpenAI's deep research agent concept by adding document handling and Google Drive integration.

## Detailed Description

This project combines two powerful agent systems:

1. **DeepResearchAgent** - Inspired by OpenAI's deep research agent, it efficiently retrieves relevant data, processes information, and provides concise research conclusions.
   - https://openai.com/index/introducing-deep-research/

2. **Google Drive Integration** - Seamlessly integrates with Google Drive to access, download, and analyze documents stored in the cloud.

The system also features a professional report writer agent that creates well-structured markdown reports with proper formatting.

## AG2 Features

- [DeepResearchAgent](https://docs.ag2.ai/docs/blog/2025-02-13-DeepResearchAgent/index) - For advanced web research and data gathering
- [GoogleDriveToolkit](https://docs.ag2.ai/latest/docs/user-guide/reference-tools/google-api/google-drive/) - For seamless Google Drive integration

## TAGS

TAGS: deep-research, data-retrieval, google-drive, document-analysis, multi-agent, report-writer, automation, research-assistant, web-scraping

## Installation

DeepResearchAgent requires Python 3.11 or higher.

### Option 1: Automated Setup (Recommended)

Use the provided setup script to automatically create a virtual environment, install dependencies, and set up Playwright:

```bash
./setup.sh
```

This script will:
1. Create a Python virtual environment
2. Install all required packages
3. Install Playwright browsers automatically

### Option 2: Manual Installation

1. Create a virtual environment (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. If you are already using `autogen` or `pyautogen`, simply upgrade:

   ```bash
   pip install -U autogen[browser-use]
   ```

4. Install Playwright (required for web data retrieval):


   ```bash
   playwright install
   ```

## Running the code

Before running the system, you need to complete some configuration steps:

### 1. Configure API Access

#### OpenAI API Configuration
Create an `OAI_CONFIG_LIST` file based on the provided sample and update the `api_key` field with your OpenAI API key:

```bash
cp OAI_CONFIG_LIST_sample OAI_CONFIG_LIST
# Edit the file to add your API key
```
## 2. Using Local LLMs with Ollama (Optional)

This system supports using local language models through Ollama as an alternative to OpenAI's API. This can provide privacy benefits, reduce costs, and enable offline usage.

###  Setting Up Ollama

1. Install Ollama by following the instructions at [Ollama's official website](https://ollama.ai/download)

2. Pull a compatible model (we recommend models with at least 7B parameters):

```bash
# Install a model (example)
ollama pull deepseek-r1
# or another compatible model
ollama pull llama3:8b


#### 3. Google Drive Integration
To enable Google Drive features, you need OAuth credentials:

1. Create a Google Cloud project and enable the Drive API
2. Create OAuth 2.0 credentials and download as `credentials.json`
3. Place `credentials.json` in the project root directory

The system will automatically handle OAuth authentication on first run.

### 2. Run the System

#### Basic Command-line Interface

Run the main application with standard research capabilities:

```bash
python main.py
```

With Google Drive capabilities enabled:

```bash
python main.py --use-gdrive
```

For testing with simulated research responses:

```bash
python main.py --use-fake
```

#### Web Interface (Optional)

## Features and Capabilities

### DeepResearchAgent
- Conducts comprehensive web research on any given topic
- Uses the latest browser automation tools to gather accurate and up-to-date information
- Analyzes multiple sources to provide balanced, objective research
- Provides citations and references for all findings


### Google Drive Integration
- Lists files and folders from your Google Drive account
- Downloads documents for local processing
- Searches Drive for specific file types or content
- Integrates downloaded documents seamlessly with the document analysis capabilities

For a detailed tutorial on the Google Drive Toolkit functionality, see the [Official AG2 Google Drive Jupyter Notebook](https://github.com/ag2ai/ag2/blob/main/notebook/tools_google_drive.ipynb)

###  Report Generation
- The Report Writer agent creates well-structured markdown reports with proper sections
- Executive summaries, key findings, and detailed analysis in consistent formatting


<!-- Add any helpful resources here! -->

For more information or any questions, please refer to the documentation or reach out to us!

- View Documentation at: https://docs.ag2.ai/docs/Home
- Reachout to us: https://github.com/ag2ai/ag2
- Join Discord: https://discord.gg/pAbnFJrkgZ

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](../LICENSE) for details.
