# Installation Guide - Flood Prediction Plugin

## Quick Installation

### Prerequisites
- QGIS 3.0 or higher (recommended: QGIS 3.40+ LTR)
- That's it! Uses Python's built-in libraries + QGIS

### Version 1.1.0 Update
- ✅ **FIXED**: "'bool' object is not iterable" raster extraction error
- Enhanced support for normalized raster data (0-1 range values)
- Multiple robust extraction methods for different QGIS versions
- Comprehensive debug logging for troubleshooting

### Step 1: Download Plugin
Download the `flood_prediction_plugin` folder to your computer.

### Step 2: Install Plugin
Copy the entire `flood_prediction_plugin` folder to your QGIS plugins directory:

**Windows:**
```
%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\
```

**Linux:**
```
~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/
```

**Mac:**
```
~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/
```

### Step 3: Enable Plugin
1. Restart QGIS
2. Go to `Plugins` → `Manage and Install Plugins`
3. Click on `Installed` tab
4. Find "Flood Prediction Plugin" and check the checkbox to enable it

### Step 4: Verify Installation
- You should see a flood prediction icon in the toolbar
- The plugin menu should be available under `Plugins` → `Flood Prediction Plugin`

## Using the Plugin

### 1. Prepare Your Data
Make sure you have your ML model file:
- `best_flood_model.pkl` (or any .pkl model file)
- **That's all you need!** No additional files required.

### 2. Load Your GIS Layers
Load relevant raster and vector layers into QGIS:
- DEM (Digital Elevation Model)
- Slope
- Aspect  
- TWI (Topographic Wetness Index)
- SPI (Stream Power Index)
- NDVI
- Any other relevant layers

### 3. Use the Plugin
1. Click the plugin icon or go to Plugins → Flood Prediction Plugin
2. Click "Select Point on Map" and click on your area of interest
3. Select relevant layers from the list
4. Click "Extract Data" to get values at the selected point
5. Browse and load your ML model file
6. Click "Make Prediction" to get flood risk assessment

## Troubleshooting

### Plugin Not Visible
- Ensure the folder is in the correct plugins directory
- Restart QGIS completely
- Check if the plugin is enabled in Plugin Manager

### Import Errors
The plugin uses only Python's built-in libraries and QGIS modules. If you get import errors:
- Restart QGIS completely
- Check that the plugin files are correctly placed

### Model Loading Issues
- Ensure model file is .pkl format
- Verify model was created with compatible scikit-learn version
- No additional files needed - just the main .pkl file

### No Data Extracted
- Verify layers have valid data at selected point
- Check layer projections match
- Ensure point falls within layer boundaries

## Support

For issues or questions, please check the README.md file for detailed usage instructions.

## Author

Created by Krushna Parmar
