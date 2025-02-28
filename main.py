import streamlit as st
import os

def main():
    st.set_page_config(page_title="Interface", layout="wide")
    
    # Sidebar Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Chat Interface", "Query History", "Coming Soon"])
    
    # Page Routing
    if page == "Chat Interface":
        chat_interface()
    elif page == "Query History":
        query_history()
    elif page == "Coming Soon":
        coming_soon()

# def chat_interface():
#     st.title("💬 Chat Interface")
#     st.write("This is where the chat UI will go.")

# API_URL = st.secrets["api"]["URL"]
# API_URL = "http://34.47.234.199:8000/generate_answer"

API_URL= os.getenv("API_URL")
if API_URL is None:
    st.write("API_URL is not set in the environment variables.")
else:
    st.write(f"API_URL is set to")
    
def chat_interface():
    """Chat interface with streaming response support."""
    st.title("💬 Chat Interface")
    
    # Sidebar: Input for Unique ID
    st.sidebar.title("Settings")
    unique_id = st.sidebar.text_input("Enter Unique ID", key="unique_id")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Display previous chat messages
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input field
    if query := st.chat_input("Ask a medical query..."):
        if not unique_id:
            st.warning("Please enter a Unique ID in the sidebar.")
        else:
            # Append user message to chat history
            st.session_state["messages"].append({"role": "user", "content": query})

            # Display user message
            with st.chat_message("user"):
                st.markdown(query)

            # Send request to API
            with st.chat_message("assistant"):
                response_container = st.empty()  # Placeholder for streaming response
                response_text = ""

                with requests.post(API_URL, json={"query": query, "unique_id": unique_id}, stream=True) as response:
                    for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                        if chunk:
                            response_text += chunk
                            response_container.markdown(response_text)

                # Append assistant response to chat history
                st.session_state["messages"].append({"role": "assistant", "content": response_text})



def query_history():
    st.title("📜 Query History")
    st.write("This is where past queries will be displayed.")

def coming_soon():
    st.title("🚧 Coming Soon")
    st.write("New features will be added here in the future!")

if __name__ == "__main__":
    main()
