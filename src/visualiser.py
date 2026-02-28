import streamlit as st
import plotly.express as px
from PIL import Image
import io
from streamlit_modal import Modal  # Importing the Modal component
import pandas as pd
import base64

class Visualiser:
    def __init__(self, data):
        self.data = data
        self.modal = Modal(title="", key="details_modal")  # Initialize the modal

    def plot_parallel_coordinates(self):
        if self.data is None:
            st.warning("No data available for visualization.")
            return

        selected_params = st.multiselect(
            "Select Parameters",
            self.data.columns,
            default=self.data.columns[:5]
        )
        if not selected_params:
            st.warning("Please select at least one parameter.")
            return

        fig = px.parallel_coordinates(self.data, dimensions=selected_params)
        st.plotly_chart(fig)


    def plot_design_grid(self, num_columns=6):
        hover_css = """
        <style>
        /* Design card styling */
        .design-card {
            position: relative;
            width: 100%;
            cursor: pointer;
            border: 3px solid #ddd;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            transition: transform 0.2s, box-shadow 0.2s;
            background-color: #fff; /* Ensure background for tooltip contrast */
            margin-bottom: 20px; /* Space below each card */
            z-index: 1; /* Default z-index */
        }

        /* Bring the card to front on hover */
        .design-card:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            z-index: 1000; /* Higher z-index to appear above other cards */
        }

        /* Image styling */
        .design-image {
            width: 100%;
            height: auto;
            display: block;
            border-bottom: 1px solid #ddd; /* Separates image from content */
            border-radius: 8px;
        }

        /* Tooltip styling */
        .tooltip {
            display: none;
            position: absolute;
            top: 10px; /* Slight offset from top */
            left: 0%; /* Position the tooltip to the right of the card */
            width: 250px; /* Adjust width as needed */
            background: rgba(0, 0, 0, 0.95); /* Dark background for contrast */
            color: #f1f1f1;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            z-index: 2000; /* Very high z-index to appear above all other elements */
            white-space: normal; /* Allow text to wrap */
            overflow-y: auto; /* Enable vertical scrolling if content is too long */
            max-height: 350px; /* Maximum height before scrolling */
            pointer-events: none; /* Prevent tooltip from capturing mouse events */
        }

        /* Show tooltip on hover */
        .design-card:hover .tooltip {
            display: block;
        }


        /* Optional: Arrow for the tooltip */
        .tooltip::before {
            content: "";
            position: absolute;
            top: 15px;
            left: -10px;
            border-width: 5px;
            border-style: solid;
            border-color: transparent rgba(0, 0, 0, 0.95) transparent transparent;
        }

        /* Scrollbar Styling for Tooltip */
        .tooltip::-webkit-scrollbar {
            width: 6px;
        }

        .tooltip::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 3px;
        }

        .tooltip::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.3);
            border-radius: 3px;
        }

        /* Ensure parent containers allow overflow */
        /* Override Streamlit's internal overflow restrictions */
        .block-container, .stApp {
            overflow: visible !important;
        }

        /* Optional: Adjust tooltip position for smaller screens */
        @media (max-width: 768px) {
            .tooltip {
                left: 50%;
                top: 105%;
                transform: translateX(-50%);
            }
            .tooltip::before {
                top: -5px;
                left: 50%;
                transform: translateX(-50%) rotate(90deg);
                border-color: transparent transparent rgba(0, 0, 0, 0.95) transparent;
            }
        }
        </style>
        """

        # Inject the optimized CSS into the Streamlit app
        st.markdown(hover_css, unsafe_allow_html=True)

        # Calculate the number of rows needed
        num_rows = (len(self.data) + num_columns - 1) // num_columns

        # Iterate over each row
        for row_idx in range(num_rows):
            cols = st.columns(num_columns)
            for col_idx in range(num_columns):
                # Calculate the index of the current design solution
                design_idx = row_idx * num_columns + col_idx
                if design_idx < len(self.data):
                    design = self.data.iloc[design_idx]

                    with cols[col_idx]:
                        # Prepare parameters to display in tooltip
                        params = [
                            f"{col.replace('out:', '')}: {design[col]}"
                            for col in self.data.columns
                            if col.startswith("out:") and col != 'image_path'
                        ]
                        params_html = "<br>".join(params)

                        # Get the image as bytes and encode for embedding
                        image_bytes = self.get_image_placeholder(design_idx)
                        encoded = base64.b64encode(image_bytes).decode()
                        image_html = f"data:image/png;base64,{encoded}"

                        # HTML structure for the design card with tooltip pop-out
                        design_card_html = f"""
                        <div class="design-card">
                            <img src="{image_html}" alt="Design {design_idx + 1}" class="design-image">
                            <div class="tooltip">
                                <div class="design-overlay-content">
                                    <H5>Design {design_idx}</H5>   
                                    <strong>Parameters:</strong><br>
                                    {params_html}
                                </div>
                            </div>
                        </div>
                        """

                        # Render the design card
                        st.markdown(design_card_html, unsafe_allow_html=True)

                        with st.container():
                            col1, col2 = st.columns([1, 1])
                            with col1:
                                # "View Details" button with unique key
                                if st.button("🔍", key=f"view_{design_idx}", use_container_width=True, help=f"View Design {design_idx} Information"):
                                    # Set the selected design in session state
                                    st.session_state.selected_design = design.to_dict()
                                    # Open the modal
                                    self.modal.open()
                            with col2:
                                # "Select Design" button with unique key
                                if st.button("⭐", key=f"select_{design_idx}", use_container_width=True, help=f"Add Design {design_idx} to Selection"):
                                    # Set the selected design in session state
                                    st.session_state.selected_design = design.to_dict()
                                    # Open the modal
                                    self.modal.open()
                            

        # Render the modal outside the loop to prevent multiple modals
        if 'selected_design' in st.session_state:
            with self.modal.container():
                st.header(f"Details for Design {st.session_state.selected_design.get('design_id', 'N/A')}")
                for key, value in st.session_state.selected_design.items():
                    if key != 'image_path':
                        st.write(f"**{key.replace('out:', '')}:** {value}")

                # Optionally, display the image again
                if 'image_path' in st.session_state.selected_design and pd.notnull(st.session_state.selected_design['image_path']):
                    try:
                        image_path = st.session_state.selected_design['image_path']
                        st.image(image_path, caption="Design Image", use_container_width=True)
                    except Exception as e:
                        st.error(f"Error loading image: {e}")

                # Button to close the modal with a unique key
                if st.button("Close", key="close_modal"):
                    self.modal.close()
                    del st.session_state.selected_design


    def get_image_placeholder(self, design_idx):
        """Return the design image as PNG bytes.

        Loads from image_path column if present and readable; otherwise
        returns a deterministic coloured placeholder.
        """
        if 'image_path' in self.data.columns:
            image_path = self.data.iloc[design_idx]['image_path']
            if pd.notnull(image_path):
                try:
                    img = Image.open(image_path)
                    buf = io.BytesIO()
                    img.save(buf, format='PNG')
                    return buf.getvalue()
                except Exception:
                    pass  # fall through to placeholder

        img = Image.new(
            'RGB',
            (200, 200),
            color=(design_idx * 30 % 255, design_idx * 60 % 255, design_idx * 90 % 255),
        )
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        return buf.getvalue()
