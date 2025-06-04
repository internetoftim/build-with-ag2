#!/usr/bin/env python3
from autogen import config_list_from_json, AssistantAgent, UserProxyAgent
from autogen.agentchat.groupchat import GroupChat
from autogen.agentchat.groupchat import GroupChatManager
from typing import Annotated, Optional

from autogen import AssistantAgent, LLMConfig
from autogen.tools import tool
from autogen.tools.experimental.google import GoogleCredentialsLocalProvider, GoogleDriveToolkit
from autogen.tools.experimental.google.model import GoogleFileInfo

# Google Drive Auth
client_secret_file = "./credentials.json"
token_file = "./token.json"

provider = GoogleCredentialsLocalProvider(
    client_secret_file=client_secret_file,
    scopes=GoogleDriveToolkit.recommended_scopes(),
    token_file=token_file,
)

credentials = provider.get_credentials()

llm_config = LLMConfig.from_json(
    path="OAI_CONFIG_LIST",
).where(model="gpt-4o")

assistant = AssistantAgent(name="assistant", llm_config=llm_config)

google_drive_toolkit = GoogleDriveToolkit(
    credentials=credentials,
    download_folder="ag2_drive_downloads",
)

user_proxy = UserProxyAgent(
    name="User",
    llm_config=llm_config,
    human_input_mode="ALWAYS",
    code_execution_config={"work_dir": "oauth_data", "use_docker": False},
)

google_drive_toolkit.register_for_execution(user_proxy)
google_drive_toolkit.register_for_llm(assistant)

# Create group chat
group_chat = GroupChat(
    agents=[user_proxy, assistant],
    messages=[],
    max_round=50,
    speaker_selection_method="auto",
)
group_chat_manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)

initial_message = "Get me the last 3 files and download all docs/sheets/slides file types. Ignore subfolders for now."

user_proxy.initiate_chat(group_chat_manager, message=initial_message)
