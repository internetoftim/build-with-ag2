import os
import autogen

# IMPORTS
import copy
from typing import Any, Dict


from autogen import (
    AFTER_WORK,
    ON_CONDITION,
    AfterWorkOption,
    SwarmAgent,
    SwarmResult,
    UserProxyAgent,
    initiate_swarm_chat,
)
from autogen.agentchat.contrib.graph_rag.document import Document, DocumentType
from graphrag_sdk.models.openai import OpenAiGenerativeModel
from autogen.agentchat.contrib.graph_rag.falkor_graph_query_engine import (
    FalkorGraphQueryEngine,
)
from autogen.agentchat.contrib.graph_rag.falkor_graph_rag_capability import (
    FalkorGraphRagCapability,
)

# local file imports
from ontology import get_trip_ontology
from google_map_platforms import Itinerary, update_itinerary_with_travel_times

# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# 1. Initialize the LLM Configuration

# Option 1: Load the configuration file
config_path = "OAI_CONFIG_LIST"
config_list = autogen.config_list_from_json(
    config_path, filter_dict={"model": ["gpt-4o"]}
)
# Option 2: Load the keys directly
# config_list = [
#     {
#         "model": "gpt-4o",
#         "api_key": open("...", "r").read(),
#     }
# ]

llm_config = {"config_list": config_list, "timeout": 120}
os.environ["OPENAI_API_KEY"] = config_list[0][
    "api_key"
]  # Put the OpenAI API key into the environment

# TODO: configure the Google API key
# os.environ["GOOGLE_MAP_API_KEY"] = open("<google_api_key_path>", "r").read()

# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# 2. Initialize the FalkorDB GraphRAG
input_paths = [
    "./trip_planner_data/attractions.json",
    "./trip_planner_data/cities.json",
    "./trip_planner_data/restaurants.json",
]
input_documents = [
    Document(doctype=DocumentType.TEXT, path_or_url=input_path)
    for input_path in input_paths
]

# Get the ontology
trip_data_ontology = get_trip_ontology()

# Create FalkorGraphQueryEngine
query_engine = FalkorGraphQueryEngine(
    name="trip_data",
    host="0.0.0.0",  # Change
    port=6379,  # if needed
    ontology=trip_data_ontology,
    model=OpenAiGenerativeModel("gpt-4o"),
)

# Ingest data and initialize the database
query_engine.init_db(input_doc=input_documents)

# If you have already ingested and created the database, you can use this connect_db instead of init_db
# query_engine.connect_db()


# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# Create Swarm Agents and start the conversation

trip_context = {
    "itinerary_confirmed": False,
    "itinerary": "",
    "structured_itinerary": None,
}


def mark_itinerary_as_complete(
    final_itinerary: str, context_variables: Dict[str, Any]
) -> SwarmResult:
    """Store and mark our itinerary as accepted by the customer."""
    context_variables["itinerary_confirmed"] = True
    context_variables["itinerary"] = final_itinerary

    # This will update the context variables and then transfer to the Structured Output agent
    return SwarmResult(
        agent="structured_output_agent",
        context_variables=context_variables,
        values="Itinerary recorded and confirmed.",
    )


def create_structured_itinerary(
    context_variables: Dict[str, Any], structured_itinerary: str
) -> SwarmResult:
    """Once a structured itinerary is created, store it and pass on to the Route Timing agent."""
    # Ensure the itinerary is confirmed, if not, back to the Planner agent to confirm it with the customer
    if not context_variables["itinerary_confirmed"]:
        return SwarmResult(
            agent="planner_agent",
            values="Itinerary not confirmed, please confirm the itinerary with the customer first.",
        )

    context_variables["structured_itinerary"] = structured_itinerary

    # This will update the context variables and then transfer to the Route Timing agent
    return SwarmResult(
        agent="route_timing_agent",
        context_variables=context_variables,
        values="Structured itinerary stored.",
    )


# Planner agent, interacting with the customer and GraphRag agent, to create an itinerary
planner_agent = SwarmAgent(
    name="planner_agent",
    system_message="You are a trip planner agent. It is important to know where the customer is going, how many days, what they want to do."
    + "You will work with another agent, graphrag_agent, to get information about restaurant and attractions. "
    + "You are also working with the customer, so you must ask the customer what they want to do if you don’t have LOCATION, NUMBER OF DAYS, MEALS, and ATTRACTIONS. "
    + "When you have the customer's requirements, work with graphrag_agent to get information for an itinerary."
    + "You are responsible for creating the itinerary and for each day in the itinerary you MUST HAVE events and EACH EVENT MUST HAVE a 'type' ('Restaurant' or 'Attraction'), 'location' (name of restaurant or attraction), 'city', and 'description'. "
    + "Finally, YOU MUST ask the customer if they are happy with the itinerary before marking the itinerary as complete.",
    functions=[mark_itinerary_as_complete],
    llm_config=llm_config,
)

