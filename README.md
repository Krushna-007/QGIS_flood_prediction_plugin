# 🌊 QGIS Flood Prediction Plugin

<div align="center">

![Flood Prediction](https://img.shields.io/badge/QGIS-Flood%20Prediction-blue?style=for-the-badge&logo=qgis)
![Version](https://img.shields.io/badge/version-2.4.0-green?style=for-the-badge)
![License](https://img.shields.io/badge/license-GPL--2.0-orange?style=for-the-badge)

**Advanced flood risk assessment using machine learning models in QGIS**

*Combining GIS data with AI-powered predictions for enhanced flood risk analysis*

</div>

---

## 📋 Overview

The **QGIS Flood Prediction Plugin** is a comprehensive tool for flood risk assessment that combines geographic information systems (GIS) data with machine learning models. This plugin allows researchers, hydrologists, and GIS professionals to predict flood probability at specific locations using various environmental and topographical factors.

### ✨ Key Features

- 🎯 **Interactive Point Selection** - Click anywhere on the map to analyze flood risk
- 🗺️ **Multi-Layer Data Extraction** - Extract values from raster and vector layers  
- 🤖 **Machine Learning Integration** - Support for multiple ML model types (Random Forest, SVM, XGBoost, LightGBM, etc.)
- 📊 **Smart Feature Mapping** - Editable feature names with intelligent suggestions
- 🎨 **Visual Results** - Color-coded map visualization of predictions
- 📈 **Probability Analysis** - Detailed probability scores and classification results
- 🔧 **Robust Error Handling** - Comprehensive logging and error recovery

## 🚀 Plugin Versions

This repository contains two versions of the plugin, each with unique strengths:

### 🆕 **Version 2 (V2)** - *Recommended*
- **Focus**: Official QGIS API compliance and simplicity
- **Strengths**: Bulletproof raster extraction, minimal dependencies
- **Best for**: Production environments, stable workflows
- **Data extraction**: Uses official `provider.sample()` pattern
- **UI**: Clean, focused interface

### 🔧 **Version 1 (V1)** - *Feature-Rich*
- **Focus**: Advanced features and comprehensive functionality  
- **Strengths**: Enhanced UI, detailed logging, fallback methods
- **Best for**: Research, development, complex workflows
- **Data extraction**: Multiple extraction methods with comprehensive error handling
- **UI**: Advanced interface with detailed data tables and suggestions

## 📦 Installation

### Prerequisites
- **QGIS 3.0+** (recommended: QGIS 3.40+ LTR)
- **Python packages**: `numpy`, `scikit-learn` (for ML models)
- **Optional**: `xgboost`, `lightgbm` (for advanced models)

### Method 1: Manual Installation

1. **Download** the plugin folder (`Plugin_V1` or `Plugin_V2`)
2. **Copy** to your QGIS plugins directory:
   - **Windows**: `%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins`
   - **Linux**: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins`
   - **Mac**: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins`
3. **Restart** QGIS
4. **Enable** the plugin in `Plugins` → `Manage and Install Plugins`

### Method 2: From ZIP
1. Go to `Plugins` → `Manage and Install Plugins` → `Install from ZIP`
2. Select the plugin ZIP file
3. Click `Install Plugin`

## 🎯 Quick Start Guide

### 1. 📂 Prepare Your Data
Load your raster layers into QGIS:
- **DEM** (Digital Elevation Model)
- **Slope** and **Aspect** layers
- **TWI** (Topographic Wetness Index)
- **SPI** (Stream Power Index)  
- **NDVI** (Normalized Difference Vegetation Index)
- **Flow Accumulation**
- Any other relevant environmental layers

### 2. 🎯 Select Analysis Point
- Open the plugin from the toolbar or `Plugins` menu
- Click **"Select Point on Map"**
- Click anywhere on the map to choose your analysis location
- Coordinates will be automatically displayed

### 3. 🗂️ Choose Data Layers
- Click **"Refresh Layers"** to see available raster layers
- Select relevant layers using checkboxes
- Click **"Extract Data"** to extract values at the selected point

### 4. ✏️ Edit Feature Names
- Review the extracted data table
- **Double-click** feature names to edit them
- Match your model's expected feature names (e.g., `dem`, `slope`, `aspect`, `twi`, `spi`, `ndvi`)

### 5. 🤖 Load ML Model
- Click **"Browse"** in the Model Selection section
- Select your trained model file (`.pkl` format)
- Model information will be displayed automatically

### 6. 🔮 Make Predictions
- Click **"Make Prediction"** to analyze flood risk
- View results:
  - **Classification**: Flood Risk / No Flood Risk
  - **Probability**: Numerical score (0.0 - 1.0)
  - **Visualization**: Color-coded point on map

## 🔬 Supported Data Types

### Raster Layers
- Digital Elevation Model (DEM)
- Slope (degrees)
- Aspect (degrees)
- Topographic Wetness Index (TWI)
- Stream Power Index (SPI)
- Normalized Difference Vegetation Index (NDVI)
- Flow Accumulation
- Curvature, Roughness, and other terrain derivatives

### Vector Layers
- Polygons with environmental attributes
- Point measurements and observations
- Line features with flow characteristics

### Machine Learning Models
- **Scikit-learn**: RandomForest, SVM, MLP, AdaBoost
- **XGBoost**: XGBClassifier, XGBRegressor
- **LightGBM**: LGBMClassifier, LGBMRegressor
- **Custom models**: Any model with `.predict()` method

## 📊 Example Workflow

```
1. Load environmental layers (DEM, slope, TWI, etc.) → 
2. Open Flood Prediction Plugin →
3. Select point of interest on map →
4. Choose relevant layers and extract data →
5. Edit feature names to match model expectations →
6. Load trained flood prediction model (.pkl) →
7. Make prediction and view results →
8. Analyze flood risk probability and classification
```

## 🛠️ Model Requirements

Your machine learning model should be:
- **Trained** using scikit-learn or compatible libraries
- **Saved** as a `.pkl` file using `pickle` or `joblib`
- **Compatible** with standard prediction interfaces

### Example model training:
```python
import pickle
from sklearn.ensemble import RandomForestClassifier

# Train your model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Save the model
with open('flood_model.pkl', 'wb') as f:
    pickle.dump(model, f)
```

## 🔧 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Plugin not appearing | Check if enabled in Plugin Manager |
| Model loading errors | Ensure model is `.pkl` format and compatible |
| No data extracted | Verify layers have valid data at selected point |
| Prediction errors | Check feature names match model expectations |
| Missing dependencies | Install required packages: `pip install numpy scikit-learn` |

### Error Messages
- **"Please select a point first"** → Click "Select Point on Map" and choose a location
- **"Please load a model first"** → Browse and load a `.pkl` model file  
- **"No valid data found"** → Select layers and extract data first
- **"Feature count mismatch"** → Ensure extracted features match model requirements

## 📈 Version History

### Version 2.4.0 (V2) - Current
- ✅ Official QGIS API compliance
- ✅ Bulletproof raster extraction using `provider.sample()`
- ✅ Enhanced model support (LightGBM, XGBoost)
- ✅ Comprehensive error handling and logging
- ✅ Clean, focused user interface

### Version 1.5.0 (V1) - Feature-Rich
- ✅ Advanced UI with comprehensive data tables
- ✅ Multiple raster extraction fallback methods
- ✅ Detailed debugging and logging with emojis
- ✅ Editable feature name mapping
- ✅ Enhanced visualization options

## 🤝 Contributing

We welcome contributions! Please feel free to:
- 🐛 Report bugs and issues
- 💡 Suggest new features
- 🔧 Submit pull requests
- 📖 Improve documentation

## 📄 License

This project is licensed under the **GNU General Public License v2.0** - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Krushna Parmar**
- Hydrologist & GIS Developer
- Specializing in flood risk assessment and machine learning applications

## 🔗 Links

- **Repository**: [GitHub](https://github.com/Krushna-007/QGIS_flood_prediction_plugin)
- **Issues**: [Bug Reports](https://github.com/Krushna-007/QGIS_flood_prediction_plugin/issues)
- **QGIS Hub**: [Plugin Page](https://plugins.qgis.org)

---

<div align="center">

**⭐ If this plugin helps your research or work, please consider giving it a star! ⭐**

*Built with ❤️ for the QGIS and hydrology communities*

</div>
