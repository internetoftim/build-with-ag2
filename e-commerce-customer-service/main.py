from autogen import config_list_from_json

from autogen.agentchat.contrib.swarm_agent import (
    ON_CONDITION,
    AfterWorkOption,
    SwarmAgent,
    initiate_swarm_chat,
    UserProxyAgent,
)

from prompts import (
    order_triage_prompt,
    tracking_order_prompt,
    login_in_management_prompt,
    order_management_prompt,
    return_prompt,
)
from functions import (
    verify_order_number,
    verify_user_information,
    login_account,
    get_order_history,
    check_order_status,
    check_return_eligibility,
    initiate_return_process,
)

# 1. Load the configuration file
config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")

# # 2. Load the keys directly
# config_list = [
#     {
#         "model": "gpt-4o",
#         "api_key": open("...", "r").read(),
#     }
# ]


llm_config = {
    "cache_seed": 42,  # change the cache_seed for different trials
    "temperature": 1,
    "config_list": config_list,
    "timeout": 120,
    "tools": [],
}

context_variables = {
    # retrieve for verfication
    "user_name": "Kevin Doe",
    "preferred_name": "Kev",
    "date_of_birth": "1998-02-01",
    "packages_information": "",
    "is_user_verified": False,
}

INIT_USER_INFO = {
    # when logging in
    "user_info": None,
    # for tracking agent
    "order_number": None,
    "order_info": None,
}


order_triage_agent = SwarmAgent(
    llm_config=llm_config,
    name="order_triage_agent",
    system_message=order_triage_prompt,
)

tracking_agent = SwarmAgent(
    name="order_tracking_agent",
    system_message=tracking_order_prompt,
    llm_config=llm_config,
    functions=[verify_order_number, verify_user_information],
)

login_agent = SwarmAgent(
    name="login_management_agent",
    system_message=login_in_management_prompt,
    llm_config=llm_config,
    functions=[login_account],
)

order_management_agent = SwarmAgent(
    name="order_management_agent",
    system_message=order_management_prompt,
    llm_config=llm_config,
    functions=[get_order_history, check_order_status],
)


return_agent = SwarmAgent(
    name="return_agent",
    system_message=return_prompt,
    llm_config=llm_config,
    functions=[check_return_eligibility, initiate_return_process],
)

to_login = ON_CONDITION(target=login_agent, condition="Transfer to the login agent")
order_triage_agent.register_hand_off(
    [
        to_login,
        ON_CONDITION(target=tracking_agent, condition="Transfer to the tracking agent"),
    ]
)
tracking_agent.register_hand_off(to_login)
order_management_agent.register_hand_off(
    ON_CONDITION(target=return_agent, condition="Transfer to the return agent")
)
return_agent.register_hand_off(
    ON_CONDITION(
        target=order_management_agent,
        condition="Transfer to the order management agent",
    )
)

user = UserProxyAgent(
    name="Customer",
    system_message="Agent that represents the Customer",
    code_execution_config=False,
)

chat_history = initiate_swarm_chat(
    initial_agent=order_triage_agent,
    agents=[
        order_triage_agent,
        tracking_agent,
        login_agent,
        order_management_agent,
        return_agent,
    ],
    context_variables=context_variables,
    messages="Hello",
    user_agent=user,
    max_rounds=40,
    after_work=AfterWorkOption.REVERT_TO_USER,
)
