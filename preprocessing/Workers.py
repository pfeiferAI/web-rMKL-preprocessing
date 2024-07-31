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

import os.path
import sys
import traceback
from datetime import datetime
from enum import Enum

import numpy as np
import pandas as pd
from PySide6.QtCore import QObject, Signal, QRunnable, Slot
from scipy.io import savemat

from preprocessing.utils import check_psd


class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)
    status = Signal(str)


class Worker(QRunnable):
    """
    Worker thread for running background tasks independently of the main view thread
    """

    def __init__(self, function, *args, **kwargs):
        super().__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.is_killed = False

        self.kwargs["callback"] = self.signals.progress
        self.kwargs["status"] = self.signals.status
        self.kwargs["error"] = self.signals.error

    @Slot()
    def run(self):
        # Retrieve args/kwargs and use them to start processing
        try:
            result = self.function(*self.args, **self.kwargs)
        except:
            e, value = sys.exc_info()[:2]
            self.signals.error.emit((e, value, traceback.format_exc()))
        else:
            # Return the result of the processing
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()  # Done

    def kill(self):
        self.is_killed = True


class FileHandler:
    """
    Class for handling file import and export operations
    """

    validation_type = Enum("validation_type",
                           ["contains_nan", "unambiguous_index", "not_numeric",
                            "not_enough_data", "not_square", "ok"])

    def __init__(self, controller):
        self.controller = controller

    def load_files(self, file_list: list, indexed: bool, overwrite_names: list | None = None):
        """Load files from a list of file paths
        Will emit signals to update the view and controller

        :param file_list: list of file paths
        :param indexed: boolean indicating if the data is indexed (has row and column names)
        :param overwrite_names: list of names to overwrite the file names (pass through for later processing)
        """
        import_worker = Worker(self._load_files, file_list, indexed, overwrite_names)
        import_worker.signals.result.connect(self.controller.update_after_raw_import)
        import_worker.signals.progress.connect(self.controller.view.update_progress_bar)
        import_worker.signals.status.connect(self.controller.view.update_progress_message)
        import_worker.signals.error.connect(self.handle_import_error)
        self.controller.view.show_progress()
        self.controller.threadpool.start(import_worker)

    def handle_import_error(self, error: tuple):
        """Handle import errors and display error messages in the view
        Check if the error is a tuple with a list of files and a DataFrame
        and display the DataFrame as a log. Otherwise, display the error message.
        """
        self.controller.input_error = True
        self.controller.view.hide_progress()
        error_files = None
        error_log_df = None
        if len(error) == 3:
            error_files = error[1]
            error_log_df = error[2]
        if not isinstance(error_files, list) and not isinstance(error_log_df, pd.DataFrame):
            self.controller.view.show_custom_message("An unexpected import error occurred", str(error))
        elif error_files is None and isinstance(error_log_df, pd.DataFrame):
            self.controller.view.show_import_error_with_log(error_log_df)
        else:
            self.controller.view.show_io_error(error_files, io_type="import")

    def _load_files(self, file_list: list, indexed: bool, overwrite_names: list,
                    callback: Signal, status: Signal, error: Signal) -> tuple[dict, list, bool] | None:
        """Load files from a list of file paths

        :param file_list: list of file paths
        :param indexed: boolean indicating if the data is indexed (has row and column names)
        :param overwrite_names: list of names to overwrite the file names (pass through for later processing)
        :param callback: signal to update the progress bar
        :param status: signal to update the progress message
        :param error: signal to handle errors
        :return: tuple of a dictionary with file names and DataFrames, a list of names to overwrite and a boolean
                 indicating if the data is indexed
        """
        progress_step = 50 / len(file_list)
        progress = 0
        name_df_dict = {}
        if indexed:
            index_col = 0
            header = 0
        else:
            index_col = None
            header = None
        error_files = []
        validation_results = {}
        all_valid = True
        for file in file_list:
            status.emit(f"Loading file {os.path.basename(file)}")
            try:
                tmp_df = pd.read_csv(file, index_col=index_col, header=header)
                if not indexed:
                    tmp_df.columns = [f"feature_{i + 1}"
                                      for i in range(tmp_df.shape[1])]
                    tmp_df.index = [f"sample_{i + 1}"
                                    for i in range(tmp_df.shape[0])]
            except Exception as e:
                status.emit(f"Error loading file "
                            f"{os.path.basename(file)}...continuing")
                error_files.append(file)
                continue
            else:
                tmp_name = os.path.basename(file)
                tmp_name = os.path.splitext(tmp_name)[0]
            progress += progress_step
            callback.emit(progress)
            # validate data
            status.emit(f"Validating file {os.path.basename(file)}")
            tmp_valid = self.validate_file(tmp_df, indexed)
            validation_results[os.path.basename(file)] = tmp_valid
            if tmp_valid != self.validation_type.ok:
                status.emit(f"Error validating file {os.path.basename(file)}...continuing")
                all_valid = False
                continue
            else:
                name_df_dict[tmp_name] = tmp_df
            progress += progress_step
            callback.emit(progress)
        if error_files:
            error.emit(("File import error", error_files, None))
        if not all_valid:
            error.emit(("File validation error", None, self.get_validation_log(validation_results)))
        else:
            return name_df_dict, overwrite_names, indexed

    def validate_file(self, file_df: pd.DataFrame, indexed: bool, check_square: bool = False) -> validation_type:
        """Validate a DataFrame for import
        Check if the data is numeric, indexed, contains NaN values, has enough data and is square (if required)

        :param file_df: DataFrame to validate
        :param indexed: boolean indicating if the data is indexed (has row and column names)
        :param check_square: boolean indicating if the data must be square
        :return: validation_type indicating the validation result
        """
        if any(s < 2 for s in file_df.shape):
            return self.validation_type.not_enough_data
        # check if data is numeric
        if not all(file_df.dtypes.apply(lambda x: np.issubdtype(x, np.number))):
            return self.validation_type.not_numeric
        # check if data is indexed
        if indexed:
            if not file_df.index.is_unique:
                return self.validation_type.unambiguous_index
        # check if data_contains nan values
        if file_df.isna().values.any():
            return self.validation_type.contains_nan
        if check_square:
            if file_df.shape[0] != file_df.shape[1]:
                return self.validation_type.not_square
        return self.validation_type.ok

    def get_validation_log(self, validation_dict: dict) -> pd.DataFrame:
        """Create a DataFrame from a dictionary of validation results to display as an error log"""
        validation_log = {}
        for name, error_type in validation_dict.items():
            if error_type == self.validation_type.contains_nan:
                validation_log[name] = "Contains NaN values"
            elif error_type == self.validation_type.unambiguous_index:
                validation_log[name] = "Index is not unambiguous"
            elif error_type == self.validation_type.not_numeric:
                validation_log[name] = "Data is not numeric"
            elif error_type == self.validation_type.not_enough_data:
                validation_log[name] = "Not enough data: less than 2 rows or columns"
            elif error_type == self.validation_type.not_square:
                validation_log[name] = "Matrix is not square"
            elif error_type == self.validation_type.ok:
                validation_log[name] = "OK"
        return pd.DataFrame.from_dict(validation_log, orient="index", columns=["Validation"])

    def load_kernels(self, file_list: list, overwrite_names: list):
        """Load kernel matrices from a list of file paths
        Will emit signals to update the view and controller

        :param file_list: list of file paths
        :param overwrite_names: list of names to overwrite the file names (pass through for later processing)
        """
        import_worker = Worker(self._load_kernels, file_list, overwrite_names)
        import_worker.signals.result.connect(self.controller.update_after_precomp_import)
        import_worker.signals.progress.connect(self.controller.view.update_progress_bar)
        import_worker.signals.status.connect(self.controller.view.update_progress_message)
        import_worker.signals.error.connect(self.handle_import_error)
        self.controller.view.show_progress()
        self.controller.view.enable_modification(False)
        self.controller.threadpool.start(import_worker)

    def _load_kernels(self, file_list: list, overwrite_names: list,
                      callback: Signal, status: Signal, error: Signal) -> tuple[dict, list] | None:
        """Load kernel matrices from a list of file paths

        :param file_list: list of file paths
        :param overwrite_names: list of names to overwrite the file names (pass through for later processing)
        :param callback: signal to update the progress bar
        :param status: signal to update the progress message
        :param error: signal to handle errors
        :return: tuple of a dictionary with file names and kernel matrices and a list of names to overwrite
        """
        progress_step = 50 / len(file_list)
        progress = 0
        name_data_dict = {}
        name_error_dict = {}
        all_valid = True
        for file in file_list:
            status.emit(f"Loading file {os.path.basename(file)}")
            try:
                tmp_df = pd.read_csv(file, index_col=None, header=None)
            except:
                status.emit(f"Error loading file {
                os.path.basename(file)}...continuing")
                name_data_dict[os.path.basename(file)] = "Could not read file"
                continue
            else:
                tmp_name = os.path.basename(file)
                tmp_name = os.path.splitext(tmp_name)[0]
            progress += progress_step
            callback.emit(progress)
            # validation
            status.emit(f"Validating file {os.path.basename(file)}")
            tmp_valid = self.validate_file(tmp_df, indexed=False)

            if not tmp_valid == self.validation_type.ok:
                all_valid = False
                status.emit(f"Error validating file {os.path.basename(file)}...continuing")
                progress += progress_step
                continue

            tmp_matrix = tmp_df.to_numpy()
            # check if matrix is symmetric and positive semi-definite
            is_sym, is_psd = check_psd(tmp_matrix)

            name_data_dict[tmp_name] = {
                "data": tmp_matrix, "symmetric": is_sym, "psd": is_psd}

            progress += progress_step
            callback.emit(progress)

        if not all_valid:
            error.emit(("File validation error",
                        None, self.get_validation_log(name_error_dict)))
        else:
            return name_data_dict, overwrite_names

    def export_kernels(self, name_kernel_dict: dict, log_data: pd.DataFrame | None = None,
                       csv: bool = False):
        """Export kernel matrices to a file or directory
        Will emit signals to update the view and controller

        :param name_kernel_dict: dictionary with kernel names and matrices
        :param log_data: DataFrame with log data to export
        :param csv: boolean indicating if the data should be exported as csv
        """
        save_worker = Worker(self._export_kernels, name_kernel_dict, log_data, csv)
        save_worker.signals.finished.connect(self.controller.update_after_export)
        save_worker.signals.progress.connect(self.controller.view.update_progress_bar)
        save_worker.signals.status.connect(self.controller.view.update_progress_message)
        save_worker.signals.error.connect(self.handle_export_error)
        self.controller.view.show_progress()
        self.controller.view.enable_modification(False)

        self.controller.threadpool.start(save_worker)

    def handle_export_error(self, error: tuple):
        """Handle export errors and display error messages in the view."""
        export_path = None
        single_file = None
        if len(error) == 3:
            export_path = error[1]
            single_file = error[2]
        if not isinstance(single_file, bool):
            self.controller.view.show_custom_message(
                "An unexpected export error occurred", str(error)
            )
        elif single_file:
            self.controller.view.show_io_error(export_path, io_type="export")
        else:
            self.controller.view.show_multi_export_error(export_path)

    def _export_kernels(self, name_kernel_dict: dict, log_data: pd.DataFrame, csv: bool,
                        callback: Signal, status: Signal, error: Signal):
        """Export kernel matrices to a file or directory

        :param name_kernel_dict: dictionary with kernel names (path + file name) and matrices
        :param log_data: DataFrame with log data to export
        :param csv: boolean indicating if the data should be exported as csv
        :param callback: signal to update the progress bar
        :param status: signal to update the progress message
        :param error: signal to handle errors
        :return: boolean indicating if the export was successful
        """
        progress = 0
        progress_step = 100 / (len(name_kernel_dict) +
                               0 if log_data is None else 1)
        export_path = None
        single_file = len(name_kernel_dict) == 1
        for name, kernel in name_kernel_dict.items():
            if export_path is None:
                export_path = os.path.dirname(name)
            status.emit(f"Exporting kernel to {
            os.path.basename(export_path)}")
            try:
                if csv:
                    np.savetxt(name, kernel, delimiter=",")
                else:
                    savemat(name, {"kernel": kernel})
            except Exception as e:
                if single_file:
                    error.emit((e, name, True))
                else:
                    error.emit((e, export_path, False))
            progress += progress_step
            callback.emit(progress)
        if log_data is not None and export_path is not None:
            status.emit("Saving log file")
            log_file_name = f"web-rMKL_preprocessing_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
            log_file_path = os.path.join(str(export_path), log_file_name)
            try:
                log_data.to_csv(log_file_path)
            except Exception as e:
                error.emit((e, log_file_path, True))
            progress += progress_step
            callback.emit(progress)
        return True

    def export_id_file(self, sample_id_list: list, export_path: str) -> bool:
        """Export a list of sample IDs to a file

        :param sample_id_list: list of sample IDs
        :param export_path: file path to export to
        :return: boolean indicating if the export was successful
        """
        if export_path is None or len(export_path) < 1:
            return False
        id_series = pd.Series(sample_id_list)
        try:
            id_series.to_csv(export_path, index=False, header=False)
        except Exception as e:
            return False
        else:
            return True


