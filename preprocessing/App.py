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
__version__ = "2.0"
__copyright__ = "2024, University of Tuebingen, Nicolas Kersten"
__author_mail__ = "nicolas.kersten@uni-tuebingen.de"
__repository_url__ = "https://github.com/pfeiferAI/web-rMKL-preprocessing"
__website_url__ = "https://web-rMKL.org"

import sys

from PySide6.QtWidgets import QApplication

from preprocessing.Controller import Controller
from preprocessing.View import View


class App(QApplication):
    """
    Main entry point for the web-rMKL preprocessing app
    """

    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.version = __version__
        self.copyright = __copyright__
        self.repo_url = __repository_url__
        self.web_rmkl_url = __website_url__
        self.main_ctrl = Controller(self)
        self.main_view = View(self.main_ctrl)
        self.main_view.show()


def main():
    app = App(sys.argv)
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
