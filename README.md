# web-rMKL preprocessing

This repository contains a GUI application for generating kernel matrices from raw/primary data. These kernel
matrices can then be uploaded to [web-rmkl.org](https://web-rmkl.org) to perform an unsupervised multi-omics joint
dimensionality reduction with subsequent sample clustering. Please refer to the original publication of
[web-rMKL](https://doi.org/10.1093/nar/gkz422) for further details about the method and this preprocessing tool.

## Installation

Binary versions of web-rMKL preprocessing can be found under
[releases](https://github.com/pfeiferAI/web-rMKL-preprocessing/releases). These binaries come bundled with a recent version
of Python and all necessary packages (see license information in the 'About' dialog of the App). This means that files
may be executed directly without installation. Please note that previous versions of the web-rMKL preprocessing tool 
that were based on Java are now deprecated (all versions prior to 2.0). It is strongly recommended to use the new
Python-based tool.

`Windows` and `Linux` executables (.exe or .bin) are compiled for x86_64 systems. Their functionality on arm64 systems
has not been evaluated. If you encounter compatibility issues, you may try to run the application from source as
described below.

For `macOS`, the application is bundled in a DMG and may either be dragged to the Programs folder or executed directly
from the DMG. We currently only provide a binary for Apple Silicon (M1 and later) systems. If you are using an Intel-based, you will have to run the application from source.

You may also run the application from source. We recommend using Python 3.12.4 since web-rMKL preprocessing was
developed with this version. To run the application from source, please follow these steps:
- Clone this repository
- [optional] Create a virtual environment with `python -m venv web-rMKL-preprocessing`
- Install the web-rMKL preprocessing package with `pip install {path_to_repository}`. All necessary dependencies will
  be installed automatically.
- Upon installing the package, a command line entry point will be created. You may run the application by executing
  `web-rmkl-preprocessing` from the command line.
- Alternatively, you may run the application from source by executing `python -m preprocessing` from the
  command line in the root directory of the repository.

## Usage

### Input file requirements for web-rMKL

Two types of files are required to run a multi-omics dimensionality reduction and clustering analysis on
[web-rmkl.org](https://web-rmkl.org):
- `.mat` files containing symmetrical, positive semi-definite kernel matrices (e.g. one file per omic)
- a `.txt`file containing sample ID (one sample per row).

### Processing primary data for a web-rMKL submission

Based on raw data or processed primary data, the preprocessing tool can be used to compute kernel matrices and
generate sample ID files.

**Basic steps for processing data for web-rMKL:**

- Select _Primary data_ mode in the start screen of web-rMKL preprocessing.
- Import data from one or multiple `.csv` file by clicking on the 'Add' or 'Add data' button. Files must be formatted to 
  contain samples as rows and features (e.g. biomarkers) as columns. The data can either be indexed (sample IDs in first 
  column and feature names in the first row) or only numerical. All files should contain the same samples and the same sorting.
  An automatic reduction of the data to the intersection of all samples as well as automatic sorting are available for
  labeled data.
- Select the desired kernel method and parameters for every imported data file separately, or enable sync mode to
  apply the same settings to all data modalities. Default parameters are available for every kernel method to facilitate
  the parameter selection. The default kernel method is the RBF kernel. Please refer to the original publication of
  [web-rMKL](https://doi.org/10.1093/nar/gkz422) for further details about the kernel methods and parameters.
- Compute all kernel matrices by clicking on the 'Compute all' button. You will automatically be directed to the
  'Preprocessed Data' tab where you can find visualizations of the kernel matrices. Please note that further processing
  of the kernels will be carried out by web-rMKL.
- Export kernel matrices as `.mat` files by clicking 'Export all' and selecting an export directory. All computed
  kernels will be exported and a log file will be included to store the parameters that were selected. A sample ID file
  can be generated automatically (named `sample_ids.txt`) and saved to the same directory. If no sample IDs were given
  in the imported data, sample IDs will be numbered based on their index in the imported files
  (i.e., sample_1, sample_2, ..).

### Using precomputed kernel matrices and converting them to `.mat` files

As an alternative to using the built-in kernel methods of the web-rMKL preprocessing tool, you may also use your own
methods to compute kernel matrices. To use your own kernel matrices with web-rMKL, there are two different options:
- Save your kernel matrices to `.mat` files directly (e.g., by using the `scipy.io.savemat` method in Python)
- Convert your kernel matrices (saved as `.csv` files) using web-rMKL preprocessing

Please make sure that your precomputed kernel matrices are positive semi-definite and that all kernels have the same
order of samples. This is especially important if you save your kernel matrices to `.mat` files directly.

**Basic steps for converting precomputed kernel matrices:**

- Select _Precomputed kernel matrices_ mode in the start screen of web-rMKL preprocessing.
- Import kernel matrices from `.csv` files by clicking on the 'Add' or 'Add data' button. Files must only contain
  numerical values. All files should contain the same samples and the same sorting. Precomputed kernel matrices must
  be symmetrical and positive semi-definite.
- Imported kernel matrices will be validated automatically. The validation procedure checks whether the kernel matrices
  are symmetrical, and positive semi-definite. If the validation fails, the kernel matrices are labeled with warning
  symbols. Non-symmetrical kernel matrices will be ignored for further processing. Matrices that are symmetrical but
  not positive semi-definite may be regularized to attempt to make them positive semi-definite.
- [optional] Kernel matrix transformation: If an imported kernel matrix is symmetrical but not positive semi-definite,
  an automated transformation procedure can be applied to attempt to make the matrix positive semi-definite. This is
  done by adding a small constant to the diagonal of the matrix. For this, the smallest eigenvalue of the matrix is
  computed and a constant is added to the diagonal that is equal to the absolute value of the smallest eigenvalue. The applied method for matrix transformation is based the method described in the book *Practical Optimization* by [Gill, Murray & Wright (1981)](https://doi.org/10.1137/1.9781611975604).
  
  If the matrix is still not positive semi-definite after a preset limit of five iterations,
  it will be ignored for further processing and cannot be exported.
  
  Please note that this procedure may not
  always be successful and that the resulting kernel matrices may be diagonal dominant, which may lead to suboptimal
  results. If you want to use your own kernel matrices, we recommend to compute them with a method that guarantees
  positive semi-definiteness.
- Export kernel matrices as `.mat` files by clicking 'Export all valid matrices' and selecting an export directory. All 
  valid kernel matrices will be exported to the selected directory. A sample ID file can be generated automatically 
  (named `sample_ids.txt`) and saved to the same directory. Sample IDs will be numbered based on their index in the
  imported files (i.e., sample_1, sample_2, ..). It is recommended to use your own sample ID file to make the
  identification of samples in the results of web-rMKL easier (see input file requirements above).

### Troubleshooting:

- If you encounter issues with the data import, please verify that your `.csv` files are comma-separated. You may need
  to convert your files to utf-8 encoding if they cannot be imported otherwise.
- If you encounter issues with the kernel computation, please verify that your data is formatted correctly and that
  the selected kernel method is applicable to your data. All kernel methods require numerical data. If you want to use
  specialized kernel methods for other types of data you may compute kernel matrices externally and either directly save
  them as `.mat` files or use web-rMKL preprocessing to convert them (see description below).
- If you encounter issues with the export, please verify that you have write permissions for the selected export
  directory.

## Citing

If you use web-rMKL and/or this preprocessing tool, please cite the original publication:
```
Röder, B., Kersten, N., Herr, M., Speicher, N. K., & Pfeifer, N. (2019).
web-rMKL: a web server for dimensionality reduction and sample clustering of
multi-view data based on unsupervised multiple kernel learning.
Nucleic acids research, 47(W1), W605–W609. https://doi.org/10.1093/nar/gkz422
```

---

Copyright &copy; 2024 University of Tübingen, Nicolas Kersten