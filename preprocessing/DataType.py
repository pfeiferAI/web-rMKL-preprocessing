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

import numpy as np
import pandas as pd

from preprocessing.utils import compute_kernel, make_psd, check_psd


class DataType:
    """
    Class for storing data, kernel settings and kernel matrix of a single raw data type
    Implements methods for computing kernel matrix and setting kernel parameters
    """
    default_kernel_method = "rbf"
    default_rbf_gamma = 0.1
    default_poly_gamma = 1
    default_poly_degree = 3
    default_poly_coef0 = 1

    def __init__(self, name: str, raw_data: pd.DataFrame):
        self.name = name
        self.raw_data = raw_data
        self.kernel_matrix = None
        self.kernel_method = self.default_kernel_method
        self._rot_params = None
        self.linear_params = {}
        self.rbf_params = {}
        self.poly_params = {}
        self.init_rot_params()
        self.kernel_matrix_computed = False
        self._current_computation_parameters = None
        self.kernel_matrix_computation_error = False

    @property
    def data_shape(self) -> tuple:
        if self.raw_data is None:
            return 0, 0
        return self.raw_data.shape

    @property
    def rot_kernel_params(self) -> dict:
        if self._rot_params is None:
            return self.compute_rot_params()
        return self._rot_params

    @property
    def default_kernel_params(self) -> dict:
        if self.kernel_method == "rbf":
            return {"gamma": self.default_rbf_gamma,
                    "degree": None,
                    "coef0": None}
        elif self.kernel_method == "poly":
            return {"gamma": self.default_poly_gamma,
                    "degree": self.default_poly_degree,
                    "coef0": self.default_poly_coef0}
        else:
            return {"gamma": None, "degree": None, "coef0": None}

    @property
    def current_computation_parameters(self) -> dict | None:
        if self._current_computation_parameters is None:
            return None
        return self._current_computation_parameters.copy()

    @property
    def computation_parameters_changed(self) -> bool:
        if not self.kernel_matrix_computed or self.current_computation_parameters is None:
            return False
        if self.current_computation_parameters["method"] != self.kernel_method:
            return True
        changed = False
        for i in ["gamma", "degree", "coef0"]:
            if self.current_computation_parameters[i] != self.get_selected_kernel_params()[i]:
                changed = True
                break
        return changed

    @property
    def selected_kernel_method(self) -> str:
        return self.kernel_method

    @selected_kernel_method.setter
    def selected_kernel_method(self, value: str):
        # validate input
        if not isinstance(value, str) or value not in ["rbf", "poly", "linear"]:
            raise ValueError("value must be a string and one of 'rbf', 'poly' or 'linear'")
        if value == self.kernel_method:
            return
        self.kernel_method = value

    def reduce_data(self, sample_names: list[str]) -> bool:
        """Rearrange data according to the given sample_names and clear kernel matrix if it was computed"""
        self.raw_data = self.raw_data.loc[sample_names, :]
        self.init_rot_params()
        if self.kernel_matrix_computed:
            self.clear_kernel_matrix()
            return True  # return True if kernel matrix was cleared
        return False

    def get_preview_data(self, n_cols: int = 50, n_rows: int = 50) -> pd.DataFrame | None:
        """Return a preview of the data

        :param n_cols: number of columns to include in the preview, default = 50
        :param n_rows: number of rows to include in the preview default = 50
        :return: DataFrame containing a subset of the data for preview
        """
        if self.raw_data is None:
            return None
        n_rows = min(n_rows, self.raw_data.shape[0])
        n_cols = min(n_cols, self.raw_data.shape[1])
        tmp = self.raw_data.iloc[:n_rows, :n_cols].copy()
        return tmp

    def get_selected_kernel_params(self, kernel_method: str | None = None) -> dict:
        """Return the currently selected kernel parameters for the given kernel method"""
        if kernel_method is None:
            kernel_method = self.kernel_method
        if kernel_method == "rbf":
            return self.rbf_params.copy()
        elif kernel_method == "poly":
            return self.poly_params.copy()
        else:
            return self.linear_params.copy()

    def set_selected_kernel_params(self, value: dict, kernel_method: str | None = None):
        """Set the kernel parameters for the given kernel method
        Parameters are validated before setting

        :param value: dictionary containing the kernel parameters
        :param kernel_method: kernel method for which the parameters should be set
        :raises ValueError: if the input is not valid
        """
        if kernel_method is None:
            kernel_method = self.kernel_method
        else:
            self.selected_kernel_method = kernel_method
        if kernel_method == "rbf":
            self.rbf_params = value
        elif kernel_method == "poly":
            self.poly_params = value
        else:
            self.linear_params = value

        self.compute_rot_params()

    def set_param_to_default(self, param_name: str):
        """Set the given parameter to the default value"""
        if param_name not in ["gamma", "degree", "coef0"]:
            raise ValueError("param_name must be one of 'gamma', 'degree' or 'coef0'")
        if self.kernel_method == "rbf":
            self.rbf_params[param_name] = self.rot_kernel_params[param_name]
        elif self.kernel_method == "poly":
            self.poly_params[param_name] = self.rot_kernel_params[param_name]
        return

    def init_rot_params(self):
        """Initialize rule of thumb (rot) kernel parameters"""
        self.linear_params = self.compute_rot_params(method="linear")
        self.rbf_params = self.compute_rot_params(method="rbf")
        self.poly_params = self.compute_rot_params(method="poly")

    def compute_rot_params(self, method: str | None = None) -> dict:
        """Compute rule of thumb kernel parameters for the given method"""
        if method is None:
            method = self.kernel_method
        if self.raw_data is None:
            return self.default_kernel_params
        if self.raw_data.shape[0] < 2:
            return self.default_kernel_params
        if method == "rbf":
            return {"gamma": 1.0 / (2 * self.raw_data.shape[1] ** 2),
                    "degree": None,
                    "coef0": None}
        elif method == "poly":
            return {"gamma": self.default_poly_gamma,
                    "degree": self.default_poly_degree,
                    "coef0": self.default_poly_coef0}
        else:
            return {"gamma": None, "degree": None, "coef0": None}

    def compute_kernel_matrix(self):
        """Compute the kernel matrix using the currently selected kernel parameters"""
        try:
            params = self.get_selected_kernel_params()
            params["method"] = self.kernel_method
            self.kernel_matrix = compute_kernel(self.raw_data, params["method"], params["gamma"],
                                                params["degree"], params["coef0"])
        except ValueError:
            self.kernel_matrix_computed = False
            self.kernel_matrix_computation_error = True
        else:
            self.kernel_matrix_computed = True
            self.kernel_matrix_computation_error = False
            self._current_computation_parameters = params

    def clear_kernel_matrix(self):
        """Clear the kernel matrix"""
        self.kernel_matrix = None
        self.kernel_matrix_computed = False
        self.kernel_matrix_computation_error = False
        self._current_computation_parameters = None


