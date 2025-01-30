# ui_components.py
import streamlit as st

class Sidebar:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.data_loaded = False
    
    def data_management(self, container):
        """
        Manage data-related sidebar components, including uploading data
        and performing data actions.
        """
        # === Section 1: Upload Data ===
        container.header("📥 Upload Data")
        
        uploaded_file = container.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file is not None:
            self.data_manager.source_type = 'csv'
            self.data_manager.source_path = uploaded_file
            self.data_manager.load_data()

        # === Section 2: Select Data ===
        container.header("⚙️ Select Data")

        # Check if data is loaded
        self.data_loaded = self.data_manager.data is not None

        if not self.data_loaded:
            container.warning("🔍 Please upload data to perform actions.")
        
        if self.data_loaded:
            # Create buttons for data actions
            reset_clicked = container.button(
                "🔄 Reset Selection",
                help="Reset all current selections.",
                use_container_width=True
            )
            exclude_clicked = container.button(
                "🚫 Exclude Selection",
                help="Exclude the selected items from the dataset.",
                use_container_width=True
            )
            save_clicked = container.button(
                "💾 Save Selection",
                help="Save the current selection to a file.",
                use_container_width=True
            )

            # Handle button actions
            if reset_clicked:
                #self.data_manager.reset_selection()
                container.success("Selection has been reset.")
            if exclude_clicked:
                #self.data_manager.exclude_selection()
                container.info("Selected items have been excluded.")
            if save_clicked:
                #self.data_manager.save_selection()
                container.success("Selection has been saved.")

    def data_filters(self, container):
        """
        Display range sliders for filtering numeric columns in the dataset.
        """
        # === Section: Range Sliders ===
        container.header("📊 Filter Data")

        st.slider(
            "Filter 1",
            min_value=1,
            max_value=12,
            value=1,
            step=1
        )

    def render(self):
        """
        Render the sidebar with two tabs: Data Management and Data Filters.
        """
        # Create two tabs in the sidebar
        tabs = st.sidebar.tabs(["📁 Data Management", "📊 Data Filters"])

        with tabs[0]:
            self.data_management(tabs[0])
        
        with tabs[1]:
            self.data_filters(tabs[1])




class MainDisplay:
    def __init__(self, data_manager, visualizer):
        self.data_manager = data_manager
        self.visualizer = visualizer

    def render(self):
        data = self.data_manager.get_data()
        if data is not None:
            st.title("Param View")
            
            self.visualizer.plot_parallel_coordinates()
            
            self.visualizer.plot_design_grid()

            # Display data overview
            st.write(data.head())

            # Future 3D Model Visualization
            # if st.button("Visualize 3D Model"):
            #     self.visualizer.plot_3d_model(model_data)
        else:
            st.warning("Please upload a data file to begin.")