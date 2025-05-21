# Climate Data Visualisation Tool in Houdini

![Language](https://img.shields.io/badge/language-Python-blue)
![Platform](https://img.shields.io/badge/platform-Houdini%20on%20Linux-critical)
![API](https://img.shields.io/badge/data-Copernicus%20API-blueviolet)
![Interface](https://img.shields.io/badge/interface-Houdini%20Shelf%20Tool%20%2B%20HTML%20Map-orange)
![Tests](https://img.shields.io/badge/tests-Pytest-brightgreen)

#
## Overview
This is a Houdini shelf tool that fetches climate data from the Copernicus API (EU satalite data platform) and visualises it directly within Houdini. It retrieves terrain elevation, optical satellite imagery, and temperature data, allowing users to explore environmental changes over time. The tool features a user-friendly UI where you can select dates, pick a region on a map, and generate dynamic 3D visualisations of terrain and temperature changes.


### Documentation

For a full breakdown of modules, file structure and hierarchy, see:

https://ncca.github.io/pipeline-project-marisalieb/

#### Demo Videos: 
Included in Brightspace submission

## Installation instructions
1. Download the **ZIP** file and extract it to your chosen folder.  
2. From the extracted folder, run the installation script.

So, in your terminal run:
  ```bash
  cd ~/your/chosen/location/
  unzip ~/Downloads/climate_vis.zip
  python installHouPackage.py
  ```
 
## Usage Instructions
In Houdini:

1. Launch Houdini and click the + icon on the shelf toolbar to add a new shelf. There select Climate Visualisation from the available shelves to load the shelf.

2. Click on the tool to bring up the UI. Choose the Start Date and End Date for your visualisation (from 2016 onwards, since this is when the tool's satellite data begins).

3. Choose the data frequency: weekly or monthly.

4. Specify a folder where the area coordinate file and downloaded Copernicus data will be saved.

5. Click the Map button to open the interactive map:
    - Select an area to view in Houdini; please note, large areas might error so smaller areas of up to 50-100km are working better.
    - Pan/zoom to your area of interest. 
    - Search for locations by name.
    - Toggle between layers, so street map or satellite-textured terrain.
    - Reset your area selection.

6. Return to Houdini and click to load the terrain data. The optical satellite imagery overlays the heightfield, showing changes over time. Depending on the size of the selected area and time range, the loading of the data might take a few seconds per image.

7. Load the temperature data to view temperature changes on top of the terrain.

### How the Visualisation Works
- **Green nodes:** Nodes intended for viewing, showing the visualisation output. You can choose to view just the terrain or terrain with temperature visualisation.

- **Red nodes:** Editable nodes where the user can change parameters. 

#### Temperature Visualisation Details
- Temperature changes over the selected time period are visualised as spheres sitting on the terrain.

- Sphere size corresponds to temperature magnitude.

- The BlendAll slider on the red Blend Values node lets you scrub through temperature changes for the time period (e.g. from 0 to 4 for 4 weeks).

- Users can adjust sphere size, colour, and toggle between textured terrain (with optical satellite overlay) or untextured terrain (blank heightfield).


### Notes
For some selected areas there is not satelite data available. In this case a red fallback plane will be displayed, indicating a failed data download. In this case just return to the map and select a new area.

Changing time parameters while using the same data folder may cause caching issues. To avoid this, either:
- Use a new folder for fresh downloads, or
- Save your Houdini file and restart Houdini.

#
### Requirements:
- Linux - developed and tested on Linux only
- Houdini - tested in Houdini 20.5
- Firefox - must be installed at '/usr/bin/firefox' or adjusted in the code (in src/utils/open_map.py)

##### Note:
- Running the tool requires no additional Python packages beyond those bundled with Houdini.  
- However, to run the tests, extra development dependencies (listed in `pyproject.toml`) must be installed separately.

#

### Acknowledgements & Sources

- ChatGPT and GitHub Copilot were used to assist with debugging, exploring ideas and concepts, and documentation.

- The Copernicus documentation was used as a reference for data requests and adapted for this project.  
  Available here: https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/Process.html 

- The HTML map code was initially based on the Leaflet example from MapTiler and then modified:  
https://docs.maptiler.com/leaflet/examples/how-to-use-leaflet/ 

- The Houdini documentation was used as a refernce for deployment. Available here: 
https://www.sidefx.com/docs/houdini/ref/plugins.html 


### Tool Examples

![Screenshot](/media/image_1.png)
![Screenshot](/media/image_3.png)

### Node Graph and UI in Houdini

![Screenshot](/media/image_2.png)