class ComputeHandler:
    """
    Class for handling kernel computation operations
    """

    def __init__(self, controller):
        self.controller = controller

    def compute_kernels(self, dt_list: list):
        """Compute kernel matrices for a list of DataTypes
        Will emit signals to update the view and controller

        :param dt_list: list of DataTypes
        """
        compute_worker = Worker(self._compute_kernel, dt_list)
        compute_worker.signals.result.connect(
            self.controller.update_after_kernel_computation)
        compute_worker.signals.progress.connect(
            self.controller.view.update_progress_bar)
        compute_worker.signals.status.connect(
            self.controller.view.update_progress_message)
        compute_worker.signals.error.connect(
            lambda e:
            self.controller.view.show_custom_message(
                "Unexpected kernel computation error", str(e)))
        self.controller.view.show_progress()

        self.controller.threadpool.start(compute_worker)

    @staticmethod
    def _compute_kernel(dt_list: list, callback: Signal, status: Signal, error: Signal) -> list:
        """Compute kernel matrices for a list of DataTypes

        :param dt_list: list of DataTypes
        :param callback: signal to update the progress bar
        :param status: signal to update the progress message
        :param error: signal to handle errors
        :return: list of names of DataTypes that were processed
        """
        progress_step = 100 / len(dt_list)
        progress = 0
        processed_dts = []
        for dt in dt_list:
            status.emit(f"Computing kernel for {dt.name}")
            try:
                dt.compute_kernel_matrix()
            except Exception as e:
                error.emit(e)
            else:
                processed_dts.append(dt.name)
            progress += progress_step
            callback.emit(progress)
        return processed_dts
