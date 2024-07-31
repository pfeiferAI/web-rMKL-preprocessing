from setuptools import setup

setup(
    name='web-rMKL-preprocessing',
    version='2.0.0',
    packages=['preprocessing'],
    entry_points = {
        'console_scripts': [
            'web-rMKL-preprocessing = preprocessing.App:main'
        ]
    },
    install_requires=[
        'PySide6==6.5.3',
        'numpy==2.0.2',
        'pandas==2.2.2',
        'scipy==1.14.0',
        'scikit-learn==1.5.1',
        'matplotlib==3.9.1'
    ],
    author='Nicolas Kersten',
    author_email='nicolas.kersten@uni-tuebingen.de',
    description='A preprocessing tool for web-rMKL',
    long_description=open('README.md', encoding='utf-8').read(),
    license='GNU General Public License v3.0',
    url='https://github.com/pfeiferAI/web-rMKL_preprocessing'
)