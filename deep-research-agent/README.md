# Reference implementation of AG2 DeepResearchAgent

- Created by [willhama](https://github.com/willhama)
- Last revision: 11/05/2025 by [willhama](https://github.com/willhama)

DeepResearchAgent is an advanced research tool built on the AG2 framework, inspired by OpenAI's deep research agent.

## Detailed Description

This is the reference implementation from OpenAI's deep research agent. It efficiently retrieves relevant data, processes information, and provides concise conclusions, helping analysts and investors make informed decisions.
https://openai.com/index/introducing-deep-research/

## AG2 Features

- [DeepResearchAgent](https://docs.ag2.ai/docs/blog/2025-02-13-DeepResearchAgent/index)

## TAGS

TAGS: deep-research, data-retrieval, automation, research-assistant, streamlit, uvicorn, web-scraping

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
   python -m playwright install
   ```

   **For Linux users only:**

   ```bash
   python -m playwright install-deps
   ```

## Running the code

Before running the demo, you need to set up your OpenAI API configuration. Create an `OAI_CONFIG_LIST` file based on the provided `OAI_CONFIG_LIST_sample` and update the `api_key` to your OpenAI API key for the configuration with the tag "gpt-4o". Change `filter_dict` tags in main.py if you want to use other models. Refer to [AutoGen configuration guide](https://docs.ag2.ai/getting-started#configuration) for more details.

```bash
cp OAI_CONFIG_LIST_sample OAI_CONFIG_LIST
```

```bash
python main.py
```

There is also a streamlit frontend and fastapi backend application that can be run with the following command:

1. Start the backend

```bash
uvicorn backend:app --reload
```

2. Start the frontend

```bash
streamlit run frontend.py
```

3. Visit your app on `http://localhost:8501/`

## Contact

<!-- Add any helpful resources here! -->

For more information or any questions, please refer to the documentation or reach out to us!

- View Documentation at: https://docs.ag2.ai/docs/Home
- Reachout to us: https://github.com/ag2ai/ag2
- Join Discord: https://discord.gg/pAbnFJrkgZ

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](../LICENSE) for details.
