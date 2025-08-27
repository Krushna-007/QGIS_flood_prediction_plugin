# Flood Prediction Plugin V2

## Official QGIS Documentation-Based Implementation

This is a completely rewritten version of the flood prediction plugin that follows **ONLY** official QGIS documentation patterns and best practices.

## Key Improvements in V2

### 🔥 **Bulletproof Raster Extraction**
- Uses **EXACT** official documentation pattern: `value, success = provider.sample(point, band)`
- **ZERO** possibility of boolean iteration errors
- Based on [Official QGIS API Documentation](https://api.qgis.org/api/classQgsRasterDataProvider.html)

### 🎨 **Comprehensive UI (V2.1+)**
- **Same advanced features as V1** with all the reliability of V2
- **Split panel layout** with grouped sections
- **Checkbox layer selection** with tooltips
- **Editable feature names** for model compatibility
- **Coordinate display** with X/Y fields
- **4-column data table** with smart suggestions
- **Visible point markers** on map with proper styling

### 🔧 **Modern QGIS Integration**
- **Up-to-date imports** following latest QGIS standards
- **Dynamic CRS handling** using map canvas settings
- **Proper layer management** with correct removal methods
- **Complete PyQt widget imports** for all UI components

### 🤖 **Machine Learning Support**
- **Multiple ML libraries** supported: scikit-learn, XGBoost, LightGBM
- **Automatic dependency detection** with helpful error messages
- **Smart feature extraction** from different model types
- **Graceful fallbacks** when libraries are not installed

### 📍 **Visible Point Selection**
- **Creates actual points** on the map (red markers)
- **Clear point functionality** to remove markers
- **Coordinate tracking** in UI fields
- **Professional point styling** with outline

### 📚 **Pure Documentation Compliance**
- Every line of code follows official QGIS patterns
- No custom workarounds or hacks
- Uses only documented API methods and signatures

### 🛡️ **Robust Error Handling**
- Comprehensive logging using `QgsMessageLog`
- Proper exception handling at every level
- Clear user feedback for all operations

### ✨ **Clean Architecture**
- Simple, maintainable code structure
- Clear separation of concerns
- No legacy code or deprecated patterns

## Features

### Core Functionality
1. **Interactive Point Selection**: Click on map with visible red marker creation
2. **Comprehensive Layer Management**: Checkbox selection with refresh capability  
3. **Smart Data Extraction**: Extract from selected layers with official API patterns
4. **Intelligent Feature Naming**: Auto-suggest model-compatible feature names
5. **Model Integration**: Load and use trained ML models (.pkl files)
6. **Flood Risk Prediction**: Binary classification with probability estimates

### User Interface Features
- **Split Panel Layout**: Left controls, right data table
- **Coordinate Display**: Real-time X/Y coordinate tracking
- **Layer Checkboxes**: Select specific layers with tooltips
- **Editable Data Table**: 4-column table with feature name editing
- **Model Information**: Display model type and expected features
- **Status Updates**: Real-time feedback on all operations
- **Clear/Reset**: Remove points and start fresh

## Installation

1. Copy the `flood_prediction_plugin_v2` folder to your QGIS plugins directory:
   - Windows: `%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\`
   - Linux: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
   - macOS: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`

2. Restart QGIS

3. Enable the plugin in `Plugins > Manage and Install Plugins`

## Usage

### Step 1: Load Raster Data
- Load your normalized raster layers (DEM, slope, aspect, TWI, SPI, etc.) into QGIS
- Ensure all layers are in the same CRS or properly projected

### Step 2: Select Analysis Point
- Click "Select Point on Map"
- Click anywhere on the map to choose your analysis location

### Step 3: Load ML Model
- Click "Browse Model File" 
- Select your trained flood prediction model (.pkl file)

### Step 4: Extract Data
- Click "Extract Raster Data"
- The plugin will sample all raster layers at the selected point
- View extracted values in the data table

### Step 5: Make Prediction
- Click "Make Prediction"
- View flood risk prediction and probability

## Technical Implementation

### Raster Value Extraction

```python
# OFFICIAL QGIS DOCUMENTATION PATTERN
value, success = provider.sample(transformed_point, band_number)

if success:
    if not math.isnan(value):
        return float(value)  # Valid extraction
    else:
        return None  # NaN value
else:
    return None  # Point outside extent or invalid band
```

### Error Prevention
- **No boolean iteration**: Uses tuple unpacking as documented
- **Proper CRS handling**: Transforms coordinates when needed
- **NaN checking**: Validates extracted values
- **Exception handling**: Graceful error recovery

### Logging
All operations are logged using `QgsMessageLog` for debugging:
```python
QgsMessageLog.logMessage("Operation details", "Flood Prediction V2", Qgis.Info)
```

## Supported Raster Data

The plugin works with any raster data format supported by QGIS:
- **Normalized data** (0-1 range): Perfect for flood modeling features
- **DEM data**: Elevation, slope, aspect
- **Hydrological indices**: TWI, SPI, flow accumulation
- **Vegetation indices**: NDVI, EVI
- **Any single-band raster**: Sampled from band 1

## Model Requirements

- **Format**: Pickle (.pkl) files
- **Input**: List/array of extracted raster values
- **Output**: Binary classification (0=No Flood, 1=Flood)
- **Optional**: `predict_proba()` method for probability estimates

## Comparison with V1

| Aspect | V1 | V2 |
|--------|----|----|
| API Usage | Mixed patterns | **Pure documentation** |
| Error Handling | Complex workarounds | **Simple, robust** |
| Code Quality | Legacy patterns | **Modern, clean** |
| Maintainability | Difficult | **Easy** |
| Reliability | Prone to edge cases | **Bulletproof** |

## Version Information

- **Version**: 2.4.0
- **QGIS Compatibility**: 3.0+
- **Python**: 3.6+
- **Dependencies**: NumPy, scikit-learn, XGBoost, LightGBM (automatically detected)

## Version History

### v2.4.0 - LightGBM-Specific Fixes & Feature Mapping (Latest)
- ✅ **LightGBM Prediction Fix**: Multiple prediction methods to handle 'NoneType' callable errors
- ✅ **Feature Count Validation**: Automatic validation of feature count with helpful warnings
- ✅ **Smart Feature Mapping**: Updated suggestions to match actual training feature names
- ✅ **Generic Column Detection**: Warns when models use generic column names (Column_0, etc.)
- ✅ **Enhanced LightGBM Support**: Fallback methods for booster predictions
- ✅ **Improved Error Messages**: Specific guidance for feature count mismatches

### v2.3.0 - Prediction Error Fixes & Enhanced Validation
- ✅ **Fixed 'NoneType' Errors**: Comprehensive model validation prevents prediction failures
- ✅ **Enhanced Error Handling**: Detailed error messages with diagnostic information
- ✅ **Model Testing**: Automatic model functionality testing on load
- ✅ **Smart Diagnostics**: Built-in model diagnostic tools for troubleshooting
- ✅ **Improved Logging**: Comprehensive logging for debugging and support
- ✅ **User-Friendly Errors**: Clear error dialogs with actionable information

### v2.2.0 - ML Library Support & Enhanced Dependencies
- ✅ **LightGBM Support**: Full support for LightGBM models
- ✅ **XGBoost Support**: Enhanced XGBoost model compatibility  
- ✅ **Smart Dependency Detection**: Automatic library checking with helpful errors
- ✅ **Improved Model Loading**: Better feature extraction from different model types
- ✅ **Enhanced Error Messages**: Clear installation instructions for missing libraries
- ✅ **Robust Prediction**: Safe handling of NumPy and ML library dependencies

### v2.1.0 - Enhanced UI & Features
- ✅ **Complete V1 Feature Parity**: All advanced V1 features now in V2
- ✅ **Visible Point Markers**: Red markers appear on map when points selected
- ✅ **Checkbox Layer Selection**: Choose specific layers with tooltips
- ✅ **Editable Feature Names**: Rename features for model compatibility
- ✅ **4-Column Data Table**: Layer, Original Attribute, Feature Name, Value
- ✅ **Split Panel UI**: Professional layout with grouped sections
- ✅ **Coordinate Display**: X/Y coordinate fields with real-time updates
- ✅ **Clear Point Function**: Remove markers and reset selection
- ✅ **Smart Feature Suggestions**: Auto-map layer names to model features
- ✅ **Model Information Display**: Show model type and expected features

### v2.0.0 - Official Documentation Implementation
- ✅ **Official QGIS API**: Pure documentation compliance
- ✅ **Bulletproof Extraction**: Zero boolean iteration errors
- ✅ **Clean Architecture**: Simple, maintainable code
- ✅ **Professional Logging**: Comprehensive error handling

## Troubleshooting

### Missing Dependencies Error

If you get "No module named 'lightgbm'" or similar errors:

1. **Install via QGIS Python Console**:
   ```python
   !pip install lightgbm
   !pip install xgboost  
   !pip install numpy
   ```

2. **Install via System Command Line**:
   ```bash
   pip install lightgbm xgboost numpy scikit-learn
   ```

3. **For Conda Users**:
   ```bash
   conda install -c conda-forge lightgbm xgboost numpy scikit-learn
   ```

The plugin will automatically detect which libraries are available and provide specific installation instructions when needed.

### "'NoneType' object is not callable" Error

If you encounter this prediction error, the plugin now provides automatic diagnosis:

1. **Check Error Details**: Click "Show Details" in the error dialog for comprehensive model diagnosis
2. **Model Validation**: The plugin automatically validates models on load to prevent this issue
3. **Common Causes**:
   - Corrupted model file
   - Model missing `predict()` method
   - Incompatible model format

The plugin now includes automatic model testing and validation to prevent these errors.

### Feature Count Mismatch Warnings

If you see "Feature count mismatch" warnings:

1. **Check Expected Features**: The model info shows how many features it expects
2. **Extract Correct Number**: Ensure you extract data from the exact number of layers needed
3. **Feature Order Matters**: For models with generic names (Column_0, Column_1, etc.), the order must match training
4. **Use Feature Mapping**: Edit feature names in the table to match your training data

**Example for 8-feature LightGBM model:**
- Extract from 8 layers
- Rename features to: `ndvi1`, `dem1`, `aspect1`, `flow_accumulation1`, `slope1`, `spi1`, `twi1`, `weights`
- Ensure the order matches your training data

### Model Loading Issues

- Ensure your model is saved as a `.pkl` file using `pickle.dump()`
- Check that the model was trained with compatible feature names
- Verify the model supports `.predict()` method for binary classification
- Use the built-in model diagnostics for troubleshooting
- For LightGBM models: Ensure `lightgbm` library is installed

## License

GNU General Public License v2.0

## Author

Krushna Parmar
Email: krushna.parmar@example.com

---

**This V2 implementation represents a complete rewrite following official QGIS documentation patterns, ensuring maximum reliability and maintainability for flood prediction workflows.** 🌊✅
