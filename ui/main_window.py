from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QLineEdit, QLabel, QCheckBox, QScrollArea, QFormLayout, QMessageBox
)
import pandas as pd
from data.fetch_data import get_stock_data
from data.filter_logic import apply_filters
import sys
import traceback


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Screener")
        self.setGeometry(100, 100, 1200, 800)
        self.layout = QVBoxLayout()

        self.metric_inputs = {}
        self.metric_checkboxes = {}

        # Define available metrics
        self.available_metrics = {
            "Market Cap": ">",
            "PE Ratio": "<",
            "EBITDA": ">",
            "Revenue Growth 1Y": ">",
            "Revenue Growth 3Y": ">",
            "EPS": ">",
            "ROE": ">",
            "Debt/Equity": "<",
            "Current Ratio": ">",
            "Dividend Yield": ">"
        }

        form_layout = QFormLayout()
        for metric, sign in self.available_metrics.items():
            hbox = QHBoxLayout()
            checkbox = QCheckBox()
            input_field = QLineEdit()
            input_field.setPlaceholderText(f"{sign} value")

            self.metric_checkboxes[metric] = checkbox
            self.metric_inputs[metric] = input_field

            hbox.addWidget(checkbox)
            hbox.addWidget(QLabel(metric))
            hbox.addWidget(input_field)
            form_layout.addRow(hbox)

        self.layout.addLayout(form_layout)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.btn = QPushButton("Run Screener")
        self.btn.clicked.connect(self.run_screener)
        self.layout.addWidget(self.btn)

        self.setLayout(self.layout)

    
    def run_screener(self):
        self.btn.setEnabled(False)
        try:
            print("Starting screener run...")
            raw_data = get_stock_data()
            print("Raw data shape:", raw_data.shape, "Columns:", raw_data.columns.tolist())
            filters = {}
            checked_metrics = []
            for metric in self.available_metrics:
                if self.metric_checkboxes[metric].isChecked():
                    checked_metrics.append(metric)
                    val = self.metric_inputs[metric].text()
                    if val.strip() == "":
                        print(f"Warning: No value entered for {metric}, skipping")
                        continue
                    try:
                        filters[metric] = float(val)
                        print(f"Added filter: {metric} = {filters[metric]}")
                    except ValueError:
                        print(f"Invalid number for {metric}: {val}, skipping")

            if checked_metrics and not filters:
                QMessageBox.warning(
                    self,
                    "Input Error",
                    "No valid filter values entered for checked metrics. Please enter numeric values."
                )
                return

            print("Running screener...")
            print("User filters:", filters)
            filtered = apply_filters(raw_data, filters)
            print("Filtered data shape:", filtered.shape)

            self.table.setRowCount(len(filtered))
            self.table.setColumnCount(len(filtered.columns))
            self.table.setHorizontalHeaderLabels(filtered.columns.tolist())

            for i, row in filtered.iterrows():
                for j, val in enumerate(row):
                    self.table.setItem(i, j, QTableWidgetItem(str(val)))

        except Exception as e:
            print("Error:", e)
            traceback.print_exc()
        finally:
            self.btn.setEnabled(True)