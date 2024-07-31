import unittest
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import rbf_kernel, polynomial_kernel, linear_kernel
from preprocessing.utils import compute_kernel, make_psd, check_psd, reduce_and_sort_data


class TestComputeKernel(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        self.data = pd.DataFrame({
            'feature1': [1, 2, 3],
            'feature2': [4, 5, 6]
        })

    def test_rbf_kernel(self):
        gamma = 0.5
        expected = rbf_kernel(self.data, gamma=gamma)
        result = compute_kernel(self.data, kernel_method="rbf", gamma=gamma)
        np.testing.assert_array_almost_equal(result, expected, decimal=6)

    def test_polynomial_kernel(self):
        degree = 3
        gamma = 0.5
        coef0 = 1
        expected = polynomial_kernel(self.data, degree=degree, gamma=gamma, coef0=coef0)
        result = compute_kernel(self.data, kernel_method="poly", degree=degree, gamma=gamma, coef0=coef0)
        np.testing.assert_array_almost_equal(result, expected, decimal=6)

    def test_linear_kernel(self):
        expected = linear_kernel(self.data)
        result = compute_kernel(self.data, kernel_method="linear")
        np.testing.assert_array_almost_equal(result, expected, decimal=6)

    def test_invalid_kernel_method(self):
        with self.assertRaises(ValueError):
            compute_kernel(self.data, kernel_method="invalid")


class TestCheckPSD(unittest.TestCase):
    
    def setUp(self):
        np.random.seed(0)
        A = np.random.rand(10, 10)
        self.psd_mat = np.dot(A, A.T)
        B = A - 0.5
        self.non_psd_mat = (B + B.T) / 2
        self.non_sym_mat = np.array([[1, 2], [3, 4]])

    def test_symmetric_and_psd_matrix(self):
        symmetric, psd = check_psd(self.psd_mat)
        self.assertTrue(symmetric)
        self.assertTrue(psd)

    def test_symmetric_but_not_psd_matrix(self):
        symmetric, psd = check_psd(self.non_psd_mat)
        self.assertTrue(symmetric)
        self.assertFalse(psd)

    def test_non_symmetric_matrix(self):
        symmetric, psd = check_psd(self.non_sym_mat)
        self.assertFalse(symmetric)
        self.assertFalse(psd)

    def test_non_square_matrix(self):
        matrix = np.array([[1, 2, 3], [4, 5, 6]])
        with self.assertRaises(ValueError):
            check_psd(matrix)

    def test_non_2d_array(self):
        matrix = np.array([1, 2, 3])
        with self.assertRaises(ValueError):
            check_psd(matrix)

    def test_non_numpy_or_dataframe_input(self):
        matrix = [[1, 2], [2, 1]]
        with self.assertRaises(ValueError):
            check_psd(matrix)


class TestMakePSD(unittest.TestCase):

    def setUp(self):
        np.random.seed(0)
        A = np.random.rand(10, 10)
        self.psd_mat = np.dot(A, A.T)
        B = A - 0.5
        self.non_psd_mat = (B + B.T) / 2
        self.non_sym_mat = np.array([[1, 2], [3, 4]])

    def test_make_psd_already_psd(self):
        result = make_psd(self.psd_mat)
        np.testing.assert_array_almost_equal(result, self.psd_mat, decimal=6)

    def test_make_psd_non_psd(self):
        result = make_psd(self.non_psd_mat)
        symmetric, psd = check_psd(result)
        self.assertTrue(symmetric)
        self.assertTrue(psd)

    def test_make_psd_non_symmetric(self):
        with self.assertRaises(ValueError):
            make_psd(self.non_sym_mat)


class TestReduceAndSortData(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        self.data_dict = {
            'df1': pd.DataFrame({
                'feature1': [1, 2, 3],
                'feature2': [4, 5, 6]
            }, index=['A', 'B', 'C']),
            'df2': pd.DataFrame({
                'feature1': [7, 8, 9],
                'feature2': [10, 11, 12]
            }, index=['B', 'C', 'A']),
            'df3': pd.DataFrame({
                'feature1': [13, 14, 15, 19],
                'feature2': [16, 17, 18, 20]
            }, index=['A', 'C', 'E', 'B'])
        }

    def test_reduce_and_sort_common_sample_names(self):
        expected_data_dict = {
            'df1': pd.DataFrame({
                'feature1': [1, 2, 3],
                'feature2': [4, 5, 6]
            }, index=['A', 'B', 'C']),
            'df2': pd.DataFrame({
                'feature1': [9, 7, 8],
                'feature2': [12, 10, 11]
            }, index=['A', 'B', 'C']),
            'df3': pd.DataFrame({
                'feature1': [13, 19, 14],
                'feature2': [16, 20, 17]
            }, index=['A', 'B', 'C'])
        }
        expected_sample_names = np.array(['A', 'B', 'C'])
        result_data_dict, result_sample_names = reduce_and_sort_data(self.data_dict)
        for key in expected_data_dict:
            pd.testing.assert_frame_equal(result_data_dict[key], expected_data_dict[key])
        np.testing.assert_array_equal(result_sample_names, expected_sample_names)

    def test_reduce_and_sort_with_provided_sample_names(self):
        sample_names = ['A', 'C']
        expected_data_dict = {
            'df1': pd.DataFrame({
                'feature1': [1, 3],
                'feature2': [4, 6]
            }, index=['A', 'C']),
            'df2': pd.DataFrame({
                'feature1': [9, 8],
                'feature2': [12, 11]
            }, index=['A', 'C']),
            'df3': pd.DataFrame({
                'feature1': [13, 14],
                'feature2': [16, 17]
            }, index=['A', 'C'])
        }
        expected_sample_names = np.array(['A', 'C'])
        result_data_dict, result_sample_names = reduce_and_sort_data(self.data_dict, sample_names)
        for key in expected_data_dict:
            pd.testing.assert_frame_equal(result_data_dict[key], expected_data_dict[key])
        np.testing.assert_array_equal(result_sample_names, expected_sample_names)

    def test_reduce_and_sort_no_common_sample_names(self):
        data_dict = {
            'df1': pd.DataFrame({
                'feature1': [1, 2],
                'feature2': [3, 4]
            }, index=['A', 'B']),
            'df2': pd.DataFrame({
                'feature1': [5, 6],
                'feature2': [7, 8]
            }, index=['C', 'D'])
        }
        expected_data_dict = {}
        expected_sample_names = np.array([])
        result_data_dict, result_sample_names = reduce_and_sort_data(data_dict)
        np.testing.assert_array_equal(result_sample_names, expected_sample_names)
        self.assertEqual(result_data_dict, expected_data_dict)

    def test_reduce_and_sort_empty_data(self):
        data_dict = {
            'df1': pd.DataFrame(columns=['feature1', 'feature2']),
            'df2': pd.DataFrame(columns=['feature1', 'feature2'])
        }
        expected_data_dict = {}
        expected_sample_names = np.array([])
        result_data_dict, result_sample_names = reduce_and_sort_data(data_dict)
        np.testing.assert_array_equal(result_sample_names, expected_sample_names)
        self.assertEqual(result_data_dict, expected_data_dict)

    def test_reduce_and_sort_no_overlap_with_provided_sample_names(self):
        expected_data_dict = {}
        expected_sample_names = np.array([])
        result_data_dict, result_sample_names = reduce_and_sort_data(self.data_dict, ['E', 'X', 'Y'])
        np.testing.assert_array_equal(result_sample_names, expected_sample_names)
        self.assertEqual(result_data_dict, expected_data_dict)
