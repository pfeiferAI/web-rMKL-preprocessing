"""
This file is part of web-rMKL preprocessing.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

__author__ = "Nicolas Kersten"
__license__ = 'GNU General Public License v3.0'

import math
import webbrowser

import numpy as np
import pandas as pd
from PySide6.QtCore import QAbstractTableModel, QModelIndex, QUrl
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QDialog
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from mpl_toolkits.axes_grid1 import make_axes_locatable

from preprocessing.AboutDialog import Ui_Dialog as AboutDialog
from preprocessing.LogDialog import Ui_Dialog as LogDialog


class SimplePandasModel(QAbstractTableModel):

    def __init__(self, parent, data, first_num_col=0, last_num_col=None, round_digits=4, nan_value=None):
        super().__init__(parent)
        self.table = parent
        self._data = data
        self.first_num_col = first_num_col
        self.last_num_col = last_num_col
        self.round_digits = round_digits
        self.nan_value = nan_value

    def rowCount(self, parent=QModelIndex()) -> int:
        """ Override method from QAbstractTableModel

        :return: row count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return self._data.shape[0]

        return 0

    def columnCount(self, parent=QModelIndex):
        """Override method from QAbstractTableModel

        :return: column count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return self._data.shape[1]
        return 0

    def data(self, index, role=Qt.DisplayRole):
        """Override method from QAbstractTableModel"""
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            if self.first_num_col is not None:
                if isinstance(value, float) and index.column() >= self.first_num_col:
                    if self.last_num_col is None or self.last_num_col >= index.column():
                        if value == 0:
                            return "0"
                        elif abs(value) > 10 ** -self.round_digits:
                            return str(round(value, ndigits=self.round_digits))
                        elif math.isnan(value):
                            return self.nan_value
                        else:
                            return '< E-%i' % self.round_digits
            if value is None or isinstance(value, float) and math.isnan(value):
                return self.nan_value
            return str(value)
        if role == Qt.TextAlignmentRole:
            if self.first_num_col is not None:
                if self.last_num_col is None:
                    if index.column() >= self.first_num_col:
                        return Qt.AlignRight + Qt.AlignVCenter
                else:
                    if self.last_num_col >= index.column() >= self.first_num_col:
                        return Qt.AlignRight + Qt.AlignVCenter
            return Qt.AlignLeft + Qt.AlignVCenter
        return None

    def set_data(self, data: pd.DataFrame):
        """Set the pandas DataFrame to be displayed in the table
        
        :param data: pandas DataFrame to be displayed
        """
        self._data = data
        self.layoutChanged.emit()
        self.dataChanged.emit(QModelIndex(), QModelIndex())
        self.table.resizeColumnsToContents()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        """Override method from QAbstractTableModel"""
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
            if orientation == Qt.Vertical:
                return str(self._data.index[section])
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return Qt.AlignLeft + Qt.AlignVCenter
            if orientation == Qt.Vertical:
                return Qt.AlignLeft + Qt.AlignVCenter
        return None

    def clear(self):
        """Clear the table"""
        self.set_data(pd.DataFrame())


class MPLKernelHeatmap(QWidget):

    def __init__(self, controller, parent=None):
        QWidget.__init__(self, parent=parent)
        self.controller = controller
        self.figure = FigureCanvasQTAgg()
        self.data = pd.DataFrame()
        self.cmap = 'plasma'

    def draw_figure(self, data: np.ndarray | None = None):
        """Draw the figure
        
        :param data: numpy array to be drawn
        """
        if data is not None and isinstance(data, np.ndarray):
            self.data = data
        self.clear()
        if self.data.shape[0] == 0:
            return

        self.figure.ax_heat = self.figure.figure.add_subplot(111)
        heatmap = self.figure.ax_heat.imshow(self.data, aspect='equal', origin='upper', cmap=self.cmap)
        self.figure.ax_heat.set_xticklabels([])
        self.figure.ax_heat.tick_params(
            axis="x", which='both', bottom=False, top=False, labelbottom=False, labeltop=False)
        self.figure.ax_heat.set_yticklabels([])
        self.figure.ax_heat.tick_params(axis="y", labelleft=False, right=False, left=False)
        max_v = self.data.max()
        min_v = self.data.min()
        divider = make_axes_locatable(self.figure.ax_heat)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cbar = self.figure.figure.colorbar(heatmap, cax=cax, orientation="vertical",
                                           ticks=np.linspace(min_v, max_v, 5), format="%.5g")
        cbar.ax.tick_params(labelsize=8)
        cbar.set_label("Kernel Value", fontsize=10)
        self.figure.figure.tight_layout(h_pad=0, w_pad=0)
        self.figure.draw()

    def clear(self):
        """Clear the figure"""
        self.figure.figure.clear()
        self.figure.draw()


class LogMessageDialog(QDialog, LogDialog):

    def __init__(self, title, info, data):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(title)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.title_text.setText(title)
        self.info_text.setText(info)
        self.log_table.setModel(SimplePandasModel(self.log_table, data))
        self.log_table.resizeColumnsToContents()


class ShowAboutDialog(QDialog, AboutDialog):

    def __init__(self, version: str, copyright_info: str, repo_url: str):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        # setup gui and interactions
        self.version_lbl.setText(f"version {version}")
        self.copyright_lbl.setText(f"Copyright {copyright_info}")
        self.buttonBox.helpRequested.connect(lambda: webbrowser.open(repo_url))
        self.license_text.setSource(QUrl("qrc:/licenses/license_text.html"))
        self.os_text.setSource(QUrl("qrc:/licenses/opensource_package_licenses.html"))
