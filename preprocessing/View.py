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

import os
import webbrowser

import numpy as np
import pandas as pd
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QIcon, QDoubleValidator
from PySide6.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QListWidgetItem, QCheckBox

from preprocessing.MainWindow import Ui_MainWindow
from preprocessing.ViewModels import SimplePandasModel, MPLKernelHeatmap, LogMessageDialog, ShowAboutDialog


class View(QMainWindow, Ui_MainWindow):
    WELCOME_TAB = 0
    RAW_DATA_TAB = 1
    RESULT_TAB = 2
    PRECOMP_DATA_TAB = 3
    DIALOG_ICON_SIZE = (64, 64)

    def __init__(self, controller, parent=None):
        super(View, self).__init__(parent)
        self.controller = controller
        self.controller.view = self
        self.setupUi(self)
        self.controller.app.setWindowIcon(QIcon(":/logo/logo.png"))
        self.show()

        self.version = self.controller.app.version
        self.start_version_label.setText(f"version {self.version}")
        self.default_window_title = "web-rMKL preprocessing"
        self.window_title_text = self.default_window_title
        self.setWindowTitle(self.window_title_text)

        self.kernel_ok_icon = QIcon(":/icons/kernel_ok.png")
        self.kernel_warn_icon = QIcon(":/icons/kernel_warn.png")
        self.kernel_icons = {
            "rbf": QIcon(":/kernels/rbf_black.png"),
            "poly": QIcon(":/kernels/poly_black.png"),
            "linear": QIcon(":/kernels/linear_black.png")
        }
        self.critical_icon = QIcon(":/icons/critical.png")
        self.warning_icon = QIcon(":/icons/warning.png")
        self.question_icon = QIcon(":/icons/question.png")

        self.mode = -1  # 0: raw, 1: precomp

        self.setup_view_basics()
        self.setup_interactions()

    @property
    def current_input_item(self) -> str | None:
        if self.controller.has_input_data:
            return self.input_listwidget.currentItem().text()
        return None

    @property
    def current_processed_item(self) -> str | None:
        if self.controller.has_computed_data:
            return self.processed_kernels_listwidget.currentItem().text()
        return None

    @current_processed_item.setter
    def current_processed_item(self, value):
        idx = self.processed_kernels_listwidget.findItems(
            value, Qt.MatchExactly)[0]
        if idx:
            self.processed_kernels_listwidget.setCurrentItem(idx)

    @property
    def current_precomp_item(self) -> str | None:
        if not self.controller.has_precomp_data:
            return None
        return self.precomp_kernels_listwidget.currentItem().text()

    def setup_view_basics(self):
        """Set up the basic view elements and hide unnecessary elements."""
        self.progress_frame.hide()
        self.enable_kernel_settings(False)
        self.kernel_settings_sync_check.setChecked(
            self.controller.sync_kernel_settings)

        self.kernel_gamma_edit.setValidator(QDoubleValidator(decimals=5))
        self.kernel_degree_edit.setValidator(QDoubleValidator(decimals=5))
        self.kernel_cost_edit.setValidator(QDoubleValidator(decimals=5))

        self.input_table_model = SimplePandasModel(
            self.input_tableview, pd.DataFrame())
        self.input_tableview.setModel(self.input_table_model)

        self.processed_vis_heatmap = MPLKernelHeatmap(self.controller)
        self.processed_vis_layout.insertWidget(
            1, self.processed_vis_heatmap.figure)
        self.processed_vis_layout.setStretch(1, 1)

        self.precomp_heatmap = MPLKernelHeatmap(self.controller)
        self.precomp_vis_layout.insertWidget(1, self.precomp_heatmap.figure)
        self.precomp_vis_layout.setStretch(1, 1)

        self.enable_precomp_export(False, False)
        self.precomp_is_sym_icon.hide()
        self.precomp_not_sym_icon.hide()
        self.precomp_is_psd_icon.hide()
        self.precomp_not_psd_icon.hide()
        self.reg_kernel_matrix_btn.hide()

        self.show_start_tab()

    def setup_interactions(self):
        """Connect signals to view and controller methods."""
        self.start_precomp_btn.clicked.connect(self.select_precomp_mode)
        self.start_raw_btn.clicked.connect(self.select_raw_mode)
        self.start_help_button.clicked.connect(
            lambda: webbrowser.open(self.controller.app.repo_url))

        self.action_compute_current.triggered.connect(
            self.controller.compute_current_kernel_matrix)
        self.action_compute_all.triggered.connect(
            self.controller.compute_all_kernel_matrices)
        self.action_export_index.triggered.connect(
            lambda: self.controller.export_id_file(output_file=None))
        self.action_help.triggered.connect(
            lambda: webbrowser.open(self.controller.app.repo_url))
        self.action_go_to_rmkl.triggered.connect(
            lambda: webbrowser.open(self.controller.app.web_rmkl_url))

        self.raw_add_data_btn.clicked.connect(self.controller.import_raw_data)
        self.precomp_add_data_btn.clicked.connect(
            self.controller.import_precomp_data)

        self.kernel_button_group.buttonClicked.connect(
            self.controller.select_kernel_method)
        self.kernel_gamma_edit.editingFinished.connect(
            self.controller.select_kernel_params)
        self.kernel_degree_edit.editingFinished.connect(
            self.controller.select_kernel_params)
        self.kernel_cost_edit.editingFinished.connect(
            self.controller.select_kernel_params)
        self.kernel_settings_sync_check.stateChanged.connect(
            self.sync_kernel_settings)
        self.apply_settings_globally_btn.clicked.connect(
            self.controller.apply_kernel_settings_globally)
        self.apply_default_gamma_btn.clicked.connect(
            lambda: self.controller.select_default_param("gamma"))
        self.apply_default_degree_btn.clicked.connect(
            lambda: self.controller.select_default_param("degree"))
        self.apply_default_cost_btn.clicked.connect(
            lambda: self.controller.select_default_param("coef0"))
        self.input_listwidget.itemSelectionChanged.connect(
            self.controller.select_raw_input_data)

        self.compute_all_btn.clicked.connect(
            self.controller.compute_all_kernel_matrices)
        self.compute_current_btn.clicked.connect(
            self.controller.compute_current_kernel_matrix)

        self.processed_kernels_listwidget.itemSelectionChanged.connect(
            self.controller.select_processed_kernel_matrix)

        self.precomp_kernels_listwidget.itemSelectionChanged.connect(
            self.controller.select_precomp_kernel_matrix)
        self.reg_kernel_matrix_btn.clicked.connect(
            self.controller.regularize_current_precomp_kernel)
        self.precomp_export_all_btn.clicked.connect(
            self.action_export_all.trigger)
        self.precomp_export_current_btn.clicked.connect(
            self.action_export_current.trigger)
        self.precomp_export_ids_btn.clicked.connect(
            self.action_export_index.trigger)
        self.processed_export_all_btn.clicked.connect(
            self.action_export_all.trigger)
        self.processed_export_current_btn.clicked.connect(
            self.action_export_current.trigger)
        self.processed_export_ids_btn.clicked.connect(
            self.action_export_index.trigger)

        self.tab_widget.currentChanged.connect(self.switch_tab)
        self.action_about.triggered.connect(self.show_about)

    def show_start_tab(self):
        """Show the start tab and hide all other tabs (hide the tab bar)."""
        self.tab_widget.setCurrentIndex(self.WELCOME_TAB)
        self.tab_widget.tabBar().hide()

    def select_precomp_mode(self):
        """Switch to the precomputed kernel matrix mode.
        Only the precomputed data tab is visible, the others are hidden. The tab bar is hidden.
        Menu actions are connected to the controller methods for precomputed data.
        """
        self.tab_widget.setCurrentIndex(self.PRECOMP_DATA_TAB)
        self.tab_widget.tabBar().hide()
        self.tab_widget.setTabVisible(self.WELCOME_TAB, False)
        self.tab_widget.setTabVisible(self.RAW_DATA_TAB, False)
        self.tab_widget.setTabVisible(self.RESULT_TAB, False)
        self.action_add_data.triggered.connect(
            self.controller.import_precomp_data)
        self.action_export_all.setText("Export all valid matrices")
        self.action_export_all.triggered.connect(
            lambda: self.controller.export_precomp_kernel(name=None))
        self.action_export_current.triggered.connect(
            lambda: self.controller.export_precomp_kernel(name=self.current_precomp_item))

    def select_raw_mode(self):
        """Switch to the raw data mode.
        The tab bar is shown and the raw data and result tabs are visible.
        Menu actions are connected to the controller methods for raw data.
        """
        self.tab_widget.setTabVisible(self.WELCOME_TAB, False)
        self.tab_widget.setTabVisible(self.PRECOMP_DATA_TAB, False)
        self.tab_widget.setCurrentIndex(1)
        self.tab_widget.tabBar().show()
        self.action_add_data.triggered.connect(self.controller.import_raw_data)
        self.action_export_all.triggered.connect(
            lambda: self.controller.export_all_kernel_matrices(csv=False))
        self.action_export_all_csv.triggered.connect(
            lambda: self.controller.export_all_kernel_matrices(csv=True))
        self.action_export_current.triggered.connect(
            self.controller.export_current_kernel_matrix)

    def enable_modification(self, value: bool):
        """Enable or disable the modification of kernel settings, computation and export.

        :param value: True to enable, False to disable
        """
        self.tab_widget.setEnabled(value)

    def enable_kernel_settings(self, enable: bool):
        """Enable or disable the kernel settings.

        :param enable: True to enable, False to disable
        """
        self.kernel_settings_frame.setEnabled(enable)

    def sync_kernel_settings(self, sync: bool, update_cbox: bool = False):
        """Synchronize the kernel settings between all data types.

        :param sync: True to synchronize, False to disable synchronization
        :param update_cbox: True to update the checkbox state, False to only update the controller
        """
        if update_cbox:
            self.kernel_settings_sync_check.setChecked(sync)
            return
        self.controller.sync_kernel_settings = sync
        if sync:
            self.controller.apply_kernel_settings_globally()
        self.apply_settings_globally_btn.setEnabled(not sync)

    def update_kernel_function_preview(self, method: str):
        """Update the kernel function preview icon to show the correct formula.

        :param method: The kernel method to show the formula for
        """
        if method in self.kernel_icons:
            self.kernel_function_preview.setIcon(self.kernel_icons[method])

    def update_param_visibility(self, kernel_method: str):
        """Update the visibility of the kernel parameters and settings based on the selected kernel method.

        :param kernel_method: The selected kernel method
        """
        if kernel_method == "rbf":
            self.kernel_params_layout.setEnabled(True)
            self.kernel_gamma_edit.setEnabled(True)
            self.kernel_gamma_label.setEnabled(True)
            self.default_gamma_value.setEnabled(True)
            self.apply_default_gamma_btn.setEnabled(True)
            self.kernel_degree_edit.setEnabled(False)
            self.kernel_degree_label.setEnabled(False)
            self.default_degree_value.setEnabled(False)
            self.apply_default_degree_btn.setEnabled(False)
            self.kernel_cost_edit.setEnabled(False)
            self.kernel_cost_label.setEnabled(False)
            self.default_cost_value.setEnabled(False)
            self.apply_default_cost_btn.setEnabled(False)
        elif kernel_method == "poly":
            self.kernel_params_layout.setEnabled(True)
            self.kernel_gamma_edit.setEnabled(True)
            self.kernel_gamma_label.setEnabled(True)
            self.default_gamma_value.setEnabled(True)
            self.apply_default_gamma_btn.setEnabled(True)
            self.kernel_degree_edit.setEnabled(True)
            self.kernel_degree_label.setEnabled(True)
            self.default_degree_value.setEnabled(True)
            self.apply_default_degree_btn.setEnabled(True)
            self.kernel_cost_edit.setEnabled(True)
            self.kernel_cost_label.setEnabled(True)
            self.default_cost_value.setEnabled(True)
            self.apply_default_cost_btn.setEnabled(True)
        else:  # linear kernel
            self.kernel_params_layout.setEnabled(False)

    def update_kernel_settings_view(self, selected_params: dict, method: str | None = None):
        """Update the kernel settings view with the selected parameters and method.

        :param selected_params: Dictionary containing selected kernel parameters
        :param method: The selected kernel method
        """
        selected_params = format_param_values(selected_params)
        self.kernel_gamma_edit.blockSignals(True)
        self.kernel_gamma_edit.setText(str(selected_params["gamma"]))
        self.kernel_gamma_edit.blockSignals(False)
        self.kernel_degree_edit.blockSignals(True)
        self.kernel_degree_edit.setText(str(selected_params["degree"]))
        self.kernel_degree_edit.blockSignals(False)
        self.kernel_cost_edit.blockSignals(True)
        self.kernel_cost_edit.setText(str(selected_params["coef0"]))
        self.kernel_cost_edit.blockSignals(False)
        if method is not None:
            self.kernel_button_group.blockSignals(True)
            if method == "linear":
                self.linear_kernel_btn.setChecked(True)
            elif method == "rbf":
                self.rbf_kernel_btn.setChecked(True)
            elif method == "poly":
                self.poly_kernel_btn.setChecked(True)
            self.kernel_button_group.blockSignals(False)
            self.update_param_visibility(method)
            self.update_kernel_function_preview(method)

    def update_default_kernel_settings_view(self, default_params: dict):
        """Update the default kernel settings view with the default parameters.

        :param default_params: Dictionary containing default kernel parameters
        """
        default_params = format_param_values(default_params)
        self.default_gamma_value.setText(str(default_params["gamma"]))
        self.default_degree_value.setText(str(default_params["degree"]))
        self.default_cost_value.setText(str(default_params["coef0"]))

    def update_input_preview(self, table_data: pd.DataFrame, sample_count: int, feature_count: int):
        """Update the input data preview table and displayed counts with the current data.

        :param table_data: The input data as a pandas DataFrame
        :param sample_count: The number of samples in the input data
        :param feature_count: The number of features in the input data
        """
        self.input_feature_count.setText(str(feature_count))
        self.input_sample_count.setText(str(sample_count))
        self.input_table_model.set_data(table_data)

    def get_current_kernel_params(self) -> dict[str, float | int | None]:
        """Retrieve the currently selected kernel parameters from the view.

        :return: Dictionary containing the selected kernel parameters
                 Keys: "gamma", "degree", "coef0"
                 Values: float or int or None
        """
        gamma = self.kernel_gamma_edit.text()
        gamma = float(gamma) if gamma != "None" and len(gamma) > 0 else None
        degree = self.kernel_degree_edit.text()
        degree = int(degree) if degree != "None" and len(degree) > 0 else None
        cost = self.kernel_cost_edit.text()
        cost = float(cost) if cost != "None" and len(cost) > 0 else None
        return {"gamma": gamma, "degree": degree, "coef0": cost}

    def get_current_kernel_method(self) -> str:
        """Retrieve the currently selected kernel method from the view."""
        if self.rbf_kernel_btn.isChecked():
            return "rbf"
        elif self.poly_kernel_btn.isChecked():
            return "poly"
        else:
            return "linear"

    def switch_tab(self):
        """Update the view based on the currently selected tab.
        Enable or disable menu actions based on the current tab and data availability.
        """
        is_input = self.tab_widget.currentIndex() == self.RAW_DATA_TAB
        can_compute = self.controller.has_input_data and is_input
        can_export = self.controller.has_computed_data and not is_input
        is_precomp = self.tab_widget.currentIndex() == self.PRECOMP_DATA_TAB
        self.action_add_data.setEnabled(is_input or is_precomp)
        self.action_compute_all.setEnabled(can_compute)
        self.action_compute_current.setEnabled(can_compute)
        self.action_export_all.setEnabled(can_export)
        self.action_export_current.setEnabled(can_export)
        self.action_export_all_csv.setEnabled(can_export)
        self.action_export_index.setEnabled(can_export)

    def go_to_results_tab(self):
        self.tab_widget.setCurrentIndex(self.RESULT_TAB)

    def add_data(self, data_names: list[str], raw: bool):
        """Add entries to the input or precomputed list widget and update settings.

        :param data_names: List of data names to add
        :param raw: True if the data is raw input data, False otherwise
        """
        if raw:
            widget = self.input_listwidget
        else:
            widget = self.precomp_kernels_listwidget
        for d in data_names:
            # prevent adding duplicates by replacing existing items
            if self.remove_from_list_widget(d, widget, complete=False):
                widget.addItem(QListWidgetItem(d))
            # remove old processed data if it exists
            if raw:
                self.remove_from_list_widget(d,
                                             self.processed_kernels_listwidget,
                                             complete=True)
        if widget.currentIndex().row() == 0:  # force update first item info
            if raw:
                self.controller.select_raw_input_data(
                    widget.item(0).text())
            else:
                self.controller.select_precomp_kernel_matrix(
                    widget.item(0).text())
        else:
            widget.setCurrentRow(0)
        if not raw:
            return
        self.enable_kernel_settings(True)
        self.switch_tab()
        # clear old processed data
        if self.processed_kernels_listwidget.count() == 0:
            self.clear_processed_output()
            return
        # select the first processed item and prevent showing old data
        if self.processed_kernels_listwidget.currentIndex().row() == 0:
            self.controller.select_processed_kernel_matrix()
        else:
            self.processed_kernels_listwidget.setCurrentRow(0)
        self.update_input_icons()

    def remove_from_list_widget(self, name: str, widget, complete: bool) -> bool:
        """Remove the item with the given name from the list widget.
        Item will only be removed if it exists in the list widget.

        :param name: Name of the item to remove
        :param widget: The list widget to search in
        :param complete: True to remove all items with the given name, False to remove only duplicates
        :return: True if all items were removed, False if only one item was found and complete is False
        """
        itm = widget.findItems(name, Qt.MatchExactly)
        if itm is not None and len(itm) >= 1:
            if not complete and len(itm) == 1:
                return False
            widget.blockSignals(True)
            for i in itm:
                tmp_row = widget.indexFromItem(i).row()
                trash_itm = widget.takeItem(tmp_row)
                del trash_itm
        widget.blockSignals(False)
        return True

    def update_input_icons(self):
        """Update the icons of the input list widget items based on the current data state.
        Three different states are displayed:
        - Kernel computation was successful
        - Kernel settings were changed but not recomputed
        - No computation was carried out so far
        """
        raw_computed_names, other_names = self.controller.computed_data_names
        changed_names = self.controller.changed_data_names
        computed_names = [
            name for name in raw_computed_names if name not in changed_names]
        for name in computed_names:
            item = self.input_listwidget.findItems(name, Qt.MatchExactly)[0]
            item.setIcon(self.kernel_ok_icon)
        for name in changed_names:
            item = self.input_listwidget.findItems(name, Qt.MatchExactly)[0]
            item.setIcon(self.kernel_warn_icon)
        for name in other_names:
            items = self.input_listwidget.findItems(name, Qt.MatchExactly)
            for item in items:
                item.setData(Qt.DecorationRole, None)

    def update_processed_data(self, names: list):
        """Update the processed kernels list widget with the given list of kernel names.

        :param names: List of kernel names to display
        """
        if len(names) == 0:
            self.clear_processed_output()
            return
        self.processed_kernels_listwidget.clear()
        self.processed_kernels_listwidget.addItems(names)
        self.processed_kernels_listwidget.setCurrentRow(0)

    def updated_processed_visualization(self, params: dict, kernel_matrix: np.ndarray):
        """Update the processed kernel visualization with the given kernel matrix and parameters.

        :param params: Dictionary containing the kernel parameters
        :param kernel_matrix: The kernel matrix to visualize
        """
        if params is None:
            return
        method = params.pop("method")
        method_replace = {"rbf": "RBF",
                          "poly": "Polynomial", "linear": "Linear"}
        method = method_replace[method]
        params = format_param_values(params)
        self.proc_method_value.setText(method)
        self.proc_method_value.setEnabled(True)
        self.proc_method_label.setEnabled(True)
        self.proc_gamma_value.setText(str(params["gamma"]))
        self.proc_degree_value.setText(str(params["degree"]))
        self.proc_cost_value.setText(str(params["coef0"]))
        if method == "RBF":
            self.proc_gamma_value.setEnabled(True)
            self.proc_gamma_label.setEnabled(True)
            self.proc_degree_value.setEnabled(False)
            self.proc_degree_label.setEnabled(False)
            self.proc_cost_value.setEnabled(False)
            self.proc_cost_label.setEnabled(False)
        elif method == "Polynomial":
            self.proc_gamma_value.setEnabled(True)
            self.proc_gamma_label.setEnabled(True)
            self.proc_degree_value.setEnabled(True)
            self.proc_degree_label.setEnabled(True)
            self.proc_cost_value.setEnabled(True)
            self.proc_cost_label.setEnabled(True)
        else:  # linear
            self.proc_gamma_value.setEnabled(False)
            self.proc_gamma_label.setEnabled(False)
            self.proc_degree_value.setEnabled(False)
            self.proc_degree_label.setEnabled(False)
            self.proc_cost_value.setEnabled(False)
            self.proc_cost_label.setEnabled(False)

        self.processed_vis_heatmap.draw_figure(kernel_matrix)

    def clear_processed_output(self):
        """Clear the processed kernel output view."""
        self.proc_method_value.setText("")
        self.proc_gamma_value.setText("")
        self.proc_degree_value.setText("")
        self.proc_cost_value.setText("")
        self.proc_gamma_value.setEnabled(False)
        self.proc_gamma_label.setEnabled(False)
        self.proc_degree_value.setEnabled(False)
        self.proc_degree_label.setEnabled(False)
        self.proc_cost_value.setEnabled(False)
        self.proc_cost_label.setEnabled(False)
        self.processed_vis_heatmap.clear()
        self.processed_kernels_listwidget.blockSignals(True)
        self.processed_kernels_listwidget.clear()
        self.processed_kernels_listwidget.blockSignals(False)
        self.update_input_icons()

    def update_precomp_vis(self, km: np.ndarray, shape: tuple, sym: bool, psd: bool, any_valid: bool, allow_reg: bool):
        """Update the precomputed kernel visualization with the given kernel matrix and properties.

        :param km: The kernel matrix to visualize
        :param shape: Tuple containing the shape of the kernel matrix
        :param sym: True if the kernel matrix is symmetric, False otherwise
        :param psd: True if the kernel matrix is positive semi-definite, False otherwise
        :param any_valid: True if any of the kernel matrices is valid, False otherwise
        :param allow_reg: True if the kernel matrix can be regularized, False otherwise
        """
        self.precomp_heatmap.draw_figure(km)
        self.precomp_shape_value.setText(f"{shape[0]} x {shape[1]}")
        self.precomp_is_sym_icon.setVisible(sym)
        self.precomp_not_sym_icon.setVisible(not sym)
        self.precomp_is_psd_icon.setVisible(psd)
        self.precomp_not_psd_icon.setVisible(not psd)
        self.enable_precomp_export(sym and psd, any_valid)
        self.reg_kernel_matrix_btn.setVisible(allow_reg)

    def update_precomp_icons(self):
        """Update the icons of the precomputed list widget items based on the current data state.
        Three different states are displayed:
        - Precomputed kernel matrix is but is allowed to be regularized
        - Precomputed kernel matrix is invalid
        - Precomputed kernel matrix is valid
        """
        invalid_names, fixable_names = self.controller.invalid_and_fixable_precomp_data
        valid_names = self.controller.valid_precomp_data
        for name in fixable_names:
            item = self.precomp_kernels_listwidget.findItems(
                name, Qt.MatchExactly)[0]
            item.setData(Qt.DecorationRole, self.kernel_warn_icon)
        for name in invalid_names:
            item = self.precomp_kernels_listwidget.findItems(
                name, Qt.MatchExactly)[0]
            item.setData(Qt.DecorationRole, self.critical_icon)
        for name in valid_names:
            item = self.precomp_kernels_listwidget.findItems(
                name, Qt.MatchExactly)[0]
            item.setData(Qt.DecorationRole, self.kernel_ok_icon)

    def enable_precomp_export(self, current: bool, all_kernels: bool):
        """Enable or disable the precomputed kernel export buttons based on data availability.

        :param current: True to enable the export current button, False to disable
        :param all_kernels: True to enable the export all button, False to disable
        """
        self.precomp_export_all_btn.setEnabled(all_kernels)
        self.precomp_export_ids_btn.setEnabled(all_kernels)
        self.precomp_export_current_btn.setEnabled(current)
        self.action_export_all.setEnabled(all_kernels)
        self.action_export_current.setEnabled(current)
        self.action_export_index.setEnabled(all_kernels)

    def update_progress_bar(self, progress: int):
        """Update the progress bar with the given progress value."""
        self.progress_bar.setValue(progress)

    def update_progress_message(self, message: str, finished: bool = False):
        """Update the progress message label with the given message or hide it after completion.

        :param message: The message to display
        :param finished: True to hide the progress frame after 2 seconds, False to keep it visible
        """
        self.progress_label.setText(message)
        if finished:
            timer = QTimer()
            timer.singleShot(2000, self.hide_progress)

    def hide_progress(self):
        """Hide the progress frame and clear the progress bar and message."""
        self.progress_frame.hide()
        self.clear_progress()

    def show_progress(self):
        """Show the progress frame and clear the progress bar and message."""
        self.clear_progress()
        self.progress_frame.show()

    def clear_progress(self):
        """Clear the progress bar and message."""
        self.progress_label.setText("")
        self.progress_bar.setValue(0)

    def ask_overwrite_data_type(self, name: str) -> bool:
        """Ask the user if they want to overwrite the existing data with the same name.

        :param name: The name of the data to overwrite
        :return: True if the user wants to overwrite, False otherwise
        """
        if isinstance(name, list):
            name = ", ".join(name)
        box = QMessageBox(self)
        box.setIconPixmap(self.question_icon.pixmap(*self.DIALOG_ICON_SIZE))
        box.setWindowTitle("Overwrite data?")
        box.setText("Overwrite data?")
        box.setInformativeText(f"Input data {name} already exists. Reimporting files with the same names will "
                               f"overwrite the existing data.\n"
                               f"Do you want to continue and overwrite the existing data?")
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        return box.exec() == QMessageBox.Yes

    def ask_kernel_correction(self, name: str) -> bool:
        """Ask the user if they want to correct the kernel matrix with the given name.

        :param name: The name of the kernel matrix to correct
        :return: True if the user wants to correct the kernel matrix, False otherwise
        """
        box = QMessageBox(self)
        box.setIconPixmap(self.question_icon.pixmap(*self.DIALOG_ICON_SIZE))
        box.setWindowTitle("Kernel matrix is not positive semi-definite")
        box.setText("Kernel matrix is not positive semi-definite!")
        box.setInformativeText(f"Kernel matrix '{name}' is not positive semi-definite. This could be caused by "
                               f"numerical instabilities. The automatic regularization method attempts to modify this "
                               f"matrix by adding a small constant to its diagonal, in order to make it positive "
                               f"semi-definite.\nNote: This may result in a diagonal dominant matrix which may affect "
                               f"the performance of downstream methods.\n"
                               f"Do you want to continue and apply the automatic regularization?")
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        return box.exec() == QMessageBox.Yes

    def get_input_type(self) -> tuple[list[str], bool] | tuple[None, None]:
        """Ask the user if they want to import indexed data and return the selected input files and choice.

        :return: Tuple containing the selected input files and the choice to import indexed data
        """
        box = QMessageBox(self)
        box.setIconPixmap(self.question_icon.pixmap(*self.DIALOG_ICON_SIZE))
        box.setStandardButtons(
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        box.setWindowTitle("Choose appropriate input files")
        box.setText("Do you want to import indexed data?")
        box.setInformativeText(
            "Input files must be in CSV format (comma-separated) with samples as rows and features as "
            "columns.\nDo your files contain an index column with sample names and a header row with feature names?")
        reply = box.exec_()
        if reply == QMessageBox.Cancel:
            return None, None
        else:
            files = self.get_input_files()
        return files, reply == QMessageBox.Yes

    def warn_input_type(self, indexed: bool) -> list | None:
        """Warn the user that the selected input files are not compatible and ask for new files.

        :param indexed: True if the existing data is indexed, False if it is numerical
        :return: List of selected input files or None if the user cancels
        """
        box = QMessageBox(self)
        box.setWindowTitle("Please choose compatible files")
        box.setText("Please choose compatible files")
        if indexed:
            box.setInformativeText("Existing data contains a sample index. Please choose appropriate input files that "
                                   "contain the same samples.")
        else:
            box.setInformativeText("Existing data is numerical. Please choose appropriate files that contain the same "
                                   "samples in the same order!")
        box.setIconPixmap(self.warning_icon.pixmap(*self.DIALOG_ICON_SIZE))
        box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        reply = box.exec()
        if reply == QMessageBox.Ok:
            files = self.get_input_files()
            return files
        else:
            return None

    def get_input_files(self) -> list[str]:
        """Open a file dialog to select input files and return the selected files.

        :return: List of selected input files
        """
        files, _ = QFileDialog.getOpenFileNames(self, "Select input files",
                                                self.controller.current_dir, "CSV Files (*.csv *.CSV)")
        if files and len(files) > 0:
            self.controller.current_dir = os.path.dirname(files[0])
        return files

    def get_input_handling(self, unequal_sizes: bool) -> bool:
        box = QMessageBox(self)
        box.setWindowTitle("Inconsistent input files")
        box.setText("Inconsistent input files. Adjust automatically?")
        if unequal_sizes:
            box.setInformativeText("Unequal sample counts detected! If you continue, samples will be reduced and "
                                   "aligned to only include overlapping samples in the same order. Otherwise, "
                                   "the import will be cancelled. Do you want to continue?")
        else:
            box.setInformativeText("Different sample sorting detected! If you continue, samples will be aligned to "
                                   "the same order. Otherwise, the import will be cancelled. Do you want to continue?")
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        box.setIconPixmap(self.critical_icon.pixmap(*self.DIALOG_ICON_SIZE))
        return box.exec() == QMessageBox.Yes

    def get_output_file(self, default_name, id_file: bool = False, force_mat: bool = False) -> str:
        """Open a file dialog to select an output file and return the selected file.

        :param default_name: Default name for the output file
        :param id_file: True if the output file is an ID file, False otherwise
        :param force_mat: True to force the output file to be a MAT file, False to allow both MAT and CSV files
        :return: The selected output file
        """
        if id_file:
            extension = "TXT File (*.txt *.TXT)"
            default_name = f"{default_name}.txt"
        else:
            extension = "MAT File (*.mat *.MAT)" if force_mat else "MAT File (*.mat *.MAT) CSV File (*.csv *.CSV)"
            # always prefer mat files due to the requirements of web-rMKL
            default_name = f"{default_name}.mat"
        tmp_dir = os.path.join(self.controller.current_dir, default_name)

        file, _ = QFileDialog.getSaveFileName(self, "Select output file",
                                              tmp_dir, extension)
        if file:
            self.controller.current_dir = os.path.dirname(file)
        return file

    def get_output_folder(self) -> str:
        """Open a file dialog to select an output folder and return the selected folder.

        :return: The selected output folder
        """
        folder = QFileDialog.getExistingDirectory(
            self, "Select output folder", self.controller.current_dir)
        if folder:
            self.controller.current_dir = folder
        return folder

    def show_export_warning(self, no_log: bool = False) -> tuple[str | None, bool]:
        """Show a warning message box to ask the user if they want to overwrite existing files.

        :param no_log: True to hide the log file information, False to show it
        :return: Tuple containing the selected output folder and the choice to generate a sample index file
        """
        box = QMessageBox(self)
        box.setIconPixmap(self.warning_icon.pixmap(*self.DIALOG_ICON_SIZE))
        box.setWindowTitle("Overwrite existing files?")
        box.setText(
            "The export will overwrite existing files with identical names. Do you want to continue?")
        log_info = ("A log file containing an overview of all selected parameters will automatically be saved to the "
                    "selected folder.\n")
        if no_log:
            log_info = ""
        box.setInformativeText(f"{log_info}Please note: web-rMKL requires a sample index file in "
                               f"addition to the kernel matrices.")
        cbx = QCheckBox(
            "Generate a sample index file in the selected directory (named sample_ids.txt)")
        cbx.setChecked(True)
        box.setCheckBox(cbx)
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        reply = box.exec()
        if reply == QMessageBox.Yes:
            folder = self.get_output_folder()
        else:
            folder = None
        return folder, cbx.isChecked()

    def show_io_error(self, file_name: str | list, io_type: str = "import"):
        """Show an error message box for an input/output error with the given file name and type.

        :param file_name: The file name or list of file names that caused the error
        :param io_type: The type of the input/output operation (import or export)
        """
        plural = " is"
        if isinstance(file_name, list):
            if len(file_name) > 1:
                file_name = ", ".join(file_name)
                plural = "s are"
            else:
                file_name = file_name[0]
        self.show_custom_message(
            title=f"{io_type.capitalize()} error",
            info=f"Could not {io_type} {file_name}. Please check if the file{plural} valid "
                 f"and that the file{plural} not accessed by another application.",
            icon=self.critical_icon
        )

    def show_numerical_data_inconsistency_error(self):
        """Show an error message box for a numerical data inconsistency."""
        self.show_custom_message(
            title="Data import cancelled!",
            info="Import cancelled due to unequal sample counts! Please check your data and try again.",
            icon=self.critical_icon
        )

    def show_multi_export_error(self, folder: str):
        """Show an error message box for a multi-export error with the given folder name."""
        self.show_custom_message(
            title="Export error",
            info=f"Could not export kernel matrices. Please check if the export folder {folder} is valid and "
                 f"if you have write permissions.",
            icon=self.critical_icon
        )

    def show_import_error_with_log(self, log_df: pd.DataFrame):
        """Show an import error message box with the given log data frame."""
        box = LogMessageDialog("Import error - invalid input files",
                               "Invalid input files were detected. Please make sure that all file requirements are "
                               "satisfied and try again.\nThe following errors occurred during import validation:",
                               log_df)
        box.exec()

    def show_custom_message(self, title: str, info: str, icon: QIcon | None = None,
                            win_title: str | None = None):
        """Show a custom message box with the given title, information, icon and window title.

        :param title: The title of the message box
        :param info: The information to display
        :param icon: The icon to display, set to self.critical_icon if None is provided
        :param win_title: The window title of the message box
        """
        if icon is None:
            icon = self.critical_icon
        box = QMessageBox(self)
        box.setWindowTitle(win_title if win_title is not None else title)
        box.setText(title)
        box.setInformativeText(info)
        box.setIconPixmap(icon.pixmap(*self.DIALOG_ICON_SIZE))
        box.exec()

    def show_warning(self, title: str, message: str):
        """Show a warning message box with the given title and message."""
        self.show_custom_message(
            title=title, info=message, icon=self.warning_icon)

    def show_about(self):
        """Show the AboutDialog with the version and repository URL."""
        dlg = ShowAboutDialog(self.version, self.controller.app.copyright,
                              self.controller.app.repo_url)
        dlg.exec()


def format_param_values(params: dict) -> dict[str, str]:
    """Format the parameter values for display in the view.

    :param params: Parameter values (dict)
    :return:  Dictionary containing formatted parameter values
    """
    formatted_params = {}
    for key, value in params.items():
        if value is None:
            formatted_params[key] = ""
        elif isinstance(value, float):
            if 1000 > value > 0.001:
                formatted_params[key] = f"{value:.3f}"
            else:
                formatted_params[key] = f"{value:.3g}"
        else:
            formatted_params[key] = str(value)
    return formatted_params
