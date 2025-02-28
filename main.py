import streamlit as st

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

def chat_interface():
    st.title("💬 Chat Interface")
    st.write("This is where the chat UI will go.")

def query_history():
    st.title("📜 Query History")
    st.write("This is where past queries will be displayed.")

def coming_soon():
    st.title("🚧 Coming Soon")
    st.write("New features will be added here in the future!")

if __name__ == "__main__":
    main()
