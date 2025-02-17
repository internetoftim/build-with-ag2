import streamlit as st
import requests
import json

st.set_page_config(page_title="Deep Research Agent", layout="wide")

st.title("Deep Research Agent")

user_input = st.text_input("Enter your deep research question:", key="user_input")


def fetch_research_results(user_query):
    response = requests.post("http://127.0.0.1:8000/chat", json={"message": user_query})

    if response.status_code == 200:
        return response.json()  # ✅ Directly returns JSON
    else:
        return {"error": "Failed to fetch response"}


if st.button("Send"):
    if user_input:

        # Create a placeholder for the loading message
        loading_message = st.empty()

        # Show the loading message
        loading_message.subheader("🔍 Researching...")

        final_result_json = fetch_research_results(user_input)
        final_result = final_result_json.get("final_result", {})
        captured_output = final_result_json.get("captured_output", "")
        loading_message.empty()

        if captured_output:
            # Display summary separately
            if "summary" in final_result:
                st.subheader("📌 Summary")
                st.markdown(f"**{final_result['summary']}**")

            # Style like a shell
            st.subheader("📝 Captured Output")
            st.code(captured_output, height=400, language="shell")

            # Display cost breakdown
            if "cost" in final_result:
                st.subheader("💰 Cost Breakdown")
                cost_details = json.dumps(final_result["cost"], indent=2)
                st.code(cost_details, language="json")
