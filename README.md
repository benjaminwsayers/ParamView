# Param View

Param View is an interactive web application built with Streamlit that leverages Rhino.Compute and machine learning to optimize and visualize parametric car park designs. It allows users to input design parameters, execute Grasshopper definitions, visualize 3D models, and receive AI-assisted design recommendations to maximize parking bay efficiency.

![Param View Screenshot](screenshots/param_view_screenshot.png)

## Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)

## Features

- **Data Management:**
  - Upload and import design data from CSV and JSON files.
  - Automatic data validation and preprocessing.

- **Interactive Visualizations:**
  - Scatter plots, parallel coordinates, grid views, and design grids to explore design solutions.
  - Interactive 3D model rendering using pythreejs for detailed design inspection.

- **Grasshopper Integration:**
  - Execute Grasshopper definitions via Rhino.Compute with custom input parameters.
  - Parse and display geometry and data outputs from Rhino.Compute.

- **AI-Assisted Design Optimization:**
  - Predict optimal design parameters to maximize parking bays using trained machine learning models.
  - Implement Bayesian Optimization and Genetic Algorithms for enhanced design recommendations.

- **User-Friendly Interface:**
  - Intuitive forms and interactive elements for seamless user experience.
  - Responsive design compatible with various devices and screen sizes.

- **Extensibility:**
  - Modular codebase allowing easy integration of additional features and functionalities.
  - Caching mechanisms to optimize performance and reduce redundant computations.

## Demo

![Interactive 3D Model](screenshots/3d_model_demo.png)

Experience the Param View in action:

1. **Upload Data:** Import your existing design solutions via CSV or JSON.
2. **Explore Designs:** Use interactive plots to analyze and compare different design parameters.
3. **Generate New Designs:** Input new parameters to execute Grasshopper models and visualize 3D layouts.
4. **Optimize Designs:** Receive AI-driven recommendations to maximize parking bay efficiency.

## Installation

Follow these steps to set up and run the Param View locally.

### Prerequisites

- **Python 3.7 or higher**
- **Rhino.Compute Server:**
  - Ensure Rhino.Compute is deployed and accessible.
  - Obtain the Rhino.Compute API endpoint and API key.

### Clone the Repository

```bash
git clone https://github.com/yourusername/design-explorer.git
cd design-explorer
