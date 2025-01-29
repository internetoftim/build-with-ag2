## Trip Planning

- This code is forked from the [trip planning notebook](https://docs.ag2.ai/notebooks/agentchat_swarm_graphrag_trip_planner#trip-planning-with-a-falkordb-graphrag-agent-using-a-swarm) from AG2.
- By [Mark](https://github.com/marklysze)


In this project, we're building a trip planning swarm which has an objective to create an itinerary together with a customer. The end result will be an itinerary that has route times and distances calculated between activities.

## Details

The following diagram outlines the key components of the Swarm, with highlights being:

- FalkorDB agent using a GraphRAG database of restaurants and attractions
- Structured Output agent that will enforce a strict format for the accepted itinerary
- Routing agent that utilises the Google Maps API to calculate distances between activites
- Swarm orchestration utilising context variables

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
    The dependency is ag2 with graphrag option.

3. Set up a FalkorDB graph database. Please refer to [https://docs.falkordb.com/](https://docs.falkordb.com/). After the database is running, please adjust FalkorDB host and port accordingly (line 74-75 in `main.py`). A quick way is to set up docker and run this command:

    ```bash
    docker run -p 6379:6379 -p 3000:3000 -it --rm falkordb/falkordb:latest
    ```
    **Note:** You need to have a FalkorDB graph database running. If you are running one in a Docker container, please ensure your Docker network is setup to allow access to it.




## Run the code

### 1. Google Maps API Key

To use Google's API to calculate travel times, you will need to have enabled the `Directions API` in your Google Maps Platform. You can get an API key and free quota, see [here](https://developers.google.com/maps/documentation/directions/overview) and [here](https://developers.google.com/maps/get-started) for more details.

Once you have your API key, set your environment variable `GOOGLE_MAP_API_KEY` to the key.

### 2. Set Configuration and OpenAI API Key
By default, FalkorDB uses OpenAI LLMs and that requires an OpenAI key in your environment variable `OPENAI_API_KEY`.

You can utilise an OAI_CONFIG_LIST file and extract the OpenAI API key and put it in the environment, as will be shown in the following cell.

Alternatively, you can load the environment variable yourself.
Please modify the `config_list` in the `main.py` as needed. Read more about configurations [here](https://docs.ag2.ai/docs/topics/llm_configuration).

### 3. Run the code
```bash
python main.py
```

You can now interact with the system through the command line to plan a trip to Rome! You can also modify the initial message to plan a trip to another city.

## Contact

For more information or any questions, please refer to the documentation or reach out to us!

-	AG2 Documentation: https://docs.ag2.ai/docs/Home
-	AG2 GitHub: https://github.com/ag2ai/ag2
-	Discord: https://discord.gg/pAbnFJrkgZ


## License
This project is licensed under the Apache License 2.0. See the [LICENSE](../LICENSE) for details.
