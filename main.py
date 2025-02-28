import streamlit as st
import os
import requests
from qdrant_client import QdrantClient

# ✅ Ensure page config is first
st.set_page_config(page_title="Interface", layout="wide")

# ✅ Load API URL (handles both local and Streamlit Cloud)
API_URL = os.getenv("API_URL", st.secrets.get("api", {}).get("URL"))
if API_URL is None:
    st.warning("API_URL is not set in the environment variables or Streamlit secrets.")

qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
 )

collection_name = "EMR-Chains-Data"
def list_unique_ids_in_collection(qdrant_client, collection_name, limit=100):
    unique_ids = set()
    next_page_offset = None

    while True:
        points, next_page_offset = qdrant_client.scroll(
            collection_name=collection_name,
            with_payload=True,
            limit=limit,
            offset=next_page_offset,
        )

        for point in points:
            if "unique_id" in point.payload:
                unique_ids.add(point.payload["unique_id"])

        if next_page_offset is None:
            break

    return list(unique_ids)


def main():
    st.markdown(
        """
        <style>
        h1 { margin-top: -10px; }  /* Adjust as needed */
        </style>
        """,
        unsafe_allow_html=True
    )
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

def chat_interface():
    """Chat interface with streaming response support."""
    st.markdown("<style>h1 { margin-top: -50px; }</style>", unsafe_allow_html=True)
    
    # Create two columns: one for the title and one for the unique ID input field
    col1, col2 = st.columns([3, 2])  # Adjust width ratio if needed

    with col1:
        st.title("💬 Chat Interface")

    with col2:
        unique_ids = list_unique_ids_in_collection(qdrant_client, collection_name)
        unique_id = st.selectbox("**Select Unique ID:**", index=None,placeholder="Select Unique ID...", options = unique_ids
 
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Display previous chat messages
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input field
    if query := st.chat_input("Ask a query..."):
        if not unique_id:
            st.warning("Please Select a Unique ID.")
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

                try:
                    with requests.post(API_URL, json={"query": query, "unique_id": unique_id}, stream=True) as response:
                        response.raise_for_status()  # Ensure valid response
                        for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                            if chunk:
                                response_text += chunk
                                response_container.markdown(response_text)

                    # Append assistant response to chat history
                    st.session_state["messages"].append({"role": "assistant", "content": response_text})

                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to API: {e}")

def query_history():
    st.markdown("<style>h1 { margin-top: -50px; }</style>", unsafe_allow_html=True)
    st.title("📜 Query History")
    st.write("This is where past queries will be displayed.")

def coming_soon():
    st.markdown("<style>h1 { margin-top: -50px; }</style>", unsafe_allow_html=True)
    st.title("🚧 Coming Soon")
    st.write("New features will be added here in the future!")

if __name__ == "__main__":
    main()
