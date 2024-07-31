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
from pathlib import Path

import numpy as np
import pandas as pd
from PySide6.QtCore import QThreadPool

from preprocessing.DataType import DataType, PrecompType
from preprocessing.Workers import ComputeHandler, FileHandler
from preprocessing.utils import reduce_and_sort_data


class Controller:
    """Interface between the view and backend"""

    def __init__(self, app, view=None):
        self.app = app
        self.view = view
        self.data_types = {}
        self.precomp_types = {}
        self.sync_kernel_settings = False
        self.threadpool = QThreadPool()
        self.file_handler = FileHandler(self)
        self.compute_handler = ComputeHandler(self)
        self._current_dir = str(Path.home())
        self.import_error = False
        self.sample_names = None
        self.files_indexed = None

    @property
    def current_dir(self) -> str:
        return self._current_dir

    @current_dir.setter
    def current_dir(self, value: str):
        """Set the current directory for file dialogs"""
        if value is not None and os.path.isdir(value):
            self._current_dir = value

    @property
    def has_input_data(self) -> bool:
        return len(self.data_types) > 0

    @property
    def has_computed_data(self) -> bool:
        if len(self.data_types) == 0:
            return False
        else:
            return any([dt.kernel_matrix_computed for dt in self.data_types.values()])

    @property
    def has_precomp_data(self) -> bool:
        return len(self.precomp_types) > 0

    @property
    def symmetric_precomp_data(self) -> list[str]:
        """Return a list of names of symmetric precomputed kernel matrices"""
        return [name for name, pt in self.precomp_types.items() if pt.symmetric]

    @property
    def valid_precomp_data(self) -> list[str]:
        """Return a list of names of valid precomputed kernel matrices"""
        return [name for name, pt in self.precomp_types.items() if pt.valid]

    @property
    def invalid_and_fixable_precomp_data(self) -> tuple[list[str], list[str]]:
        """Return a tuple of lists of names of invalid and fixable precomputed kernel matrices"""
        invalid_data = []
        fixable_data = []
        for name, pt in self.precomp_types.items():
            if not pt.valid:
                if pt.regularization_possible:
                    fixable_data.append(name)
                else:
                    invalid_data.append(name)
        return invalid_data, fixable_data

    @property
    def computed_data_names(self) -> tuple[list, list]:
        computed_data = []
        other_data = []
        for name, dt in self.data_types.items():
            if dt.kernel_matrix_computed:
                computed_data.append(name)
            else:
                other_data.append(name)
        return computed_data, other_data

    @property
    def changed_data_names(self) -> list:
        return [name for name, dt in self.data_types.items() if dt.computation_parameters_changed]

    def import_precomp_data(self):
        """Import precomputed kernel matrices"""
        input_files = self.view.get_input_files()
        if not input_files:
            return
        tmp_names = [os.path.splitext(os.path.basename(f))[0]
                     for f in input_files]
        dup_names = [name for name in tmp_names if name in self.data_types]
        if len(dup_names) > 0:
            overwrite = self.view.ask_overwrite_data_type(dup_names)
        else:
            overwrite = False
        if not overwrite:
            input_files = [
                f for f in input_files if os.path.splitext(
                    os.path.basename(f))[0] not in dup_names]
        self.file_handler.load_kernels(input_files, overwrite_names=dup_names)

    def update_after_precomp_import(self, *args):
        """Update the view after importing precomputed kernel matrices"""
        if not args[0]:
            self.view.update_progress_message(
                "Error while importing data", finished=True)
            return
        # values are dicts with "data", "symmetric", "psd" entries
        data_dict = args[0][0]
        overwrite_names = args[0][1]
        for name in overwrite_names:  # remove existing data that should be overwritten
            self.precomp_types.pop(name)

        if len(self.precomp_types) == 0:
            self.sample_names = None

        remaining_names = [name for name in data_dict]
        # check if any matrix is symmetric
        symmetric_matrices = [
            name for name in data_dict if data_dict[name]["symmetric"]]
        if len(symmetric_matrices) == 0:
            self.view.show_warning("No symmetric kernel matrices found",
                                   "None of the selected kernel matrices are symmetric. Data will be imported and "
                                   "visualized, but cannot be exported or used for web-rMKL.")

        # check if all matrices have the same shape
        if len(data_dict) == 1:
            equal_shape = True
        else:
            equal_shape = len(
                set([data_dict[name]["data"].shape[0] for name in data_dict])) == 1
        if self.has_precomp_data:
            current_shape = list(
                self.precomp_types.values())[0].kernel_shape[0]
            if equal_shape:
                all_shapes_equal = current_shape == list(
                    data_dict.values())[0]["data"].shape[0]
            else:
                matching_shapes = [
                    name for name in data_dict if data_dict[name]["data"].shape[0] == current_shape]
                if len(matching_shapes) == 0:
                    all_shapes_equal = False
                else:
                    self.view.show_warning("Kernel shape mismatch!",
                                           f"Not all selected kernel matrices match the shape of the existing data. "
                                           f"Only the following matrices will be imported:\n"
                                           f"{', '.join(matching_shapes)}")
                    remaining_names = matching_shapes
                    all_shapes_equal = True
            if not all_shapes_equal:
                remaining_names = []
                self.view.show_warning("Kernel shape mismatch!",
                                       f"Kernel matrix import aborted: none of the imported matrices match the "
                                       f"shape of the existing data ({' x '.join(
                                           current_shape)}). All kernel "
                                       f"matrices must have the same shape. Please check the input data and try "
                                       f"again.")
        else:
            if not equal_shape:
                remaining_names = []
                self.view.show_warning("Kernel shape mismatch!",
                                       f"Kernel matrix import aborted: the selected kernel matrices do not have "
                                       f"the same shape. All kernel matrices must have the same shape. Please "
                                       f"check the input data and try again.")

        if len(remaining_names) == 0:
            self.view.update_progress_message("Kernel matrix import aborted: no valid kernel matrices found",
                                              finished=True)
            return

        for name in remaining_names:
            self.precomp_types[name] = PrecompType(name, data_dict[name]["data"], data_dict[name]["symmetric"],
                                                   data_dict[name]["psd"])
        self.view.add_data(remaining_names, raw=False)
        self.sample_names = [
            f"sample_{i + 1}"
            for i in range(list(self.precomp_types.values())[0].kernel_shape[0])]
        self.view.precomp_kernels_listwidget.setCurrentRow(0)
        self.select_precomp_kernel_matrix()
        self.view.update_progress_message(
            "Kernel matrices imported successfully", finished=True)
        self.view.update_precomp_icons()
        self.view.enable_modification(True)

    def import_raw_data(self):
        """Import raw data"""
        if self.files_indexed is None:
            input_files, indexed = self.view.get_input_type()
        else:
            indexed = self.files_indexed
            input_files = self.view.warn_input_type(self.files_indexed)
        if not input_files:
            return
        tmp_names = [os.path.splitext(os.path.basename(f))[0]
                     for f in input_files]
        dup_names = [name for name in tmp_names if name in self.data_types]
        if len(dup_names) > 0:
            overwrite = self.view.ask_overwrite_data_type(dup_names)
        else:
            overwrite = False
        if not overwrite:
            input_files = [
                f for f in input_files if os.path.splitext(
                    os.path.basename(f))[0] not in dup_names]
        self.import_error = False
        self.file_handler.load_files(
            input_files, indexed=indexed, overwrite_names=dup_names)

    def update_after_raw_import(self, *args):
        """Update the view after importing raw data"""
        if self.import_error or not args[0]:
            self.view.update_progress_message(
                "Error while importing data", finished=True)
            return
        data_dict = args[0][0]
        overwrite_names = args[0][1]
        indexed = args[0][2]
        if len(data_dict) == 1 and self.sample_names is None:
            tmp_sample_names = list(data_dict.values())[0].index.to_list()
            self.add_raw_data(data_dict=data_dict, indexed=indexed, overwrite_names=overwrite_names,
                              sample_names=tmp_sample_names)
            return

        sample_names = self.sample_names
        # check if all existing data should be overwritten
        if all(name in overwrite_names for name in self.data_types.keys()):
            sample_names = None

        if indexed:
            new_sample_name_list = [v.index.values for v in data_dict.values()]
            new_sample_name_max_count = max(
                [len(s) for s in new_sample_name_list])
            new_names_inter = set.intersection(
                *[set(s) for s in new_sample_name_list])
            if sample_names is not None:
                new_names_inter = set(
                    sample_names).intersection(new_names_inter)
            if len(new_names_inter) < 2:  # check for a minimum overlap of 2 samples
                self.view.update_progress_message("Error while importing data: not enough overlapping samples",
                                                  finished=True)
                self.view.show_warning("Not enough overlapping samples",
                                       "The imported data does not contain enough overlapping samples. "
                                       "At least two samples are required for kernel computation. "
                                       "Please check the input data and try again.")
                return

            if sample_names is None:  # check if all samples overlap
                equal_names = new_sample_name_max_count == len(new_names_inter)
            else:  # check if there is a 100% overlap with the existing sample names
                equal_names = len(new_names_inter) == len(sample_names)

            all_names_list = new_sample_name_list
            if sample_names is not None:
                all_names_list.insert(0, sample_names)
            equal_sorting = all(np.array_equal(
                all_names_list[0], s) for s in all_names_list[1:])

            if not (equal_names and equal_sorting):
                if self.view.get_input_handling(unequal_sizes=not equal_names):
                    self.view.update_progress_message(
                        "Aligning data for import...", finished=False)
                    new_data_dict, new_sample_names = reduce_and_sort_data(data_dict=data_dict,
                                                                           sample_names=sample_names)
                    if len(new_data_dict) == 0:
                        self.view.update_progress_message("Data import cancelled: could not align data",
                                                          finished=True)
                        return
                    self.update_existing_raw_data(new_sample_names)
                    self.add_raw_data(data_dict=new_data_dict, indexed=indexed, overwrite_names=overwrite_names,
                                      sample_names=new_sample_names)
                else:
                    self.view.update_progress_message("Data import cancelled: Cannot import inconsistent data without "
                                                      "reformatting", finished=True)
                    return
            else:
                tmp_sample_names = None if sample_names is not None else all_names_list[0]
                self.add_raw_data(data_dict=data_dict, indexed=indexed, overwrite_names=overwrite_names,
                                  sample_names=tmp_sample_names)
                return
        else:
            equal_sizes = len(set([data_dict[name].shape[0]
                                   for name in data_dict])) == 1
            if sample_names is not None:
                equal_sizes = equal_sizes and len(
                    sample_names) == data_dict[list(data_dict.keys())[0]].shape[0]
            if equal_sizes:
                if sample_names is None:
                    tmp_sample_names = list(data_dict.values())[
                        0].index.to_list()
                else:
                    tmp_sample_names = None
                self.add_raw_data(data_dict=data_dict, indexed=indexed, overwrite_names=overwrite_names,
                                  sample_names=tmp_sample_names)
            else:
                self.view.update_progress_message("Error while importing data: sample counts are not equal",
                                                  finished=True)
                self.view.show_numerical_data_inconsistency_error()
                return

    def add_raw_data(self, data_dict: dict, indexed: bool, overwrite_names: list,
                     sample_names: list | np.ndarray | None = None):
        """Add raw data to the data_types dictionary

        :param data_dict: dictionary of data to be added
        :param indexed: whether the data is indexed
        :param overwrite_names: list of names of data that should be overwritten
        :param sample_names: list of sample names
        """
        if self.sync_kernel_settings and (len(overwrite_names) > 0 or len(self.data_types) > 0):
            self.view.sync_kernel_settings(sync=False, update_cbox=True)
            self.view.show_warning("Settings sync disabled", "Settings sync was disabled to prevent unexpected "
                                                             "behavior with the newly added data.")
        data_names = []
        for name in data_dict:
            self.data_types[name] = DataType(name, data_dict[name])
            data_names.append(name)
        if self.files_indexed is None:
            self.files_indexed = indexed
        if sample_names is not None:
            self.sample_names = sample_names
        self.view.add_data(data_names, raw=True)
        self.view.update_progress_message(
            "Data imported successfully", finished=True)

    def update_existing_raw_data(self, new_sample_ids: list | np.ndarray):
        """Update existing raw data with new sample IDs and clear processed data

        :param new_sample_ids: list of new sample IDs
        """
        if len(self.data_types) == 0 or len(new_sample_ids) < 2:
            return
        clear_kernel = False
        for dt in self.data_types.values():
            clear_kernel = max(dt.reduce_data(
                sample_names=new_sample_ids), False)
        if clear_kernel:
            self.view.clear_processed_output()

    def select_raw_input_data(self, dt_name: str | None = None):
        """Select raw input data for display and update the view

        :param dt_name: name of the data type to be selected
        """
        if dt_name is not None and dt_name in self.data_types.keys():
            current_dt = self.data_types[dt_name]
        else:
            current_dt = self.data_types[self.view.current_input_item]
        sample_count, feature_count = current_dt.data_shape
        kernel_method = current_dt.selected_kernel_method
        kernel_params = current_dt.get_selected_kernel_params()
        default_kernel_params = current_dt.rot_kernel_params
        table_data = current_dt.get_preview_data()
        self.view.update_input_preview(table_data, sample_count, feature_count)
        self.view.update_kernel_settings_view(
            kernel_params, method=kernel_method)
        self.view.update_default_kernel_settings_view(default_kernel_params)

    def select_kernel_method(self, btn):
        """Select a kernel method and update the view

        :param btn: button that was clicked to select the kernel method
        """
        method = btn.text().lower()
        method = "poly" if method == "polynomial" else method
        current_dt = self.data_types[self.view.current_input_item]
        if self.sync_kernel_settings:
            for dt in self.data_types.values():
                dt.selected_kernel_method = method
        else:
            current_dt.selected_kernel_method = method
        self.view.update_param_visibility(method)
        self.view.update_kernel_settings_view(
            current_dt.get_selected_kernel_params())
        self.view.update_default_kernel_settings_view(
            current_dt.rot_kernel_params)
        self.view.update_kernel_function_preview(method)
        self.view.update_input_icons()

    def select_kernel_params(self):
        """Get the selected kernel parameters and update the view"""
        current_params = self.view.get_current_kernel_params()
        current_method = self.view.get_current_kernel_method()
        if self.sync_kernel_settings:
            for dt in self.data_types.values():
                dt.set_selected_kernel_params(
                    current_params, kernel_method=current_method)
        else:
            current_dt = self.data_types[self.view.current_input_item]
            current_dt.set_selected_kernel_params(
                current_params, kernel_method=current_method)
        self.view.update_kernel_settings_view(current_params)
        self.view.update_input_icons()

    def select_default_param(self, param_name: str):
        """Set the selected kernel parameter to its default value and update the view

        :param param_name: name of the parameter to be set to default
        """
        current_dt = self.data_types[self.view.current_input_item]
        if self.sync_kernel_settings:
            for dt in self.data_types.values():
                dt.set_param_to_default(param_name)
        else:
            current_dt.set_param_to_default(param_name)
        self.view.update_kernel_settings_view(
            current_dt.get_selected_kernel_params())
        self.view.update_input_icons()

    def apply_kernel_settings_globally(self):
        """Apply the current kernel settings to all data types"""
        current_dt = self.data_types[self.view.current_input_item]
        current_params = current_dt.get_selected_kernel_params()
        current_method = current_dt.selected_kernel_method
        for dt in self.data_types.values():
            if dt != current_dt:
                dt.set_selected_kernel_params(
                    current_params, kernel_method=current_method)
        self.view.update_input_icons()

    def select_processed_kernel_matrix(self):
        """Select a processed kernel matrix for display and update the view"""
        current_dt = self.data_types[self.view.current_processed_item]
        self.view.updated_processed_visualization(
            current_dt.current_computation_parameters, current_dt.kernel_matrix)

    def select_precomp_kernel_matrix(self, pt_name: str | None = None):
        """Select a precomputed kernel matrix by the given name and update the view"""
        if pt_name is not None and pt_name in self.precomp_types.keys():
            current_pt = self.precomp_types[pt_name]
        else:
            current_pt = self.precomp_types[self.view.current_precomp_item]
        self.view.update_precomp_vis(km=current_pt.kernel_matrix,
                                     shape=current_pt.kernel_shape,
                                     sym=current_pt.sym,
                                     psd=current_pt.psd, any_valid=len(
                self.valid_precomp_data) > 0,
                                     allow_reg=current_pt.regularization_possible)

    def select_processed_by_name(self, name: str):
        """Select a processed kernel matrix by the given name and update the view"""
        self.view.current_processed_item = name

    def compute_all_kernel_matrices(self):
        self.compute_handler.compute_kernels(list(self.data_types.values()))

    def compute_current_kernel_matrix(self):
        current_dt = self.data_types[self.view.current_input_item]
        self.compute_handler.compute_kernels([current_dt])

    def update_after_kernel_computation(self, *args):
        """Update the view after kernel computation

        :param args: list of data type/kernel matrix names
        """
        dt_name_list = args[0]
        computed_names = [dt_name for dt_name,
        dt in self.data_types.items() if dt.kernel_matrix_computed]
        self.view.update_processed_data(computed_names)
        if len(dt_name_list) == 1:
            dt_name = dt_name_list[0]
            self.select_processed_by_name(dt_name)
        self.view.go_to_results_tab()
        self.view.update_progress_message(
            "Kernel matrices computed successfully", finished=True)
        self.view.update_input_icons()

    def regularize_current_precomp_kernel(self):
        """Regularize the current precomputed kernel matrix and update the view"""
        current_pt = self.precomp_types[self.view.current_precomp_item]
        should_reg = self.view.ask_kernel_correction(current_pt.name)
        if not should_reg:
            return
        try:
            current_pt.regularize()
        except ValueError:
            self.view.show_warning("Regularization failed",
                                   "Regularization failed: the matrix could not be made positive semi-definite by "
                                   "regularization. Please check the input data and try again. The matrix will be "
                                   "excluded from export as it is not valid.")
        self.view.update_precomp_vis(km=current_pt.kernel_matrix, shape=current_pt.kernel_shape, sym=current_pt.sym,
                                     psd=current_pt.psd, any_valid=len(
                self.valid_precomp_data) > 0,
                                     allow_reg=current_pt.regularization_possible)
        self.view.update_precomp_icons()

    def export_current_kernel_matrix(self):
        """Export the current kernel matrix to a file"""
        current_dt = self.data_types[self.view.current_processed_item]
        output_file = self.view.get_output_file(
            current_dt.name, force_mat=True)
        if not output_file:
            return
        if os.path.splitext(output_file)[1].lower() == ".mat":
            csv = False
        else:
            csv = True
        if current_dt.kernel_matrix_computed and isinstance(current_dt.kernel_matrix, np.ndarray):
            self.file_handler.export_kernels(
                {output_file: current_dt.kernel_matrix}, csv=csv)

    def export_all_kernel_matrices(self, csv=False):
        """Export all kernel matrices to a folder

        :param csv: whether to export the matrices as csv files
        """
        output_folder, export_id_file = self.view.show_export_warning()
        if not output_folder:
            return
        file_name_kernel_dict = {}
        name_param_dict = {}
        for name, dt in self.data_types.items():
            if dt.kernel_matrix_computed:
                dt_params = dt.current_computation_parameters
                method = dt_params["method"]
                if csv:
                    export_name = f"{name}_{method}_kernel.csv"
                else:
                    export_name = f"{name}_{method}_kernel.mat"
                export_path = os.path.join(output_folder, export_name)
                name_param_dict[export_name] = dt_params
                file_name_kernel_dict[export_path] = dt.kernel_matrix
        param_df = pd.DataFrame.from_dict(name_param_dict, orient="index")
        self.file_handler.export_kernels(
            file_name_kernel_dict, param_df, csv=csv)
        if export_id_file:
            self.export_id_file(os.path.join(output_folder, "sample_ids.txt"))

    def export_id_file(self, output_file):
        """Export the sample IDs to the given file"""
        if self.sample_names is None:
            self.view.update_progress_message("ID file export error: no sample IDs available! Please check your data.",
                                              finished=True)
            return
        if output_file is None:
            output_file = self.view.get_output_file("sample_ids", id_file=True)
        if not output_file:
            self.view.update_progress_message(
                "ID file export canceled: file name not valid", finished=True)
            return
        self.file_handler.export_id_file(self.sample_names, output_file)

    def update_after_export(self):
        """Update the view after exporting kernel matrices"""
        self.view.enable_modification(True)
        self.view.update_progress_message(
            "Kernel matrices saved successfully", finished=True)

    def export_precomp_kernel(self, name: str | None = None):
        """Export a precomputed kernel matrix to a file

        :param name: name of the precomputed kernel matrix to be exported
                     if None, export all valid precomputed kernel matrices
        """
        if name is None:
            if not self.has_precomp_data:
                return
            valid_names = self.valid_precomp_data
            if len(valid_names) == 0:
                return
            output_folder, export_ids = self.view.show_export_warning(
                no_log=True)
            if not output_folder:
                return
            km_dict = {
                os.path.join(output_folder, f"{name}.mat"): self.precomp_types[name].kernel_matrix for name in
                valid_names}
            self.file_handler.export_kernels(
                km_dict, log_data=None, csv=False)
            if export_ids:
                self.export_id_file(os.path.join(
                    output_folder, "sample_ids.txt"))
        else:
            if name not in self.precomp_types:
                return
            current_pt = self.precomp_types[self.view.current_precomp_item]
            if not current_pt.valid:
                return
            output_file = self.view.get_output_file(
                current_pt.name, id_file=False, force_mat=True)
            if not output_file:
                return
            self.file_handler.export_kernels({output_file: current_pt.kernel_matrix},
                                             csv=False)
