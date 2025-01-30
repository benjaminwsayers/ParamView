# app.py
import streamlit as st
from controllers import DesignExplorerApp

def main():
    # Set the page configuration
    st.set_page_config(
        page_title="Param View",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    # Initialize and run the app
    app = DesignExplorerApp()
    app.run()

if __name__ == "__main__":
    main()
