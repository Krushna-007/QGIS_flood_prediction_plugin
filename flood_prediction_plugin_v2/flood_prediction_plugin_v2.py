# -*- coding: utf-8 -*-
"""
/***************************************************************************
 FloodPredictionPluginV2
                                 A QGIS plugin
 Official Documentation-Based Flood Risk Prediction Plugin
                              -------------------
        begin                : 2025-08-26
        git sha              : $Format:%H$
        copyright            : (C) 2025 by Krushna Parmar
        email                : krushna.parmar@example.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

# Standard library imports
import os.path
import pickle
import math

# ML library imports with fallbacks
try:
    import lightgbm as lgb
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False
    
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

# QGIS imports - following official documentation patterns
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt, QVariant
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QFileDialog, QMessageBox, QCheckBox, QLabel, QTableWidgetItem

from qgis.core import (
    QgsProject,
    QgsPointXY,
    QgsRasterLayer,
    QgsVectorLayer,
    QgsCoordinateTransform,
    QgsCoordinateReferenceSystem,
    QgsRaster,
    QgsMessageLog,
    Qgis,
    QgsGeometry,
    QgsFeature,
    QgsField,
    QgsMarkerSymbol,
    QgsSingleSymbolRenderer,
    QgsSymbol,
    QgsWkbTypes,
    QgsRectangle,
    QgsRasterDataProvider,
    QgsApplication,
    QgsSettings
)

from qgis.gui import QgsMapToolEmitPoint
from qgis.utils import iface

# Initialize Qt resources from file resources.py
from .resources import *

# Import the dialog class
from .flood_prediction_plugin_v2_dialog import FloodPredictionPluginV2Dialog


class FloodPredictionPluginV2:
    """QGIS Plugin Implementation following official documentation patterns."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        
        # Initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        
        # Initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'FloodPredictionPluginV2_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Flood Prediction V2')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None
        
        # Plugin state variables
        self.selected_point = None
        self.model = None
        self.point_tool = None
        self.point_layer = None  # Layer to store the selected point
        self.expected_feature_count = None  # Expected number of features for the model

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('FloodPredictionPluginV2', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/flood_prediction_plugin_v2/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Flood Prediction V2'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Flood Prediction V2'),
                action)
            self.iface.removeToolBarIcon(action)

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = FloodPredictionPluginV2Dialog()
            
            # Connect dialog buttons to their functions
            self.dlg.pushButton_select_point.clicked.connect(self.select_point_on_map)
            self.dlg.pushButton_load_model.clicked.connect(self.load_model)
            self.dlg.pushButton_refresh_layers.clicked.connect(self.refresh_layers)
            self.dlg.pushButton_extract_data.clicked.connect(self.extract_data)
            self.dlg.pushButton_predict.clicked.connect(self.predict_flood)
            self.dlg.pushButton_clear_point.clicked.connect(self.clear_point)
            
            # Initialize UI
            self.refresh_layers()

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

    def select_point_on_map(self):
        """Activate point selection tool - following official documentation pattern"""
        try:
            QgsMessageLog.logMessage("Activating point selection tool", "Flood Prediction V2", Qgis.Info)
            
            # Create point tool if it doesn't exist
            if self.point_tool is None:
                self.point_tool = QgsMapToolEmitPoint(self.iface.mapCanvas())
                self.point_tool.canvasClicked.connect(self.point_selected)
            
            # Set the tool
            self.iface.mapCanvas().setMapTool(self.point_tool)
            self.dlg.label_status.setText("Click on the map to select a point...")
            
        except Exception as e:
            QgsMessageLog.logMessage(f"Error activating point tool: {str(e)}", "Flood Prediction V2", Qgis.Critical)
            QMessageBox.critical(self.dlg, "Error", f"Failed to activate point selection: {str(e)}")

    def point_selected(self, point, button):
        """Handle point selection - create visible point on map"""
        try:
            self.selected_point = point
            QgsMessageLog.logMessage(f"Point selected: {point.x()}, {point.y()}", "Flood Prediction V2", Qgis.Info)
            
            # Update coordinate display
            self.dlg.lineEdit_x_coord.setText(f"{point.x():.6f}")
            self.dlg.lineEdit_y_coord.setText(f"{point.y():.6f}")
            self.dlg.label_status.setText(f"Point selected at {point.x():.6f}, {point.y():.6f}")
            
            # Create visible point on map
            self.create_point_on_map(point)
            
            # Reset map tool
            self.iface.mapCanvas().unsetMapTool(self.point_tool)
            
        except Exception as e:
            QgsMessageLog.logMessage(f"Error handling point selection: {str(e)}", "Flood Prediction V2", Qgis.Critical)
            QMessageBox.critical(self.dlg, "Error", f"Failed to handle point selection: {str(e)}")

    def create_point_on_map(self, point):
        """Create a visible point marker on the map - following V1 pattern"""
        try:
            # Remove existing point layer if it exists
            if self.point_layer:
                QgsProject.instance().removeMapLayer(self.point_layer)
            
            # Get current map canvas CRS (like V1)
            crs = self.iface.mapCanvas().mapSettings().destinationCrs().authid()
            self.point_layer = QgsVectorLayer(f'Point?crs={crs}', 'Selected Point', 'memory')
            
            # Add attributes like V1
            provider = self.point_layer.dataProvider()
            provider.addAttributes([
                QgsField('x_coord', QVariant.Double),
                QgsField('y_coord', QVariant.Double),
                QgsField('prediction', QVariant.String),
                QgsField('probability', QVariant.Double)
            ])
            self.point_layer.updateFields()
            
            # Create point feature
            feature = QgsFeature()
            feature.setGeometry(QgsGeometry.fromPointXY(point))
            feature.setAttributes([point.x(), point.y(), 'Not predicted', 0.0])
            
            # Add feature to layer
            provider.addFeature(feature)
            
            # Style the point like V1 (red circle with black outline)
            symbol = QgsMarkerSymbol.createSimple({
                'name': 'circle',
                'color': 'red',
                'size': '6',
                'outline_color': 'black',
                'outline_width': '1'
            })
            
            renderer = QgsSingleSymbolRenderer(symbol)
            self.point_layer.setRenderer(renderer)
            
            # Add layer to project
            QgsProject.instance().addMapLayer(self.point_layer)
            
            QgsMessageLog.logMessage("Point marker created on map", "Flood Prediction V2", Qgis.Info)
            
        except Exception as e:
            QgsMessageLog.logMessage(f"Error creating point marker: {str(e)}", "Flood Prediction V2", Qgis.Warning)

    def clear_point(self):
        """Clear the selected point and remove from map"""
        try:
            # Clear selected point
            self.selected_point = None
            
            # Clear coordinate display
            self.dlg.lineEdit_x_coord.clear()
            self.dlg.lineEdit_y_coord.clear()
            
            # Remove point layer from map
            if self.point_layer:
                QgsProject.instance().removeMapLayer(self.point_layer)
                self.point_layer = None
            
            # Update status
            self.dlg.label_status.setText("Point cleared - select a new point")
            
            # Refresh canvas
            self.iface.mapCanvas().refresh()
            
            QgsMessageLog.logMessage("Point cleared", "Flood Prediction V2", Qgis.Info)
            
        except Exception as e:
            QgsMessageLog.logMessage(f"Error clearing point: {str(e)}", "Flood Prediction V2", Qgis.Critical)

    def load_model(self):
        """Load ML model with comprehensive UI updates"""
        try:
            # Open file dialog
            model_path, _ = QFileDialog.getOpenFileName(
                self.dlg,
                "Select Trained Flood Model",
                "",
                "Pickle Files (*.pkl);;All Files (*)"
            )
            
            if model_path:
                QgsMessageLog.logMessage(f"Loading model from: {model_path}", "Flood Prediction V2", Qgis.Info)
                
                # Load the model using standard pickle
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                
                # Validate loaded model immediately
                if self.model is None:
                    raise ValueError("Model loaded as None - the file may be corrupted")
                
                # Check if model has required methods
                if not hasattr(self.model, 'predict'):
                    raise AttributeError(f"Loaded model (type: {type(self.model).__name__}) does not have a predict method")
                
                if not callable(self.model.predict):
                    raise TypeError(f"Model predict attribute is not callable (type: {type(self.model.predict)})")
                
                # Test model functionality with a simple prediction
                try:
                    # Try to determine the expected number of features
                    test_features = 10  # Default test size
                    if hasattr(self.model, 'n_features_in_'):
                        test_features = self.model.n_features_in_
                    elif hasattr(self.model, 'n_features_'):
                        test_features = self.model.n_features_
                    
                    # Create test data
                    if NUMPY_AVAILABLE:
                        test_data = np.zeros((1, test_features))
                        test_prediction = self.model.predict(test_data)
                        QgsMessageLog.logMessage(f"Model test prediction successful with {test_features} features", "Flood Prediction V2", Qgis.Info)
                    else:
                        QgsMessageLog.logMessage("Skipping model test - NumPy not available", "Flood Prediction V2", Qgis.Warning)
                        
                except Exception as test_error:
                    QgsMessageLog.logMessage(f"Model test prediction failed: {str(test_error)}", "Flood Prediction V2", Qgis.Warning)
                    # Don't fail loading for test issues, just warn
                
                # Log successful validation
                QgsMessageLog.logMessage(f"Model validation passed: {type(self.model).__name__}", "Flood Prediction V2", Qgis.Info)
                
                # Update UI
                model_name = os.path.basename(model_path)
                self.dlg.lineEdit_model_path.setText(model_path)
                
                # Try to get model information
                try:
                    model_type = type(self.model).__name__
                    self.dlg.label_model_info.setText(f"Model type: {model_type}")
                    
                    # Check model dependencies after loading
                    self._check_model_dependencies(model_type)
                    
                    # Try multiple ways to get feature information
                    feature_info = ""
                    feature_count = 0
                    
                    if hasattr(self.model, 'feature_names_in_'):
                        features = list(self.model.feature_names_in_)
                        feature_count = len(features)
                        
                        # Check if features are generic (Column_0, Column_1, etc.)
                        if all(f.startswith('Column_') for f in features):
                            feature_info = f"Expected features: {feature_count} features (generic names: {', '.join(features[:3])}{'...' if len(features) > 3 else ''})"
                            feature_info += f"\n⚠️ Model trained with generic column names - ensure feature order matches training data"
                        else:
                            feature_info = f"Expected features: {', '.join(features)}"
                            
                    elif hasattr(self.model, 'feature_names_'):
                        features = list(self.model.feature_names_)
                        feature_count = len(features)
                        feature_info = f"Expected features: {', '.join(features)}"
                        
                    elif hasattr(self.model, 'booster_') and hasattr(self.model.booster_, 'feature_names'):
                        # For LightGBM models
                        features = list(self.model.booster_.feature_names)
                        feature_count = len(features)
                        feature_info = f"Expected features: {', '.join(features)}"
                        
                    elif hasattr(self.model, 'n_features_in_'):
                        feature_count = self.model.n_features_in_
                        feature_info = f"Expected features: {feature_count} features (names unknown)"
                        
                    elif hasattr(self.model, 'n_features_'):
                        feature_count = self.model.n_features_
                        feature_info = f"Expected features: {feature_count} features (names unknown)"
                        
                    else:
                        feature_info = "Expected features: Cannot determine"
                    
                    self.dlg.label_model_features.setText(feature_info)
                    
                    # Store feature count for validation
                    self.expected_feature_count = feature_count if feature_count > 0 else None
                    
                except Exception:
                    self.dlg.label_model_features.setText("Expected features: Cannot determine")
                    self.dlg.label_model_info.setText("Model info: Basic model loaded")
                
                self.dlg.label_status.setText(f"Model loaded: {model_name}")
                QgsMessageLog.logMessage("Model loaded successfully", "Flood Prediction V2", Qgis.Info)
                
        except Exception as e:
            error_msg = str(e)
            
            # Provide specific error messages for common dependency issues
            if "No module named 'lightgbm'" in error_msg:
                error_msg = "LightGBM library required but not installed.\n\nPlease install using:\npip install lightgbm\n\nOr in QGIS Python Console:\n!pip install lightgbm"
            elif "No module named 'xgboost'" in error_msg:
                error_msg = "XGBoost library required but not installed.\n\nPlease install using:\npip install xgboost\n\nOr in QGIS Python Console:\n!pip install xgboost"
            elif "No module named 'sklearn'" in error_msg:
                error_msg = "Scikit-learn library required but not installed.\n\nPlease install using:\npip install scikit-learn\n\nOr in QGIS Python Console:\n!pip install scikit-learn"
            elif "No module named 'numpy'" in error_msg:
                error_msg = "NumPy library required but not installed.\n\nPlease install using:\npip install numpy\n\nOr in QGIS Python Console:\n!pip install numpy"
            
            QgsMessageLog.logMessage(f"Error loading model: {error_msg}", "Flood Prediction V2", Qgis.Critical)
            QMessageBox.critical(self.dlg, "Model Loading Error", f"Failed to load model:\n\n{error_msg}")

    def _check_model_dependencies(self, model_type):
        """Check if required dependencies are available for the model type"""
        missing_deps = []
        warnings = []
        
        # Check for LightGBM models
        if 'LGB' in model_type.upper() or 'LIGHTGBM' in model_type.upper():
            if not LIGHTGBM_AVAILABLE:
                missing_deps.append("lightgbm")
                warnings.append("LightGBM models require the lightgbm library")
        
        # Check for XGBoost models  
        if 'XGB' in model_type.upper() or 'XGBOOST' in model_type.upper():
            if not XGBOOST_AVAILABLE:
                missing_deps.append("xgboost")
                warnings.append("XGBoost models require the xgboost library")
        
        # Check for NumPy (required by most models)
        if not NUMPY_AVAILABLE:
            missing_deps.append("numpy")
            warnings.append("Most ML models require NumPy for predictions")
        
        if missing_deps:
            dep_list = ", ".join(missing_deps)
            warning_msg = f"Missing dependencies detected: {dep_list}\n\n"
            warning_msg += "The model loaded successfully but prediction may fail.\n\n"
            warning_msg += "Install missing libraries:\n"
            for dep in missing_deps:
                warning_msg += f"• pip install {dep}\n"
            
            QgsMessageLog.logMessage(f"Missing dependencies: {dep_list}", "Flood Prediction V2", Qgis.Warning)
            QMessageBox.warning(self.dlg, "Missing Dependencies", warning_msg)

    def diagnose_model(self):
        """Diagnostic method to help troubleshoot model issues"""
        try:
            if not self.model:
                return "No model loaded"
            
            diagnosis = []
            diagnosis.append(f"Model Type: {type(self.model).__name__}")
            diagnosis.append(f"Model Object: {self.model}")
            
            # Check methods
            diagnosis.append(f"Has predict method: {hasattr(self.model, 'predict')}")
            if hasattr(self.model, 'predict'):
                diagnosis.append(f"Predict is callable: {callable(self.model.predict)}")
                diagnosis.append(f"Predict type: {type(self.model.predict)}")
            
            diagnosis.append(f"Has predict_proba method: {hasattr(self.model, 'predict_proba')}")
            
            # Check attributes
            attrs = ['n_features_in_', 'n_features_', 'feature_names_in_', 'feature_names_']
            for attr in attrs:
                if hasattr(self.model, attr):
                    value = getattr(self.model, attr)
                    diagnosis.append(f"{attr}: {value}")
            
            # Check if it's a specific model type
            model_name = type(self.model).__name__
            if 'LGB' in model_name.upper():
                diagnosis.append("Detected: LightGBM model")
            elif 'XGB' in model_name.upper():
                diagnosis.append("Detected: XGBoost model")
            elif any(x in model_name for x in ['Forest', 'SVM', 'MLP', 'Classifier', 'Regressor']):
                diagnosis.append("Detected: Scikit-learn model")
            
            return "\n".join(diagnosis)
            
        except Exception as e:
            return f"Diagnosis failed: {str(e)}"

    def refresh_layers(self):
        """Refresh the list of available layers with checkboxes"""
        try:
            QgsMessageLog.logMessage("Refreshing layer list", "Flood Prediction V2", Qgis.Info)
            
            # Clear existing checkboxes
            for checkbox in self.dlg.layer_checkboxes.values():
                checkbox.setParent(None)
            self.dlg.layer_checkboxes.clear()
            
            # Get all layers from project
            project = QgsProject.instance()
            layers = project.mapLayers().values()
            
            # Filter for raster layers
            raster_layers = [layer for layer in layers if isinstance(layer, QgsRasterLayer)]
            
            if not raster_layers:
                # Add message if no raster layers
                no_layers_label = QLabel("No raster layers found in project")
                no_layers_label.setStyleSheet("color: #666; font-style: italic;")
                self.dlg.scroll_layout.addWidget(no_layers_label)
                self.dlg.layer_checkboxes['__no_layers__'] = no_layers_label
            else:
                # Create checkboxes for each raster layer
                for layer in raster_layers:
                    layer_name = layer.name()
                    checkbox = QCheckBox(layer_name)
                    checkbox.setChecked(True)  # Check all by default
                    
                    # Add tooltip with layer info
                    tooltip = f"Layer: {layer_name}\nBands: {layer.bandCount()}\nExtent: {layer.extent()}"
                    checkbox.setToolTip(tooltip)
                    
                    self.dlg.scroll_layout.addWidget(checkbox)
                    self.dlg.layer_checkboxes[layer_name] = checkbox
            
            # Update status
            layer_count = len(raster_layers)
            self.dlg.label_status.setText(f"Found {layer_count} raster layers")
            QgsMessageLog.logMessage(f"Found {layer_count} raster layers", "Flood Prediction V2", Qgis.Info)
            
        except Exception as e:
            QgsMessageLog.logMessage(f"Error refreshing layers: {str(e)}", "Flood Prediction V2", Qgis.Critical)
            QMessageBox.critical(self.dlg, "Error", f"Failed to refresh layers: {str(e)}")

    def extract_data(self):
        """Extract raster data from selected layers with editable feature names"""
        try:
            if not self.selected_point:
                QMessageBox.warning(self.dlg, "Warning", "Please select a point first")
                return
            
            QgsMessageLog.logMessage("Starting data extraction", "Flood Prediction V2", Qgis.Info)
            
            # Get selected layers from checkboxes
            selected_layers = []
            for layer_name, checkbox in self.dlg.layer_checkboxes.items():
                if layer_name != '__no_layers__' and isinstance(checkbox, QCheckBox) and checkbox.isChecked():
                    selected_layers.append(layer_name)
            
            if not selected_layers:
                QMessageBox.warning(self.dlg, "Warning", "Please select at least one layer")
                return
            
            # Clear previous data
            self.dlg.tableWidget_data.setRowCount(0)
            
            extracted_data = {}
            successful_extractions = 0
            row = 0
            
            # Extract data from each selected layer
            for layer_name in selected_layers:
                layer = self.get_layer_by_name(layer_name)
                
                if not layer:
                    QgsMessageLog.logMessage(f"Layer not found: {layer_name}", "Flood Prediction V2", Qgis.Warning)
                    continue
                
                QgsMessageLog.logMessage(f"Processing layer: {layer_name}", "Flood Prediction V2", Qgis.Info)
                
                # Extract value using official documentation pattern
                value = self.extract_raster_value_official(layer, self.selected_point)
                
                if value is not None:
                    successful_extractions += 1
                    
                    # Create feature name suggestion
                    feature_name = self.suggest_feature_name(layer_name)
                    original_attr = layer_name
                    
                    # Add to table with 4 columns like V1
                    self.dlg.tableWidget_data.insertRow(row)
                    
                    # Column 0: Layer Name (read-only)
                    self.dlg.tableWidget_data.setItem(row, 0, self.create_readonly_item(layer_name))
                    
                    # Column 1: Original Attribute (read-only)
                    self.dlg.tableWidget_data.setItem(row, 1, self.create_readonly_item(original_attr))
                    
                    # Column 2: Feature Name (editable)
                    feature_item = self.create_table_item(feature_name)
                    self.dlg.tableWidget_data.setItem(row, 2, feature_item)
                    
                    # Column 3: Value (read-only)
                    value_item = self.create_readonly_item(f"{value:.6f}")
                    self.dlg.tableWidget_data.setItem(row, 3, value_item)
                    
                    # Store extracted data
                    extracted_data[feature_name] = value
                    
                    QgsMessageLog.logMessage(f"Extracted {layer_name}: {value}", "Flood Prediction V2", Qgis.Info)
                    row += 1
                else:
                    QgsMessageLog.logMessage(f"Failed to extract from {layer_name}", "Flood Prediction V2", Qgis.Warning)
            
            # Update status
            status_text = f"Extracted data from {successful_extractions}/{len(selected_layers)} selected layers"
            self.dlg.label_status.setText(status_text)
            QgsMessageLog.logMessage(status_text, "Flood Prediction V2", Qgis.Info)
            
            # Store extracted data for prediction
            self.extracted_data = extracted_data
            
        except Exception as e:
            QgsMessageLog.logMessage(f"Error extracting data: {str(e)}", "Flood Prediction V2", Qgis.Critical)
            QMessageBox.critical(self.dlg, "Error", f"Failed to extract data: {str(e)}")

    def get_layer_by_name(self, name):
        """Get layer by name from project"""
        project = QgsProject.instance()
        layers = project.mapLayers().values()
        for layer in layers:
            if layer.name() == name:
                return layer
        return None

    def suggest_feature_name(self, layer_name):
        """Suggest a feature name based on layer name (like V1)"""
        # Clean the name
        clean_name = layer_name.lower().replace(' ', '_').replace('-', '_')
        
        # Common mappings for flood modeling features
        # Updated to match user's actual training feature names
        mappings = {
            'dem': 'dem1',
            'elevation': 'dem1',
            'slope': 'slope1', 
            'aspect': 'aspect1',
            'twi': 'twi1',
            'spi': 'spi1',
            'ndvi': 'ndvi1',
            'flow': 'flow_accumulation1',
            'accumulation': 'flow_accumulation1',
            'weight': 'weights',
            'weights': 'weights',
            # Fallback mappings
            'curvature': 'curvature',
            'drainage': 'drainage_density',
            'distance': 'distance_to_water',
            'soil': 'soil_type',
            'geology': 'geology',
            'land': 'landuse',
            'cover': 'landcover'
        }
        
        # Try to find a mapping
        for key, value in mappings.items():
            if key in clean_name:
                return value
        
        # Return cleaned original name if no mapping found
        return clean_name

    def extract_raster_value_official(self, raster_layer, point):
        """
        Extract raster value using OFFICIAL QGIS documentation pattern
        
        Based on: https://api.qgis.org/api/classQgsRasterDataProvider.html
        Pattern: value, success = provider.sample(point, band)
        """
        try:
            if not raster_layer or not raster_layer.isValid():
                QgsMessageLog.logMessage("Invalid raster layer", "Flood Prediction V2", Qgis.Warning)
                return None
            
            # Get data provider
            provider = raster_layer.dataProvider()
            if not provider or not provider.isValid():
                QgsMessageLog.logMessage("Invalid raster data provider", "Flood Prediction V2", Qgis.Warning)
                return None
            
            # Transform point to layer CRS if needed
            canvas_crs = self.iface.mapCanvas().mapSettings().destinationCrs()
            layer_crs = raster_layer.crs()
            
            if canvas_crs != layer_crs:
                transform = QgsCoordinateTransform(canvas_crs, layer_crs, QgsProject.instance())
                transformed_point = transform.transform(point)
                QgsMessageLog.logMessage(f"Transformed point from {canvas_crs.authid()} to {layer_crs.authid()}", "Flood Prediction V2", Qgis.Info)
            else:
                transformed_point = point
            
            # OFFICIAL DOCUMENTATION PATTERN: Use sample() method
            # Returns tuple (value, success) as documented
            band_number = 1  # Sample from band 1 (1-based index)
            
            QgsMessageLog.logMessage(f"Sampling at point: {transformed_point.x()}, {transformed_point.y()}", "Flood Prediction V2", Qgis.Info)
            
            # This is the EXACT pattern from official QGIS documentation
            value, success = provider.sample(transformed_point, band_number)
            
            QgsMessageLog.logMessage(f"Sample result: value={value}, success={success}", "Flood Prediction V2", Qgis.Info)
            
            if success:
                # Check for NaN values as recommended in documentation
                if not math.isnan(value):
                    return float(value)
                else:
                    QgsMessageLog.logMessage("Sampled value is NaN", "Flood Prediction V2", Qgis.Warning)
                    return None
            else:
                QgsMessageLog.logMessage("Sampling failed - point outside extent or invalid band", "Flood Prediction V2", Qgis.Warning)
                return None
                
        except Exception as e:
            QgsMessageLog.logMessage(f"Exception in extract_raster_value_official: {str(e)}", "Flood Prediction V2", Qgis.Critical)
            return None

    def create_table_item(self, text):
        """Helper to create editable table widget item"""
        return QTableWidgetItem(str(text))

    def create_readonly_item(self, text):
        """Helper to create read-only table widget item"""
        item = QTableWidgetItem(str(text))
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        return item

    def predict_flood(self):
        """Make flood prediction using data from editable table"""
        try:
            if not self.model:
                QMessageBox.warning(self.dlg, "Warning", "Please load a model first")
                return
            
            # Read data from table (using editable feature names)
            features = []
            feature_names = []
            
            for row in range(self.dlg.tableWidget_data.rowCount()):
                # Column 2 contains the editable feature name
                feature_name_item = self.dlg.tableWidget_data.item(row, 2)
                # Column 3 contains the value
                value_item = self.dlg.tableWidget_data.item(row, 3)
                
                if feature_name_item and value_item:
                    feature_name = feature_name_item.text()
                    try:
                        value = float(value_item.text())
                        features.append(value)
                        feature_names.append(feature_name)
                    except ValueError:
                        QgsMessageLog.logMessage(f"Invalid value in table: {value_item.text()}", "Flood Prediction V2", Qgis.Warning)
                        continue
            
            if not features:
                QMessageBox.warning(self.dlg, "Warning", "No valid data found in table")
                return
            
            # Validate feature count if known
            if self.expected_feature_count and len(features) != self.expected_feature_count:
                warning_msg = f"""Feature count mismatch:
                
Expected: {self.expected_feature_count} features
Provided: {len(features)} features

Your model was trained with {self.expected_feature_count} features but you're providing {len(features)}.

Feature mapping suggestion:
Model expects: Column_0, Column_1, Column_2, ..., Column_{self.expected_feature_count-1}
Your features: {', '.join(feature_names)}

Please ensure you have exactly {self.expected_feature_count} features in the correct order."""
                
                QMessageBox.warning(self.dlg, "Feature Count Mismatch", warning_msg)
                QgsMessageLog.logMessage(f"Feature count mismatch: expected {self.expected_feature_count}, got {len(features)}", "Flood Prediction V2", Qgis.Warning)
                # Don't return - allow user to proceed if they want to try anyway
            
            QgsMessageLog.logMessage(f"Making prediction with {len(features)} features", "Flood Prediction V2", Qgis.Info)
            QgsMessageLog.logMessage(f"Feature names: {feature_names}", "Flood Prediction V2", Qgis.Info)
            QgsMessageLog.logMessage(f"Feature values: {features}", "Flood Prediction V2", Qgis.Info)
            
            # Validate model before prediction
            if not self.model:
                raise ValueError("Model is None - please reload the model")
            
            # Check if model has predict method
            if not hasattr(self.model, 'predict'):
                raise AttributeError(f"Model of type {type(self.model).__name__} does not have a predict method")
            
            if not callable(self.model.predict):
                raise TypeError(f"Model predict attribute is not callable: {type(self.model.predict)}")
            
            # Make prediction using model
            # Reshape for sklearn models that expect 2D input
            if not NUMPY_AVAILABLE:
                raise ImportError("NumPy is required for predictions but not installed")
            
            features_array = np.array(features).reshape(1, -1)
            QgsMessageLog.logMessage(f"Features array shape: {features_array.shape}", "Flood Prediction V2", Qgis.Info)
            QgsMessageLog.logMessage(f"Model type: {type(self.model).__name__}", "Flood Prediction V2", Qgis.Info)
            
            # Attempt prediction with detailed error handling
            try:
                # Special handling for LightGBM models
                model_type = type(self.model).__name__
                if 'LGB' in model_type.upper() or 'LIGHTGBM' in model_type.upper():
                    QgsMessageLog.logMessage("Using LightGBM-specific prediction method", "Flood Prediction V2", Qgis.Info)
                    
                    # Check LightGBM specific attributes
                    if hasattr(self.model, 'booster_') and self.model.booster_ is not None:
                        QgsMessageLog.logMessage(f"LightGBM booster available: {type(self.model.booster_)}", "Flood Prediction V2", Qgis.Info)
                    else:
                        QgsMessageLog.logMessage("LightGBM booster not available or None", "Flood Prediction V2", Qgis.Warning)
                    
                    # Try multiple LightGBM prediction approaches
                    try:
                        # Method 1: Standard sklearn interface
                        prediction = self.model.predict(features_array)
                        QgsMessageLog.logMessage("LightGBM prediction successful with standard method", "Flood Prediction V2", Qgis.Info)
                    except Exception as lgb_error1:
                        QgsMessageLog.logMessage(f"LightGBM standard method failed: {str(lgb_error1)}", "Flood Prediction V2", Qgis.Warning)
                        try:
                            # Method 2: With explicit parameters
                            prediction = self.model.predict(features_array, num_iteration=None)
                            QgsMessageLog.logMessage("LightGBM prediction successful with explicit parameters", "Flood Prediction V2", Qgis.Info)
                        except Exception as lgb_error2:
                            QgsMessageLog.logMessage(f"LightGBM explicit parameters failed: {str(lgb_error2)}", "Flood Prediction V2", Qgis.Warning)
                            try:
                                # Method 3: Direct booster prediction (if available)
                                if hasattr(self.model, 'booster_') and self.model.booster_ is not None:
                                    prediction = self.model.booster_.predict(features_array)
                                    QgsMessageLog.logMessage("LightGBM prediction successful with booster method", "Flood Prediction V2", Qgis.Info)
                                else:
                                    raise Exception("No valid LightGBM prediction method available")
                            except Exception as lgb_error3:
                                QgsMessageLog.logMessage(f"All LightGBM methods failed: {str(lgb_error3)}", "Flood Prediction V2", Qgis.Critical)
                                raise lgb_error1  # Raise the original error
                else:
                    # Standard prediction for other models
                    prediction = self.model.predict(features_array)
                
                QgsMessageLog.logMessage(f"Raw prediction result: {prediction}, type: {type(prediction)}", "Flood Prediction V2", Qgis.Info)
                
            except Exception as pred_error:
                QgsMessageLog.logMessage(f"Model prediction failed: {str(pred_error)}", "Flood Prediction V2", Qgis.Critical)
                
                # Enhanced error information for LightGBM
                if 'LGB' in type(self.model).__name__.upper():
                    lgb_info = []
                    lgb_info.append(f"LightGBM version check required")
                    if hasattr(self.model, 'booster_'):
                        lgb_info.append(f"Booster type: {type(self.model.booster_)}")
                        lgb_info.append(f"Booster is None: {self.model.booster_ is None}")
                    
                    lgb_details = "\n".join(lgb_info)
                    QgsMessageLog.logMessage(f"LightGBM diagnostic info: {lgb_details}", "Flood Prediction V2", Qgis.Info)
                
                raise RuntimeError(f"Model prediction failed: {str(pred_error)}")
            
            # Handle prediction result safely
            if hasattr(prediction, '__len__') and len(prediction) > 0:
                prediction_value = prediction[0]
            else:
                prediction_value = prediction
            
            # Get probability if available
            try:
                probabilities = self.model.predict_proba(features_array)
                if hasattr(probabilities, '__len__') and len(probabilities) > 0:
                    probs = probabilities[0]
                    if hasattr(probs, '__len__') and len(probs) > 1:
                        flood_probability = probs[1]  # Probability of flood class (class 1)
                    else:
                        flood_probability = 0.5
                else:
                    flood_probability = 0.5
            except:
                flood_probability = 0.5
            
            # Update results
            prediction_text = "Flood Risk" if prediction_value == 1 else "No Flood Risk"
            self.dlg.label_prediction_result.setText(f"Prediction: {prediction_text}")
            self.dlg.label_probability.setText(f"Flood Probability: {flood_probability:.4f}")
            
            # Create features summary for status
            features_summary = f"Used {len(features)} features: {', '.join(feature_names[:3])}{'...' if len(feature_names) > 3 else ''}"
            self.dlg.label_status.setText(f"Prediction: {prediction_text} | {features_summary}")
            
            QgsMessageLog.logMessage(f"Prediction: {prediction_text}, Probability: {flood_probability:.4f}", "Flood Prediction V2", Qgis.Info)
            
        except Exception as e:
            error_msg = str(e)
            
            # Add model diagnosis to error for troubleshooting
            diagnosis = self.diagnose_model()
            detailed_error = f"Prediction Error: {error_msg}\n\nModel Diagnosis:\n{diagnosis}"
            
            QgsMessageLog.logMessage(f"Error making prediction: {error_msg}", "Flood Prediction V2", Qgis.Critical)
            QgsMessageLog.logMessage(f"Model diagnosis: {diagnosis}", "Flood Prediction V2", Qgis.Info)
            
            # Show user-friendly error with option to see details
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle("Prediction Error")
            msg_box.setText(f"Failed to make prediction: {error_msg}")
            msg_box.setDetailedText(detailed_error)
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
