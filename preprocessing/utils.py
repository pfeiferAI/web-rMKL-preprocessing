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
from sklearn.metrics.pairwise import rbf_kernel, polynomial_kernel, linear_kernel


def check_psd(matrix: np.ndarray | pd.DataFrame) -> tuple[bool, bool]:
    """Check if a given kernel matrix is positive semi-definite and symmetric
    
    :param matrix: kernel matrix
    :return: tuple of bools (symmetric, positive semi-definite)
    """
    if not isinstance(matrix, np.ndarray):
        if isinstance(matrix, pd.DataFrame):
            matrix = matrix.to_numpy()
        else:
            raise ValueError("matrix must be a numpy array")
    if matrix.ndim != 2:
        raise ValueError("matrix must be a 2D array")
    if matrix.shape[0] != matrix.shape[1]:
        raise ValueError("matrix must be square")
    if not np.allclose(matrix, matrix.T):
        return False, False
    try:
        psd = all(np.linalg.eigvalsh(matrix) >= 0)
    except np.linalg.LinAlgError:
        return True, False
    else:
        return True, psd


def make_psd(matrix: np.ndarray, max_iter: int = 5) -> np.ndarray:
    """Make a given matrix positive semi-definite by adding a small value to the diagonal
    Method based on "Practical Optimization" by Gill, Murray & Wright (1981) https://doi.org/10.1137/1.9781611975604
    
    :param matrix: kernel matrix
    :param max_iter: maximum number of iterations to make matrix positive semi-definite
    :return: positive semi-definite matrix
    :raises ValueError: if matrix cannot be made positive semi-definite
    """
    input_symmetric, input_psd = check_psd(matrix)
    if not input_symmetric:
        raise ValueError("matrix must be symmetric!")
    if input_psd:
        return matrix
    psd = False
    it_count = 1
    matrix_ = matrix.copy()
    while not psd:
        eigvals = np.linalg.eigvalsh(matrix_)
        if eigvals.min() >= 0:
            psd = True
            break
        matrix_ = matrix_ + np.eye(matrix.shape[0]) * (1 - eigvals.min())
        psd = check_psd(matrix_)[1]
        it_count += 1
        if it_count > max_iter:
            break
    if psd:
        return matrix_
    else:
        raise ValueError("could not make matrix positive semi-definite")


def compute_kernel(data: pd.DataFrame, kernel_method: str, gamma: float | None = None,
                   degree: int | None = None, coef0: float | None = None) -> np.ndarray:
    """Compute rbf, polynomial, linear or custom kernel for a given intput dataframe or 2D array
    
    :param data: input raw data as dataframe or 2d array
    :param kernel_method: rbf, poly or linear
    :param coef0: coef0 parameter for poly kernel
    :param degree: degree of polynomial kernel
    :param gamma: gamma parameter for rbf and poly kernel
    :return: kernel matrix as 2D array
    :raises ValueError: if kernel method is not supported
    """
    if kernel_method == "rbf":
        return rbf_kernel(data, gamma=gamma)
    elif kernel_method == "poly":
        return polynomial_kernel(data, degree=degree, gamma=gamma, coef0=coef0)
    elif kernel_method == "linear":
        return linear_kernel(data)
    else:
        raise ValueError(f"kernel method {kernel_method} not supported!")


def reduce_and_sort_data(data_dict: dict[str, pd.DataFrame],
                         sample_names: list | np.ndarray | None = None) -> tuple[dict[str, pd.DataFrame], np.ndarray]:
    """Reduce data to common sample names and sort them to have the same order in all dataframes
    
    :param data_dict: dictionary containing dataframes
    :param sample_names: list of sample names to reduce to and sort by
    :return: reduced data_dict and sorted sample names
    """
    # check if there are any common sample names
    all_sample_names = [set(v.index.values) for v in data_dict.values()]
    overlap = all_sample_names[0].intersection(*all_sample_names[1:])
    if not overlap:
        return {}, np.array([])
    overlap = np.array(list(overlap))
    if sample_names is not None:
        new_sample_names = [n for n in overlap if n in sample_names]
    else:
        new_sample_names = overlap
    new_sample_names = np.sort(new_sample_names)
    new_data_dict = {}
    for k, v in data_dict.items():
        new_data_dict[k] = v.loc[new_sample_names, :]
    if all(v.empty for v in new_data_dict.values()):
        return {}, np.array([])
    return new_data_dict, new_sample_names
