# Installation Guide - Flood Prediction Plugin V2

## Quick Installation

### Step 1: Locate QGIS Plugin Directory
Find your QGIS plugins directory based on your operating system:

**Windows:**
```
%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\
```
Example: `C:\Users\YourName\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`

**Linux:**
```
~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/
```

**macOS:**
```
~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/
```

### Step 2: Copy Plugin Files
1. Copy the entire `flood_prediction_plugin_v2` folder to your plugins directory
2. Ensure the folder structure looks like this:
   ```
   plugins/
   └── flood_prediction_plugin_v2/
       ├── __init__.py
       ├── metadata.txt
       ├── flood_prediction_plugin_v2.py
       ├── flood_prediction_plugin_v2_dialog.py
       ├── resources.py
       ├── icon.png
       └── README.md
   ```

### Step 3: Enable Plugin
1. **Restart QGIS** completely
2. Go to `Plugins` → `Manage and Install Plugins`
3. Click on `Installed` tab
4. Find `Flood Prediction Plugin V2`
5. Check the checkbox to enable it
6. Click `Close`

### Step 4: Verify Installation
- Look for the plugin icon in the toolbar
- Or go to `Plugins` → `Flood Prediction V2`
- The plugin dialog should open successfully

## Dependencies

### Core Requirements
- **QGIS**: Version 3.0 or higher
- **Python**: 3.6+ (included with QGIS)
- **PyQt5**: Included with QGIS

### For ML Models
If you plan to use machine learning models:
- **NumPy**: For array operations
- **scikit-learn**: For ML model support

### Installing ML Dependencies in QGIS
Open QGIS Python Console and run:
```python
import subprocess
import sys

# Install numpy
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'numpy'])

# Install scikit-learn  
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'scikit-learn'])
```

## Troubleshooting

### Plugin Not Appearing
1. **Check folder name**: Must be exactly `flood_prediction_plugin_v2`
2. **Restart QGIS**: Required after copying files
3. **Check permissions**: Ensure files are readable
4. **Check QGIS version**: Requires QGIS 3.0+

### Plugin Won't Enable
1. **Check Python Console**: Look for error messages
2. **Verify dependencies**: Install NumPy if using ML models
3. **Check file integrity**: Ensure all files copied correctly

### Common Error Messages

#### "No module named 'flood_prediction_plugin_v2'"
- **Solution**: Restart QGIS and check folder name

#### "Plugin couldn't be loaded due to an error when calling its classFactory() method"
- **Solution**: Check Python Console for detailed error
- Often caused by missing dependencies

#### "No module named 'numpy'" or "'sklearn'"
- **Solution**: Install ML dependencies as shown above

## Testing Installation

### Basic Test
1. Open plugin dialog
2. Try selecting a point on the map
3. Plugin should respond without errors

### Full Test (with data)
1. Load a raster layer in QGIS
2. Open plugin and select a point
3. Try extracting data
4. Should see values in the table

## Uninstallation

### To Remove Plugin
1. Go to `Plugins` → `Manage and Install Plugins`
2. Find `Flood Prediction Plugin V2`
3. Uncheck to disable
4. Delete the `flood_prediction_plugin_v2` folder from plugins directory
5. Restart QGIS

## Version Information

- **Plugin Version**: 2.0.0
- **QGIS Compatibility**: 3.0+
- **Documentation Compliance**: 100%
- **Last Updated**: August 2025

## Support

### For Issues
1. Check the QGIS Python Console for error messages
2. Verify all installation steps were followed
3. Ensure dependencies are installed
4. Check that raster data is properly loaded in QGIS

### Plugin Features
- ✅ Point selection on map
- ✅ Raster data extraction using official QGIS API
- ✅ ML model loading (.pkl files)
- ✅ Flood risk prediction
- ✅ Professional error handling and logging

**The V2 plugin follows official QGIS documentation patterns for maximum reliability and compatibility.** 🌊✅