# FalkorDB GraphRAG agent, utilising the FalkorDB to gather data for the Planner agent
graphrag_agent = SwarmAgent(
    name="graphrag_agent",
    system_message="Return a list of restaurants and/or attractions. List them separately and provide ALL the options in the location. Do not provide travel advice.",
)

# Adding the FalkorDB capability to the agent
graph_rag_capability = FalkorGraphRagCapability(query_engine)
graph_rag_capability.add_to_agent(graphrag_agent)

# Structured Output agent, formatting the itinerary into a structured format through the response_format on the LLM Configuration
structured_config_list = copy.deepcopy(config_list)
for config in structured_config_list:
    config["response_format"] = Itinerary

structured_output_agent = SwarmAgent(
    name="structured_output_agent",
    system_message="You are a data formatting agent, format the provided itinerary in the context below into the provided format.",
    llm_config={"config_list": structured_config_list, "timeout": 120},
    functions=[create_structured_itinerary],
)

# Route Timing agent, adding estimated travel times to the itinerary by utilising the Google Maps Platform
route_timing_agent = SwarmAgent(
    name="route_timing_agent",
    system_message="You are a route timing agent. YOU MUST call the update_itinerary_with_travel_times tool if you do not see the exact phrase 'Timed itinerary added to context with travel times' is seen in this conversation. Only after this please tell the customer 'Your itinerary is ready!'.",
    llm_config=llm_config,
    functions=[update_itinerary_with_travel_times],
)

# Our customer will be a human in the loop
customer = UserProxyAgent(name="customer", code_execution_config=False)

planner_agent.register_hand_off(
    hand_to=[
        ON_CONDITION(
            graphrag_agent,
            "Need information on the restaurants and attractions for a location. DO NOT call more than once at a time.",
        ),  # Get info from FalkorDB GraphRAG
        ON_CONDITION(structured_output_agent, "Itinerary is confirmed by the customer"),
        AFTER_WORK(
            AfterWorkOption.REVERT_TO_USER
        ),  # Revert to the customer for more information on their plans
    ]
)

# Back to the Planner when information has been retrieved
graphrag_agent.register_hand_off(hand_to=[AFTER_WORK(planner_agent)])

# Once we have formatted our itinerary, we can hand off to the route timing agent to add in the travel timings
structured_output_agent.register_hand_off(hand_to=[AFTER_WORK(route_timing_agent)])

# Finally, once the route timing agent has finished, we can terminate the swarm
route_timing_agent.register_hand_off(
    hand_to=[
        AFTER_WORK(AfterWorkOption.TERMINATE)
    ]  # Once this agent has finished, the swarm can terminate
)

# Start the conversation
chat_result, context_variables, last_agent = initiate_swarm_chat(
    initial_agent=planner_agent,
    agents=[planner_agent, graphrag_agent, structured_output_agent, route_timing_agent],
    user_agent=customer,
    context_variables=trip_context,
    messages="I want to go to Rome for a couple of days. Can you help me plan my trip?",
    after_work=AfterWorkOption.TERMINATE,
    max_rounds=100,
)


def print_itinerary(itinerary_data):
    header = "█             █\n █           █ \n  █  █████  █  \n   ██     ██   \n  █         █  \n █  ███████  █ \n █ ██ ███ ██ █ \n   █████████   \n\n ██   ███ ███  \n█  █ █       █ \n████ █ ██  ██  \n█  █ █  █ █    \n█  █  ██  ████ \n"
    width = 80
    icons = {"Travel": "🚶", "Restaurant": "🍽️", "Attraction": "🏛️"}

    for line in header.split("\n"):
        print(line.center(width))
    print(
        f"Itinerary for {itinerary_data['days'][0]['events'][0]['city']}".center(width)
    )
    print("=" * width)

    for day_num, day in enumerate(itinerary_data["days"], 1):
        print(f"\nDay {day_num}".center(width))
        print("-" * width)

        for event in day["events"]:
            event_type = event["type"]
            print(f"\n  {icons[event_type]} {event['location']}")
            if event_type != "Travel":
                words = event["description"].split()
                line = "    "
                for word in words:
                    if len(line) + len(word) + 1 <= 76:
                        line += word + " "
                    else:
                        print(line)
                        line = "    " + word + " "
                if line.strip():
                    print(line)
            else:
                print(f"    {event['description']}")
        print("\n" + "-" * width)


if "timed_itinerary" in context_variables:
    print_itinerary(context_variables["timed_itinerary"])
else:
    print("No itinerary available to print.")
