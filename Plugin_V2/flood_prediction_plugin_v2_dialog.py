# -*- coding: utf-8 -*-
"""
/***************************************************************************
 FloodPredictionPluginV2Dialog
                                 A QGIS plugin
 Official Documentation-Based Flood Risk Prediction Plugin
                             -------------------
        begin                : 2025-08-26
        git sha              : $Format:%H$
        copyright            : (C) 2025 by Krushna Parmar
        email                : contact@krushnaparmar.dev
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

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTableWidget, 
    QTableWidgetItem, QHeaderView, QGroupBox, QScrollArea, QCheckBox, QLineEdit,
    QSplitter, QTextEdit, QFrame
)
from qgis.PyQt.QtCore import Qt
from qgis.PyQt import QtWidgets

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
UI_FILE = None  # We'll create the UI programmatically

class FloodPredictionPluginV2Dialog(QDialog):
    """Dialog for Flood Prediction Plugin V2 - Comprehensive UI like V1"""

    def __init__(self):
        """Constructor - create comprehensive UI like V1"""
        super(FloodPredictionPluginV2Dialog, self).__init__()
        
        # Set window properties
        self.setWindowTitle("Flood Prediction Plugin V2")
        self.setMinimumSize(800, 600)
        
        # Initialize layer checkboxes dictionary
        self.layer_checkboxes = {}
        
        # Create layout
        self.setup_ui()

    def setup_ui(self):
        """Setup comprehensive UI elements like V1"""
        self.setObjectName("FloodPredictionPluginV2Dialog")
        self.resize(800, 600)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Create splitter for main content
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left panel
        left_widget = QtWidgets.QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # Point Selection Group
        point_group = QGroupBox("Point Selection")
        point_layout = QVBoxLayout(point_group)
        
        self.pushButton_select_point = QPushButton("Select Point on Map")
        point_layout.addWidget(self.pushButton_select_point)
        
        coord_layout = QHBoxLayout()
        coord_layout.addWidget(QLabel("X:"))
        self.lineEdit_x_coord = QLineEdit()
        self.lineEdit_x_coord.setReadOnly(True)
        coord_layout.addWidget(self.lineEdit_x_coord)
        
        coord_layout.addWidget(QLabel("Y:"))
        self.lineEdit_y_coord = QLineEdit()
        self.lineEdit_y_coord.setReadOnly(True)
        coord_layout.addWidget(self.lineEdit_y_coord)
        
        point_layout.addLayout(coord_layout)
        left_layout.addWidget(point_group)
        
        # Layer Selection Group
        layer_group = QGroupBox("Layer Selection")
        layer_layout = QVBoxLayout(layer_group)
        
        layer_buttons_layout = QHBoxLayout()
        self.pushButton_refresh_layers = QPushButton("Refresh Layers")
        layer_buttons_layout.addWidget(self.pushButton_refresh_layers)
        
        self.pushButton_extract_data = QPushButton("Extract Data")
        layer_buttons_layout.addWidget(self.pushButton_extract_data)
        layer_layout.addLayout(layer_buttons_layout)
        
        layer_layout.addWidget(QLabel("Available Layers (check to select):"))
        
        # Create scrollable area for layer checkboxes
        self.scroll_area = QScrollArea()
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMaximumHeight(200)
        self.scroll_area.setMinimumHeight(100)
        layer_layout.addWidget(self.scroll_area)
        
        left_layout.addWidget(layer_group)
        
        # Model Selection Group
        model_group = QGroupBox("Model Selection")
        model_layout = QVBoxLayout(model_group)
        
        model_file_layout = QHBoxLayout()
        model_file_layout.addWidget(QLabel("Model File:"))
        self.lineEdit_model_path = QLineEdit()
        self.lineEdit_model_path.setReadOnly(True)
        model_file_layout.addWidget(self.lineEdit_model_path)
        self.pushButton_load_model = QPushButton("Browse")
        model_file_layout.addWidget(self.pushButton_load_model)
        model_layout.addLayout(model_file_layout)
        
        self.label_model_features = QLabel("Expected features: Not loaded")
        self.label_model_features.setWordWrap(True)
        model_layout.addWidget(self.label_model_features)
        
        self.label_model_info = QLabel("Model info: Not loaded")
        self.label_model_info.setWordWrap(True)
        model_layout.addWidget(self.label_model_info)
        
        left_layout.addWidget(model_group)
        
        # Prediction Group
        prediction_group = QGroupBox("Prediction")
        prediction_layout = QVBoxLayout(prediction_group)
        
        prediction_buttons_layout = QHBoxLayout()
        self.pushButton_predict = QPushButton("Make Prediction")
        self.pushButton_predict.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; }")
        prediction_buttons_layout.addWidget(self.pushButton_predict)
        
        self.pushButton_clear_point = QPushButton("Clear Point")
        prediction_buttons_layout.addWidget(self.pushButton_clear_point)
        prediction_layout.addLayout(prediction_buttons_layout)
        
        # Prediction results
        self.label_prediction_result = QLabel("Prediction: Not made")
        self.label_prediction_result.setStyleSheet("font-weight: bold;")
        prediction_layout.addWidget(self.label_prediction_result)
        
        self.label_probability = QLabel("Probability: Not calculated")
        prediction_layout.addWidget(self.label_probability)
        
        left_layout.addWidget(prediction_group)
        
        # Add left panel to splitter
        splitter.addWidget(left_widget)
        
        # Right panel - Data Table
        right_widget = QtWidgets.QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # Data group
        data_group = QGroupBox("Extracted Data")
        data_layout = QVBoxLayout(data_group)
        
        # Suggestion label
        suggestion_label = QLabel("Tip: Edit 'Feature Name' column to match your model's expected feature names")
        suggestion_label.setStyleSheet("color: #666; font-style: italic; margin: 5px;")
        data_layout.addWidget(suggestion_label)
        
        # Data table with 4 columns like V1
        self.tableWidget_data = QTableWidget()
        self.tableWidget_data.setColumnCount(4)
        self.tableWidget_data.setHorizontalHeaderLabels(["Layer", "Original Attribute", "Feature Name", "Value"])
        
        # Set column properties
        header = self.tableWidget_data.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Layer
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Original Attribute
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # Feature Name (editable)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Value
        
        data_layout.addWidget(self.tableWidget_data)
        right_layout.addWidget(data_group)
        
        # Add right panel to splitter
        splitter.addWidget(right_widget)
        
        # Set splitter proportions
        splitter.setSizes([400, 400])
        
        # Status bar
        self.label_status = QLabel("Ready - Select a point and load layers to begin")
        self.label_status.setStyleSheet("background-color: #f0f0f0; padding: 8px; border: 1px solid #ccc; margin-top: 10px;")
        main_layout.addWidget(self.label_status)
