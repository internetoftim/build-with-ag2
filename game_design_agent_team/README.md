# AI Game Design Agent Team

- This project is collected and modified from the [awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps) repository. Check out the original code [here](https://github.com/Shubhamsaboo/awesome-llm-apps/tree/main/ai_agent_tutorials/ai_game_design_agent_team).

The AI Game Design Agent Team is a collaborative game design system that generates comprehensive game concepts through the coordination of multiple specialized AI agents, each focusing on different aspects of game design based on user inputs such as game type, target audience, art style, and technical requirements. This is built on AG2's new [swarm feature](https://docs.ag2.ai/notebooks/agentchat_swarm#swarm-orchestration-with-ag2) run through initiate_chat() method.


## Description

**Agents and Workflow**
We initialize context variables (e.g., project details, user inputs) to store the relevant game design requirements. The AI Game Design Agent Team comprises the following specialized agents:
-	🎭 Story Agent:
Focuses on narrative design and world-building. Responsible for character backgrounds, lore, plot arcs, and dialogue.
-	🎮 Gameplay Agent:
Specializes in game mechanics, systems design, resource management, progression, balancing, and overall gameplay flow.
-	🎨 Visuals Agent:
Manages the art direction (including style guidelines, character/environment art, UI/UX) and also addresses audio elements like sound effects and music.
-	⚙️ Tech Agent:
Provides technical architecture and implementation guidance—engine selection, optimization strategies, networking requirements, platform constraints, and development roadmap.

When a user provides high-level game requirements (e.g., game type, setting, audience, visuals, platform), we start the swarm to allocate requirements to the respective specialized agents. Each agent elaborates on its area of expertise, and final outputs are combined into a cohesive game design proposal.

## Installation
1. Clone and navigate to the folder:
  ```bash
  git clone https://github.com/ag2ai/build-with-ag2.git
  cd build-with-ag2/game_design_agent_team
  ```
2. Install the required dependencies:
  ```bash
  pip install -r requirements.txt
  ```
The two dependencies are the ag2 (AG2) library and streamlit.

## Run the code

Before start, go to [OpenAI's platform](https://platform.openai.com/) to get an API key if you don't have one.

Run the Streamlit app to start a web interface for the AI Game Design Agent Team.
```bash
streamlit run ai_game_design_agent_team/game_design_agent_team.py
```

In the web interface to the left, put your OpenAI API key in the sidebar. 

Now you can interact with it through your browser, and click `Generate Game Concept` to receive a comprehensive design output from the specialized agents.

## Contact

For more information or any questions, please refer to the documentation or reach out to us!

- Original Code: https://github.com/Shubhamsaboo/awesome-llm-apps/tree/main/ai_agent_tutorials/ai_game_design_agent_team
-	AG2 Documentation: https://docs.ag2.ai/docs/Home
-	AG2 GitHub: https://github.com/ag2ai/ag2
-	Discord: https://discord.gg/pAbnFJrkgZ

## License

This project is licensed under the Apache License 2.0 from the [awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps). See the [LICENSE](./LICENSE) for details.