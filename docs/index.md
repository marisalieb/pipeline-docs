# Pipeline Project – Climate Visualisation

This is a Houdini shelf tool that fetches climate data from the Copernicus API (EU satalite data platform) and visualises it directly within Houdini. It retrieves terrain elevation, optical satellite imagery, and temperature data, allowing users to explore environmental changes over time. The tool features a user-friendly UI where you can select dates, pick a region on a map, and generate dynamic 3D visualisations of terrain and temperature changes.

### Quick Start

To explore the modules, use the navigation bar on the left.

### How It Works (Summary)

1. User interacts with the **UI** inside Houdini
2. The UI passes input to the **Import Data**
3. Import Data:
    - Calls **Utilities** for map and folder setup
    - Instantiates the appropriate **Data Download** classes to fetch Copernicus data
    - Passes results to **Node Setup** classes to build visual networks in Houdini
4. Final result: Interactive visualisation inside Houdini based on the selected parameters


## Project Structure

- **UI**  
  Folder containing Houdini shelf tool code and user interface logic. This is the entry point for:
    - Selecting time ranges and frequency
    - Choosing coordinates via an interactive map
    - Triggering the full import and visualisation process

- **Import Data**  
  The central controller module that connects all components. It:
    - Receives input from the UI
    - Uses utility functions (e.g. for coordinate parsing)
    - Instantiates and executes data import classes (e.g. `DEMFetcher`, `OpticalFetcher`, `ThermalFetcher`)
    - Triggers Houdini node creation via the corresponding setup classes

- **Data Download**  
  Contains a base DataFetcher class and specialised child classes for each data type:
    - `terrain.py` - downloads elevation data
    - `optical.py` - downloads satellite imagery
    - `thermal.py` - downloads climate data

- **Node Setup**  
  Contains a base node setup class and child classes for generating Houdini node graphs:
    - `terrain_nodes.py` - builds heightfield terrain
    - `optical_nodes.py` - adds texture overlays
    - `temperature_nodes.py` - adds temperature sphere visualisation
    - also contains noder helper functions

- **Utilities**  
  A set of general helper functions and tools, including:
    - Authentification on Copernicus
    - Area bounding box 
    - Date ranges
    - Calculating dimensions based on the map coordinates
    - Map interaction logic