class PrecompType:
    """
    Class for storing kernel matrix and its properties of a single precomputed data type
    Implements kernel regularization
    """

    def __init__(self, name: str, km: np.ndarray | pd.DataFrame, sym: bool, psd: bool):
        self.name = name
        if isinstance(km, pd.DataFrame):
            km = km.to_numpy()
        self.original_kernel_matrix = km
        self.psd_matrix = None  # positive semi-definite kernel matrix that was generated from original kernel matrix
        self.sym = sym  # kernel matrix is symmetric
        self.psd = psd  # kernel matrix is positive semi-definite
        self.regularization_possible = self.sym and not self.psd  # will be set to false after the first regularization

    @property
    def kernel_shape(self) -> tuple:
        return self.kernel_matrix.shape

    @property
    def valid(self) -> bool:
        return self.sym and self.psd

    @property
    def kernel_matrix(self) -> np.ndarray:
        if self.psd_matrix is None:
            return self.original_kernel_matrix
        return self.psd_matrix

    def regularize(self):
        """Regularize the kernel matrix to make it positive semi-definite and symmetric
        If the matrix is already positive semi-definite, it will be returned unchanged

        :raises ValueError: if the matrix cannot be regularized
        """
        try:
            tmp_matrix = make_psd(self.original_kernel_matrix)
        except ValueError as e:
            self.regularization_possible = False
            self.psd_matrix = None
            self.psd = False
            raise e
        else:
            self.psd_matrix = tmp_matrix
            self.sym, self.psd = check_psd(self.psd_matrix)
            self.regularization_possible = False
            return
