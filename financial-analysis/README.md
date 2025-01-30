# Financial Analysis of a Given Stock

- By [yiranwu0](https://github.com/yiranwu0)
- This project referenced the AG2 notebook [task solving with code generation, execution, and debugging](https://docs.ag2.ai/notebooks/agentchat_auto_feedback_from_code_execution#a-comparative-analysis-of-meta-and-tesla-stocks-in-early-2024)

This project retrieves news and stock price changes for a given stock symbol (e.g., AAPL) and generates a summarized market analysis report.

## Features
- Getting news from Yahoo Finance
- Getting stock price changes with Python Code
- Summarized report and analysis report generation -> `market_analysis_report.md`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ag2ai/build-with-ag2.git
cd financial-analysis
```

```bash
pip install -r requirements.txt
```
## Run the code

Before running the demo, you need to set up your OpenAI API configuration:

1. Create a file named `OAI_CONFIG_LIST` in the project root
2. Configure your OpenAI API settings following the [AutoGen configuration guide](https://docs.ag2.ai/getting-started#configuration)


```bash
python main.py
```

Checkout the generated `market_analysis_report.md` file for the summarized market analysis report.


## Contact

For more information or any questions, please refer to the documentation or reach out to us!
-	AG2 Documentation: https://docs.ag2.ai/docs/Home
-	AG2 GitHub: https://github.com/ag2ai/ag2
-	Discord: https://discord.gg/pAbnFJrkgZ


## License
This project is also licensed under the Apache License 2.0: [LICENSE](../LICENSE)
