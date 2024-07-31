# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QButtonGroup, QCheckBox,
    QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QListView,
    QListWidget, QListWidgetItem, QMainWindow, QMenu,
    QMenuBar, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QTabWidget, QTableView, QToolButton,
    QVBoxLayout, QWidget)
from preprocessing import icons_and_img_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(u"")
        MainWindow.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)
        self.action_compute_all = QAction(MainWindow)
        self.action_compute_all.setObjectName(u"action_compute_all")
        self.action_compute_all.setEnabled(False)
        self.action_compute_current = QAction(MainWindow)
        self.action_compute_current.setObjectName(u"action_compute_current")
        self.action_compute_current.setEnabled(False)
        self.action_add_data = QAction(MainWindow)
        self.action_add_data.setObjectName(u"action_add_data")
        self.action_add_data.setEnabled(False)
        self.action_export_all = QAction(MainWindow)
        self.action_export_all.setObjectName(u"action_export_all")
        self.action_export_all.setEnabled(False)
        self.action_export_current = QAction(MainWindow)
        self.action_export_current.setObjectName(u"action_export_current")
        self.action_export_current.setEnabled(False)
        font = QFont()
        self.action_export_current.setFont(font)
        self.action_help = QAction(MainWindow)
        self.action_help.setObjectName(u"action_help")
        self.action_about = QAction(MainWindow)
        self.action_about.setObjectName(u"action_about")
        self.action_go_to_rmkl = QAction(MainWindow)
        self.action_go_to_rmkl.setObjectName(u"action_go_to_rmkl")
        self.action_export_all_csv = QAction(MainWindow)
        self.action_export_all_csv.setObjectName(u"action_export_all_csv")
        self.action_export_all_csv.setEnabled(False)
        self.action_export_index = QAction(MainWindow)
        self.action_export_index.setObjectName(u"action_export_index")
        self.action_export_index.setEnabled(False)
        self.central_widget = QWidget(MainWindow)
        self.central_widget.setObjectName(u"central_widget")
        self.verticalLayout = QVBoxLayout(self.central_widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 10, 5, 10)
        self.tab_widget = QTabWidget(self.central_widget)
        self.tab_widget.setObjectName(u"tab_widget")
        self.tab_widget.setStyleSheet(u"QTabWidget::tab-bar {\n"
"	alignment: center;\n"
"}")
        self.tab_widget.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.input_selection_tab = QWidget()
        self.input_selection_tab.setObjectName(u"input_selection_tab")
        self.verticalLayout_3 = QVBoxLayout(self.input_selection_tab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)

        self.start_icon_layout = QHBoxLayout()
        self.start_icon_layout.setSpacing(10)
        self.start_icon_layout.setObjectName(u"start_icon_layout")
        self.start_icon = QToolButton(self.input_selection_tab)
        self.start_icon.setObjectName(u"start_icon")
        self.start_icon.setStyleSheet(u"background: transparent;")
        self.start_icon.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        icon = QIcon()
        icon.addFile(u":/logo/logo.png", QSize(), QIcon.Mode.Disabled, QIcon.State.Off)
        self.start_icon.setIcon(icon)
        self.start_icon.setIconSize(QSize(80, 80))

        self.start_icon_layout.addWidget(self.start_icon)


        self.verticalLayout_3.addLayout(self.start_icon_layout)

        self.start_name_label = QLabel(self.input_selection_tab)
        self.start_name_label.setObjectName(u"start_name_label")
        font1 = QFont()
        font1.setPointSize(20)
        font1.setBold(True)
        self.start_name_label.setFont(font1)
        self.start_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.start_name_label)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.start_input_question_label = QLabel(self.input_selection_tab)
        self.start_input_question_label.setObjectName(u"start_input_question_label")
        font2 = QFont()
        font2.setBold(True)
        self.start_input_question_label.setFont(font2)
        self.start_input_question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.start_input_question_label.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.start_input_question_label)

        self.input_selection_layout = QGridLayout()
        self.input_selection_layout.setObjectName(u"input_selection_layout")
        self.start_raw_btn = QPushButton(self.input_selection_tab)
        self.start_raw_btn.setObjectName(u"start_raw_btn")
        font3 = QFont()
        font3.setPointSize(15)
        font3.setBold(True)
        self.start_raw_btn.setFont(font3)
        self.start_raw_btn.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.start_raw_btn.setText(u"Primary data")

        self.input_selection_layout.addWidget(self.start_raw_btn, 0, 0, 1, 1)

        self.primary_info_text = QLabel(self.input_selection_tab)
        self.primary_info_text.setObjectName(u"primary_info_text")

        self.input_selection_layout.addWidget(self.primary_info_text, 1, 0, 1, 1)

        self.start_precomp_btn = QPushButton(self.input_selection_tab)
        self.start_precomp_btn.setObjectName(u"start_precomp_btn")
        self.start_precomp_btn.setFont(font3)
        self.start_precomp_btn.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.start_precomp_btn.setText(u"Precomputed kernel matrices")

        self.input_selection_layout.addWidget(self.start_precomp_btn, 0, 1, 1, 1)

        self.precomp_info_text = QLabel(self.input_selection_tab)
        self.precomp_info_text.setObjectName(u"precomp_info_text")

        self.input_selection_layout.addWidget(self.precomp_info_text, 1, 1, 1, 1)


        self.verticalLayout_3.addLayout(self.input_selection_layout)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.start_help_layout = QHBoxLayout()
        self.start_help_layout.setObjectName(u"start_help_layout")
        self.start_version_label = QLabel(self.input_selection_tab)
        self.start_version_label.setObjectName(u"start_version_label")

        self.start_help_layout.addWidget(self.start_version_label)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.start_help_layout.addItem(self.horizontalSpacer_4)

        self.start_help_button = QPushButton(self.input_selection_tab)
        self.start_help_button.setObjectName(u"start_help_button")

        self.start_help_layout.addWidget(self.start_help_button)


        self.verticalLayout_3.addLayout(self.start_help_layout)

        self.tab_widget.addTab(self.input_selection_tab, "")
        self.raw_input_tab = QWidget()
        self.raw_input_tab.setObjectName(u"raw_input_tab")
        self.verticalLayout_6 = QVBoxLayout(self.raw_input_tab)
        self.verticalLayout_6.setSpacing(5)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(10, 10, 10, 10)
        self.raw_input_layout = QHBoxLayout()
        self.raw_input_layout.setSpacing(20)
        self.raw_input_layout.setObjectName(u"raw_input_layout")
        self.raw_input_list_layout = QVBoxLayout()
        self.raw_input_list_layout.setSpacing(3)
        self.raw_input_list_layout.setObjectName(u"raw_input_list_layout")
        self.raw_import_layout = QHBoxLayout()
        self.raw_import_layout.setObjectName(u"raw_import_layout")
        self.input_list_label = QLabel(self.raw_input_tab)
        self.input_list_label.setObjectName(u"input_list_label")
        self.input_list_label.setFont(font2)
        self.input_list_label.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))

        self.raw_import_layout.addWidget(self.input_list_label)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.raw_import_layout.addItem(self.horizontalSpacer_6)

        self.raw_add_data_btn = QPushButton(self.raw_input_tab)
        self.raw_add_data_btn.setObjectName(u"raw_add_data_btn")

        self.raw_import_layout.addWidget(self.raw_add_data_btn)


        self.raw_input_list_layout.addLayout(self.raw_import_layout)

        self.input_listwidget = QListWidget(self.raw_input_tab)
        self.input_listwidget.setObjectName(u"input_listwidget")
        self.input_listwidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.input_listwidget.setDefaultDropAction(Qt.DropAction.CopyAction)
        self.input_listwidget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.input_listwidget.setMovement(QListView.Movement.Static)
        self.input_listwidget.setFlow(QListView.Flow.TopToBottom)
        self.input_listwidget.setProperty("isWrapping", False)
        self.input_listwidget.setViewMode(QListView.ViewMode.ListMode)

        self.raw_input_list_layout.addWidget(self.input_listwidget)

        self.raw_input_list_layout.setStretch(1, 1)

        self.raw_input_layout.addLayout(self.raw_input_list_layout)

        self.input_table_layout = QVBoxLayout()
        self.input_table_layout.setSpacing(3)
        self.input_table_layout.setObjectName(u"input_table_layout")
        self.input_counts_layout = QHBoxLayout()
        self.input_counts_layout.setSpacing(10)
        self.input_counts_layout.setObjectName(u"input_counts_layout")
        self.input_counts_layout.setContentsMargins(-1, 3, -1, 3)
        self.input_preview_label = QLabel(self.raw_input_tab)
        self.input_preview_label.setObjectName(u"input_preview_label")
        self.input_preview_label.setFont(font2)
        self.input_preview_label.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))

        self.input_counts_layout.addWidget(self.input_preview_label)

        self.input_sample_count = QLabel(self.raw_input_tab)
        self.input_sample_count.setObjectName(u"input_sample_count")

        self.input_counts_layout.addWidget(self.input_sample_count)

        self.input_samples_label = QLabel(self.raw_input_tab)
        self.input_samples_label.setObjectName(u"input_samples_label")

        self.input_counts_layout.addWidget(self.input_samples_label)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.input_counts_layout.addItem(self.horizontalSpacer_3)

        self.input_feature_count = QLabel(self.raw_input_tab)
        self.input_feature_count.setObjectName(u"input_feature_count")

        self.input_counts_layout.addWidget(self.input_feature_count)

        self.input_features_label = QLabel(self.raw_input_tab)
        self.input_features_label.setObjectName(u"input_features_label")

        self.input_counts_layout.addWidget(self.input_features_label)

        self.input_counts_layout.setStretch(0, 1)

        self.input_table_layout.addLayout(self.input_counts_layout)

        self.input_tableview = QTableView(self.raw_input_tab)
        self.input_tableview.setObjectName(u"input_tableview")
        self.input_tableview.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.input_tableview.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.input_tableview.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

        self.input_table_layout.addWidget(self.input_tableview)

        self.input_table_layout.setStretch(1, 1)

        self.raw_input_layout.addLayout(self.input_table_layout)

        self.raw_input_layout.setStretch(0, 1)
        self.raw_input_layout.setStretch(1, 3)

        self.verticalLayout_6.addLayout(self.raw_input_layout)

        self.icon_legend_layout = QHBoxLayout()
        self.icon_legend_layout.setSpacing(0)
        self.icon_legend_layout.setObjectName(u"icon_legend_layout")
        self.input_computed_legend_icon = QToolButton(self.raw_input_tab)
        self.input_computed_legend_icon.setObjectName(u"input_computed_legend_icon")
        self.input_computed_legend_icon.setStyleSheet(u"background: transparent;")
        icon1 = QIcon()
        icon1.addFile(u":/icons/kernel_ok.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.input_computed_legend_icon.setIcon(icon1)
        self.input_computed_legend_icon.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.icon_legend_layout.addWidget(self.input_computed_legend_icon)

        self.input_changed_legend_icon = QToolButton(self.raw_input_tab)
        self.input_changed_legend_icon.setObjectName(u"input_changed_legend_icon")
        self.input_changed_legend_icon.setStyleSheet(u"background: transparent;")
        icon2 = QIcon()
        icon2.addFile(u":/icons/kernel_warn.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.input_changed_legend_icon.setIcon(icon2)
        self.input_changed_legend_icon.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.icon_legend_layout.addWidget(self.input_changed_legend_icon)

        self.input_preview_limits_label = QLabel(self.raw_input_tab)
        self.input_preview_limits_label.setObjectName(u"input_preview_limits_label")
        font4 = QFont()
        font4.setPointSize(10)
        self.input_preview_limits_label.setFont(font4)
        self.input_preview_limits_label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.icon_legend_layout.addWidget(self.input_preview_limits_label)


        self.verticalLayout_6.addLayout(self.icon_legend_layout)

        self.line = QFrame(self.raw_input_tab)
        self.line.setObjectName(u"line")
        self.line.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_6.addWidget(self.line)

        self.kernel_settings_frame = QFrame(self.raw_input_tab)
        self.kernel_settings_frame.setObjectName(u"kernel_settings_frame")
        self.kernel_settings_layout = QHBoxLayout(self.kernel_settings_frame)
        self.kernel_settings_layout.setSpacing(2)
        self.kernel_settings_layout.setObjectName(u"kernel_settings_layout")
        self.kernel_settings_layout.setContentsMargins(5, 10, 5, 0)
        self.kernel_selection_layout = QGroupBox(self.kernel_settings_frame)
        self.kernel_selection_layout.setObjectName(u"kernel_selection_layout")
        self.kernel_selection_layout.setFont(font2)
        self.verticalLayout_2 = QVBoxLayout(self.kernel_selection_layout)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.kernel_method_layout = QHBoxLayout()
        self.kernel_method_layout.setObjectName(u"kernel_method_layout")
        self.rbf_kernel_btn = QPushButton(self.kernel_selection_layout)
        self.kernel_button_group = QButtonGroup(MainWindow)
        self.kernel_button_group.setObjectName(u"kernel_button_group")
        self.kernel_button_group.addButton(self.rbf_kernel_btn)
        self.rbf_kernel_btn.setObjectName(u"rbf_kernel_btn")
        font5 = QFont()
        font5.setBold(False)
        self.rbf_kernel_btn.setFont(font5)
        self.rbf_kernel_btn.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.rbf_kernel_btn.setCheckable(True)
        self.rbf_kernel_btn.setChecked(True)

        self.kernel_method_layout.addWidget(self.rbf_kernel_btn)

        self.poly_kernel_btn = QPushButton(self.kernel_selection_layout)
        self.kernel_button_group.addButton(self.poly_kernel_btn)
        self.poly_kernel_btn.setObjectName(u"poly_kernel_btn")
        self.poly_kernel_btn.setFont(font5)
        self.poly_kernel_btn.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.poly_kernel_btn.setCheckable(True)

        self.kernel_method_layout.addWidget(self.poly_kernel_btn)

        self.linear_kernel_btn = QPushButton(self.kernel_selection_layout)
        self.kernel_button_group.addButton(self.linear_kernel_btn)
        self.linear_kernel_btn.setObjectName(u"linear_kernel_btn")
        self.linear_kernel_btn.setFont(font5)
        self.linear_kernel_btn.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.linear_kernel_btn.setCheckable(True)

        self.kernel_method_layout.addWidget(self.linear_kernel_btn)


        self.verticalLayout_2.addLayout(self.kernel_method_layout)

        self.kernel_function_widget = QWidget(self.kernel_selection_layout)
        self.kernel_function_widget.setObjectName(u"kernel_function_widget")
        self.kernel_function_widget.setStyleSheet(u"background: gray; border-radius: 10px;")
        self.horizontalLayout = QHBoxLayout(self.kernel_function_widget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.kernel_function_preview = QToolButton(self.kernel_function_widget)
        self.kernel_function_preview.setObjectName(u"kernel_function_preview")
        self.kernel_function_preview.setEnabled(True)
        self.kernel_function_preview.setStyleSheet(u"background: transparent;")
        self.kernel_function_preview.setIconSize(QSize(220, 20))

        self.horizontalLayout.addWidget(self.kernel_function_preview)


        self.verticalLayout_2.addWidget(self.kernel_function_widget)


        self.kernel_settings_layout.addWidget(self.kernel_selection_layout)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.kernel_settings_layout.addItem(self.horizontalSpacer_2)

        self.kernel_params_layout = QGroupBox(self.kernel_settings_frame)
        self.kernel_params_layout.setObjectName(u"kernel_params_layout")
        self.kernel_params_layout.setFont(font2)
        self.kernel_params_layout.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.kernel_params_layout.setFlat(False)
        self.gridLayout = QGridLayout(self.kernel_params_layout)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(5)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.kernel_gamma_label = QLabel(self.kernel_params_layout)
        self.kernel_gamma_label.setObjectName(u"kernel_gamma_label")
        self.kernel_gamma_label.setFont(font5)
        self.kernel_gamma_label.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.kernel_gamma_label.setTextFormat(Qt.TextFormat.RichText)

        self.gridLayout.addWidget(self.kernel_gamma_label, 1, 0, 1, 1)

        self.default_cost_layout = QHBoxLayout()
        self.default_cost_layout.setObjectName(u"default_cost_layout")
        self.apply_default_cost_btn = QToolButton(self.kernel_params_layout)
        self.apply_default_cost_btn.setObjectName(u"apply_default_cost_btn")
        self.apply_default_cost_btn.setEnabled(False)
        self.apply_default_cost_btn.setFont(font5)
        self.apply_default_cost_btn.setStyleSheet(u"background: transparent;")
        self.apply_default_cost_btn.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        icon3 = QIcon()
        icon3.addFile(u":/icons/left_arrow.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.apply_default_cost_btn.setIcon(icon3)
        self.apply_default_cost_btn.setIconSize(QSize(16, 14))

        self.default_cost_layout.addWidget(self.apply_default_cost_btn)

        self.default_cost_value = QLabel(self.kernel_params_layout)
        self.default_cost_value.setObjectName(u"default_cost_value")
        self.default_cost_value.setEnabled(False)
        self.default_cost_value.setFont(font5)
        self.default_cost_value.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.default_cost_value.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.default_cost_layout.addWidget(self.default_cost_value)


        self.gridLayout.addLayout(self.default_cost_layout, 3, 2, 1, 1)

        self.selected_param_label = QLabel(self.kernel_params_layout)
        self.selected_param_label.setObjectName(u"selected_param_label")
        self.selected_param_label.setFont(font5)
        self.selected_param_label.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.selected_param_label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.selected_param_label, 0, 1, 1, 1)

        self.kernel_cost_edit = QLineEdit(self.kernel_params_layout)
        self.kernel_cost_edit.setObjectName(u"kernel_cost_edit")
        self.kernel_cost_edit.setEnabled(False)
        self.kernel_cost_edit.setFont(font5)
        self.kernel_cost_edit.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.kernel_cost_edit.setMaxLength(10)
        self.kernel_cost_edit.setFrame(False)
        self.kernel_cost_edit.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.kernel_cost_edit, 3, 1, 1, 1)

        self.kernel_degree_edit = QLineEdit(self.kernel_params_layout)
        self.kernel_degree_edit.setObjectName(u"kernel_degree_edit")
        self.kernel_degree_edit.setEnabled(False)
        self.kernel_degree_edit.setFont(font5)
        self.kernel_degree_edit.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.kernel_degree_edit.setMaxLength(10)
        self.kernel_degree_edit.setFrame(False)
        self.kernel_degree_edit.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.kernel_degree_edit, 2, 1, 1, 1)

        self.kernel_cost_label = QLabel(self.kernel_params_layout)
        self.kernel_cost_label.setObjectName(u"kernel_cost_label")
        self.kernel_cost_label.setEnabled(False)
        self.kernel_cost_label.setFont(font5)
        self.kernel_cost_label.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.kernel_cost_label.setTextFormat(Qt.TextFormat.RichText)

        self.gridLayout.addWidget(self.kernel_cost_label, 3, 0, 1, 1)

        self.default_gamma_layout = QHBoxLayout()
        self.default_gamma_layout.setObjectName(u"default_gamma_layout")
        self.apply_default_gamma_btn = QToolButton(self.kernel_params_layout)
        self.apply_default_gamma_btn.setObjectName(u"apply_default_gamma_btn")
        self.apply_default_gamma_btn.setFont(font5)
        self.apply_default_gamma_btn.setStyleSheet(u"background: transparent;")
        self.apply_default_gamma_btn.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.apply_default_gamma_btn.setIcon(icon3)
        self.apply_default_gamma_btn.setIconSize(QSize(16, 14))

        self.default_gamma_layout.addWidget(self.apply_default_gamma_btn)

        self.default_gamma_value = QLabel(self.kernel_params_layout)
        self.default_gamma_value.setObjectName(u"default_gamma_value")
        self.default_gamma_value.setFont(font5)
        self.default_gamma_value.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.default_gamma_value.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.default_gamma_layout.addWidget(self.default_gamma_value)


        self.gridLayout.addLayout(self.default_gamma_layout, 1, 2, 1, 1)

        self.default_param_label = QLabel(self.kernel_params_layout)
        self.default_param_label.setObjectName(u"default_param_label")
        self.default_param_label.setFont(font5)
        self.default_param_label.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.default_param_label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.default_param_label, 0, 2, 1, 1)

        self.kernel_degree_label = QLabel(self.kernel_params_layout)
        self.kernel_degree_label.setObjectName(u"kernel_degree_label")
        self.kernel_degree_label.setEnabled(False)
        self.kernel_degree_label.setFont(font5)
        self.kernel_degree_label.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))

        self.gridLayout.addWidget(self.kernel_degree_label, 2, 0, 1, 1)

        self.kernel_gamma_edit = QLineEdit(self.kernel_params_layout)
        self.kernel_gamma_edit.setObjectName(u"kernel_gamma_edit")
        self.kernel_gamma_edit.setFont(font5)
        self.kernel_gamma_edit.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.kernel_gamma_edit.setMaxLength(10)
        self.kernel_gamma_edit.setFrame(False)
        self.kernel_gamma_edit.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.kernel_gamma_edit.setClearButtonEnabled(False)

        self.gridLayout.addWidget(self.kernel_gamma_edit, 1, 1, 1, 1)

        self.default_degree_layout = QHBoxLayout()
        self.default_degree_layout.setObjectName(u"default_degree_layout")
        self.apply_default_degree_btn = QToolButton(self.kernel_params_layout)
        self.apply_default_degree_btn.setObjectName(u"apply_default_degree_btn")
        self.apply_default_degree_btn.setEnabled(False)
        self.apply_default_degree_btn.setFont(font5)
        self.apply_default_degree_btn.setStyleSheet(u"background: transparent;")
        self.apply_default_degree_btn.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.apply_default_degree_btn.setIcon(icon3)
        self.apply_default_degree_btn.setIconSize(QSize(16, 14))

        self.default_degree_layout.addWidget(self.apply_default_degree_btn)

        self.default_degree_value = QLabel(self.kernel_params_layout)
        self.default_degree_value.setObjectName(u"default_degree_value")
        self.default_degree_value.setEnabled(False)
        self.default_degree_value.setFont(font5)
        self.default_degree_value.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.default_degree_value.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.default_degree_layout.addWidget(self.default_degree_value)


        self.gridLayout.addLayout(self.default_degree_layout, 2, 2, 1, 1)

        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setColumnMinimumWidth(1, 1)
        self.gridLayout.setColumnMinimumWidth(2, 1)
        self.gridLayout.setRowMinimumHeight(0, 1)

        self.kernel_settings_layout.addWidget(self.kernel_params_layout)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.kernel_settings_layout.addItem(self.horizontalSpacer)

        self.kernel_settings_actions_layout = QVBoxLayout()
        self.kernel_settings_actions_layout.setSpacing(10)
        self.kernel_settings_actions_layout.setObjectName(u"kernel_settings_actions_layout")
        self.kernel_settings_sync_check = QCheckBox(self.kernel_settings_frame)
        self.kernel_settings_sync_check.setObjectName(u"kernel_settings_sync_check")

        self.kernel_settings_actions_layout.addWidget(self.kernel_settings_sync_check)

        self.apply_settings_globally_btn = QPushButton(self.kernel_settings_frame)
        self.apply_settings_globally_btn.setObjectName(u"apply_settings_globally_btn")
        self.apply_settings_globally_btn.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))

        self.kernel_settings_actions_layout.addWidget(self.apply_settings_globally_btn)

        self.line_2 = QFrame(self.kernel_settings_frame)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.kernel_settings_actions_layout.addWidget(self.line_2)

        self.compute_current_btn = QPushButton(self.kernel_settings_frame)
        self.compute_current_btn.setObjectName(u"compute_current_btn")

        self.kernel_settings_actions_layout.addWidget(self.compute_current_btn)

        self.compute_all_btn = QPushButton(self.kernel_settings_frame)
        self.compute_all_btn.setObjectName(u"compute_all_btn")
        self.compute_all_btn.setFont(font5)

        self.kernel_settings_actions_layout.addWidget(self.compute_all_btn)


        self.kernel_settings_layout.addLayout(self.kernel_settings_actions_layout)


        self.verticalLayout_6.addWidget(self.kernel_settings_frame)

        self.verticalLayout_6.setStretch(0, 1)
        self.tab_widget.addTab(self.raw_input_tab, "")
        self.processed_tab = QWidget()
        self.processed_tab.setObjectName(u"processed_tab")
        self.horizontalLayout_9 = QHBoxLayout(self.processed_tab)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.processed_kernels_layout = QVBoxLayout()
        self.processed_kernels_layout.setObjectName(u"processed_kernels_layout")
        self.processed_kernels_label = QLabel(self.processed_tab)
        self.processed_kernels_label.setObjectName(u"processed_kernels_label")
        self.processed_kernels_label.setFont(font2)

        self.processed_kernels_layout.addWidget(self.processed_kernels_label)

        self.processed_kernels_listwidget = QListWidget(self.processed_tab)
        self.processed_kernels_listwidget.setObjectName(u"processed_kernels_listwidget")
        self.processed_kernels_listwidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.processed_kernels_listwidget.setDefaultDropAction(Qt.DropAction.IgnoreAction)

        self.processed_kernels_layout.addWidget(self.processed_kernels_listwidget)


        self.horizontalLayout_9.addLayout(self.processed_kernels_layout)

        self.processed_vis_layout = QVBoxLayout()
        self.processed_vis_layout.setObjectName(u"processed_vis_layout")
        self.processed_preview_layout = QHBoxLayout()
        self.processed_preview_layout.setObjectName(u"processed_preview_layout")
        self.visualization_label = QLabel(self.processed_tab)
        self.visualization_label.setObjectName(u"visualization_label")
        self.visualization_label.setFont(font2)

        self.processed_preview_layout.addWidget(self.visualization_label)


        self.processed_vis_layout.addLayout(self.processed_preview_layout)

        self.processed_settings_layout = QGridLayout()
        self.processed_settings_layout.setObjectName(u"processed_settings_layout")
        self.proc_gamma_label = QLabel(self.processed_tab)
        self.proc_gamma_label.setObjectName(u"proc_gamma_label")
        self.proc_gamma_label.setEnabled(False)
        self.proc_gamma_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.processed_settings_layout.addWidget(self.proc_gamma_label, 0, 1, 1, 1)

        self.proc_degree_value = QLabel(self.processed_tab)
        self.proc_degree_value.setObjectName(u"proc_degree_value")
        self.proc_degree_value.setEnabled(False)
        self.proc_degree_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.processed_settings_layout.addWidget(self.proc_degree_value, 1, 2, 1, 1)

        self.proc_gamma_value = QLabel(self.processed_tab)
        self.proc_gamma_value.setObjectName(u"proc_gamma_value")
        self.proc_gamma_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.processed_settings_layout.addWidget(self.proc_gamma_value, 1, 1, 1, 1)

        self.proc_method_value = QLabel(self.processed_tab)
        self.proc_method_value.setObjectName(u"proc_method_value")
        self.proc_method_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.processed_settings_layout.addWidget(self.proc_method_value, 1, 0, 1, 1)

        self.proc_cost_label = QLabel(self.processed_tab)
        self.proc_cost_label.setObjectName(u"proc_cost_label")
        self.proc_cost_label.setEnabled(False)
        self.proc_cost_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.processed_settings_layout.addWidget(self.proc_cost_label, 0, 3, 1, 1)

        self.proc_method_label = QLabel(self.processed_tab)
        self.proc_method_label.setObjectName(u"proc_method_label")
        self.proc_method_label.setEnabled(False)
        self.proc_method_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.processed_settings_layout.addWidget(self.proc_method_label, 0, 0, 1, 1)

        self.proc_degree_label = QLabel(self.processed_tab)
        self.proc_degree_label.setObjectName(u"proc_degree_label")
        self.proc_degree_label.setEnabled(False)
        self.proc_degree_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.processed_settings_layout.addWidget(self.proc_degree_label, 0, 2, 1, 1)

        self.proc_cost_value = QLabel(self.processed_tab)
        self.proc_cost_value.setObjectName(u"proc_cost_value")
        self.proc_cost_value.setEnabled(False)
        self.proc_cost_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.processed_settings_layout.addWidget(self.proc_cost_value, 1, 3, 1, 1)


        self.processed_vis_layout.addLayout(self.processed_settings_layout)

        self.processed_export_layout = QHBoxLayout()
        self.processed_export_layout.setSpacing(10)
        self.processed_export_layout.setObjectName(u"processed_export_layout")
        self.processed_export_all_btn = QPushButton(self.processed_tab)
        self.processed_export_all_btn.setObjectName(u"processed_export_all_btn")

        self.processed_export_layout.addWidget(self.processed_export_all_btn)

        self.processed_export_current_btn = QPushButton(self.processed_tab)
        self.processed_export_current_btn.setObjectName(u"processed_export_current_btn")

        self.processed_export_layout.addWidget(self.processed_export_current_btn)

        self.processed_export_ids_btn = QPushButton(self.processed_tab)
        self.processed_export_ids_btn.setObjectName(u"processed_export_ids_btn")

        self.processed_export_layout.addWidget(self.processed_export_ids_btn)


        self.processed_vis_layout.addLayout(self.processed_export_layout)


        self.horizontalLayout_9.addLayout(self.processed_vis_layout)

        self.horizontalLayout_9.setStretch(0, 1)
        self.horizontalLayout_9.setStretch(1, 3)
        self.tab_widget.addTab(self.processed_tab, "")
        self.precomp_tab = QWidget()
        self.precomp_tab.setObjectName(u"precomp_tab")
        self.horizontalLayout_3 = QHBoxLayout(self.precomp_tab)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.precomp_kernels_layout = QVBoxLayout()
        self.precomp_kernels_layout.setObjectName(u"precomp_kernels_layout")
        self.precomp_input_layout = QHBoxLayout()
        self.precomp_input_layout.setObjectName(u"precomp_input_layout")
        self.precomp_kernels_label = QLabel(self.precomp_tab)
        self.precomp_kernels_label.setObjectName(u"precomp_kernels_label")
        self.precomp_kernels_label.setFont(font2)

        self.precomp_input_layout.addWidget(self.precomp_kernels_label)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.precomp_input_layout.addItem(self.horizontalSpacer_5)

        self.precomp_add_data_btn = QPushButton(self.precomp_tab)
        self.precomp_add_data_btn.setObjectName(u"precomp_add_data_btn")

        self.precomp_input_layout.addWidget(self.precomp_add_data_btn)


        self.precomp_kernels_layout.addLayout(self.precomp_input_layout)

        self.precomp_kernels_listwidget = QListWidget(self.precomp_tab)
        self.precomp_kernels_listwidget.setObjectName(u"precomp_kernels_listwidget")
        self.precomp_kernels_listwidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.precomp_kernels_listwidget.setDefaultDropAction(Qt.DropAction.IgnoreAction)

        self.precomp_kernels_layout.addWidget(self.precomp_kernels_listwidget)

        self.precomp_kernels_layout.setStretch(1, 1)

        self.horizontalLayout_3.addLayout(self.precomp_kernels_layout)

        self.precomp_vis_layout = QVBoxLayout()
        self.precomp_vis_layout.setObjectName(u"precomp_vis_layout")
        self.precomp_preview_layout = QHBoxLayout()
        self.precomp_preview_layout.setObjectName(u"precomp_preview_layout")
        self.precomp_visualization_label = QLabel(self.precomp_tab)
        self.precomp_visualization_label.setObjectName(u"precomp_visualization_label")
        self.precomp_visualization_label.setFont(font2)

        self.precomp_preview_layout.addWidget(self.precomp_visualization_label)


        self.precomp_vis_layout.addLayout(self.precomp_preview_layout)

        self.precomp_properties_layout = QGridLayout()
        self.precomp_properties_layout.setObjectName(u"precomp_properties_layout")
        self.precomp_sym_label = QLabel(self.precomp_tab)
        self.precomp_sym_label.setObjectName(u"precomp_sym_label")
        self.precomp_sym_label.setEnabled(True)
        self.precomp_sym_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.precomp_properties_layout.addWidget(self.precomp_sym_label, 0, 1, 1, 1)

        self.precomp_shape_label = QLabel(self.precomp_tab)
        self.precomp_shape_label.setObjectName(u"precomp_shape_label")
        self.precomp_shape_label.setEnabled(True)
        self.precomp_shape_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.precomp_properties_layout.addWidget(self.precomp_shape_label, 0, 0, 1, 1)

        self.precomp_psd_label = QLabel(self.precomp_tab)
        self.precomp_psd_label.setObjectName(u"precomp_psd_label")
        self.precomp_psd_label.setEnabled(True)
        self.precomp_psd_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.precomp_properties_layout.addWidget(self.precomp_psd_label, 0, 2, 1, 1)

        self.precomp_shape_value = QLabel(self.precomp_tab)
        self.precomp_shape_value.setObjectName(u"precomp_shape_value")
        self.precomp_shape_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.precomp_properties_layout.addWidget(self.precomp_shape_value, 1, 0, 1, 1)

        self.precomp_sym_layout = QHBoxLayout()
        self.precomp_sym_layout.setSpacing(0)
        self.precomp_sym_layout.setObjectName(u"precomp_sym_layout")
        self.precomp_not_sym_icon = QToolButton(self.precomp_tab)
        self.precomp_not_sym_icon.setObjectName(u"precomp_not_sym_icon")
        self.precomp_not_sym_icon.setStyleSheet(u"background: transparent;")
        icon4 = QIcon()
        icon4.addFile(u":/icons/warning.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.precomp_not_sym_icon.setIcon(icon4)
        self.precomp_not_sym_icon.setIconSize(QSize(20, 20))

        self.precomp_sym_layout.addWidget(self.precomp_not_sym_icon)

        self.precomp_is_sym_icon = QToolButton(self.precomp_tab)
        self.precomp_is_sym_icon.setObjectName(u"precomp_is_sym_icon")
        self.precomp_is_sym_icon.setStyleSheet(u"background: transparent;")
        icon5 = QIcon()
        icon5.addFile(u":/icons/okay.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.precomp_is_sym_icon.setIcon(icon5)
        self.precomp_is_sym_icon.setIconSize(QSize(20, 20))

        self.precomp_sym_layout.addWidget(self.precomp_is_sym_icon)


        self.precomp_properties_layout.addLayout(self.precomp_sym_layout, 1, 1, 1, 1)

        self.precomp_psd_layout = QHBoxLayout()
        self.precomp_psd_layout.setSpacing(0)
        self.precomp_psd_layout.setObjectName(u"precomp_psd_layout")
        self.precomp_not_psd_icon = QToolButton(self.precomp_tab)
        self.precomp_not_psd_icon.setObjectName(u"precomp_not_psd_icon")
        self.precomp_not_psd_icon.setStyleSheet(u"background: transparent;")
        self.precomp_not_psd_icon.setIcon(icon4)
        self.precomp_not_psd_icon.setIconSize(QSize(20, 20))

        self.precomp_psd_layout.addWidget(self.precomp_not_psd_icon)

        self.precomp_is_psd_icon = QToolButton(self.precomp_tab)
        self.precomp_is_psd_icon.setObjectName(u"precomp_is_psd_icon")
        self.precomp_is_psd_icon.setStyleSheet(u"background: transparent;")
        self.precomp_is_psd_icon.setIcon(icon5)
        self.precomp_is_psd_icon.setIconSize(QSize(20, 20))

        self.precomp_psd_layout.addWidget(self.precomp_is_psd_icon)


        self.precomp_properties_layout.addLayout(self.precomp_psd_layout, 1, 2, 1, 1)

        self.reg_kernel_matrix_btn = QPushButton(self.precomp_tab)
        self.reg_kernel_matrix_btn.setObjectName(u"reg_kernel_matrix_btn")

        self.precomp_properties_layout.addWidget(self.reg_kernel_matrix_btn, 2, 2, 1, 1)


        self.precomp_vis_layout.addLayout(self.precomp_properties_layout)

        self.precomp_export_layout = QHBoxLayout()
        self.precomp_export_layout.setSpacing(10)
        self.precomp_export_layout.setObjectName(u"precomp_export_layout")
        self.precomp_export_all_btn = QPushButton(self.precomp_tab)
        self.precomp_export_all_btn.setObjectName(u"precomp_export_all_btn")

        self.precomp_export_layout.addWidget(self.precomp_export_all_btn)

        self.precomp_export_current_btn = QPushButton(self.precomp_tab)
        self.precomp_export_current_btn.setObjectName(u"precomp_export_current_btn")

        self.precomp_export_layout.addWidget(self.precomp_export_current_btn)

        self.precomp_export_ids_btn = QPushButton(self.precomp_tab)
        self.precomp_export_ids_btn.setObjectName(u"precomp_export_ids_btn")

        self.precomp_export_layout.addWidget(self.precomp_export_ids_btn)


        self.precomp_vis_layout.addLayout(self.precomp_export_layout)


        self.horizontalLayout_3.addLayout(self.precomp_vis_layout)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 3)
        self.tab_widget.addTab(self.precomp_tab, "")

        self.verticalLayout.addWidget(self.tab_widget)

        self.progress_frame = QFrame(self.central_widget)
        self.progress_frame.setObjectName(u"progress_frame")
        self.progress_layout = QHBoxLayout(self.progress_frame)
        self.progress_layout.setSpacing(2)
        self.progress_layout.setObjectName(u"progress_layout")
        self.progress_layout.setContentsMargins(5, 2, 5, 10)
        self.progress_bar = QProgressBar(self.progress_frame)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.progress_bar.setValue(0)

        self.progress_layout.addWidget(self.progress_bar)

        self.progress_label = QLabel(self.progress_frame)
        self.progress_label.setObjectName(u"progress_label")
        self.progress_label.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.progress_layout.addWidget(self.progress_label)

        self.progress_layout.setStretch(0, 1)
        self.progress_layout.setStretch(1, 2)

        self.verticalLayout.addWidget(self.progress_frame)

        MainWindow.setCentralWidget(self.central_widget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 24))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuInfo = QMenu(self.menubar)
        self.menuInfo.setObjectName(u"menuInfo")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuInfo.menuAction())
        self.menuFile.addAction(self.action_add_data)
        self.menuFile.addAction(self.action_export_all)
        self.menuFile.addAction(self.action_export_current)
        self.menuFile.addAction(self.action_export_index)
        self.menuFile.addAction(self.action_export_all_csv)
        self.menuEdit.addAction(self.action_compute_all)
        self.menuEdit.addAction(self.action_compute_current)
        self.menuInfo.addAction(self.action_about)
        self.menuInfo.addAction(self.action_help)
        self.menuInfo.addAction(self.action_go_to_rmkl)

        self.retranslateUi(MainWindow)

        self.tab_widget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action_compute_all.setText(QCoreApplication.translate("MainWindow", u"Compute all", None))
        self.action_compute_current.setText(QCoreApplication.translate("MainWindow", u"Compute current", None))
        self.action_add_data.setText(QCoreApplication.translate("MainWindow", u"Add data", None))
        self.action_export_all.setText(QCoreApplication.translate("MainWindow", u"Export all", None))
        self.action_export_current.setText(QCoreApplication.translate("MainWindow", u"Export current kernel matrix", None))
        self.action_help.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.action_about.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.action_go_to_rmkl.setText(QCoreApplication.translate("MainWindow", u"Go to web-rMKL.org", None))
        self.action_export_all_csv.setText(QCoreApplication.translate("MainWindow", u"Export all matrices as CSV", None))
        self.action_export_index.setText(QCoreApplication.translate("MainWindow", u"Export sample index", None))
        self.start_icon.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.start_name_label.setText(QCoreApplication.translate("MainWindow", u"web-rMKL preprocessing", None))
        self.start_input_question_label.setText(QCoreApplication.translate("MainWindow", u"Please select the type of input data that you want to prepare for submission to web-rMKL.org", None))
        self.primary_info_text.setText(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"</style></head><body style=\" font-family:'.AppleSystemUIFont'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- Import primary data in CSV format</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- Compute kernel matrices</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- Export kernel matrices as MAT files</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- Ex"
                        "port sample IDs for web-rMKL</p></body></html>", None))
        self.precomp_info_text.setText(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"</style></head><body style=\" font-family:'.AppleSystemUIFont'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- Import precomputed kernels in CSV format</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- Validate kernel matrices</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- Export kernel matrices as MAT files</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px"
                        ";\">- Export sample IDs for web-rMKL</p></body></html>", None))
        self.start_version_label.setText(QCoreApplication.translate("MainWindow", u"version", None))
        self.start_help_button.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.input_selection_tab), QCoreApplication.translate("MainWindow", u"Input type selection", None))
        self.input_list_label.setText(QCoreApplication.translate("MainWindow", u"Imported data", None))
        self.raw_add_data_btn.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.input_preview_label.setText(QCoreApplication.translate("MainWindow", u"Preview", None))
        self.input_sample_count.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.input_samples_label.setText(QCoreApplication.translate("MainWindow", u"samples", None))
        self.input_feature_count.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.input_features_label.setText(QCoreApplication.translate("MainWindow", u"features", None))
        self.input_computed_legend_icon.setText(QCoreApplication.translate("MainWindow", u"computed", None))
        self.input_changed_legend_icon.setText(QCoreApplication.translate("MainWindow", u"settings changed", None))
        self.input_preview_limits_label.setText(QCoreApplication.translate("MainWindow", u"(first 50 x 50 entries shown)", None))
        self.kernel_selection_layout.setTitle(QCoreApplication.translate("MainWindow", u"Kernel method", None))
        self.rbf_kernel_btn.setText(QCoreApplication.translate("MainWindow", u"RBF", None))
        self.poly_kernel_btn.setText(QCoreApplication.translate("MainWindow", u"Polynomial", None))
        self.linear_kernel_btn.setText(QCoreApplication.translate("MainWindow", u"Linear", None))
        self.kernel_function_preview.setText("")
        self.kernel_params_layout.setTitle(QCoreApplication.translate("MainWindow", u"Kernel parameters", None))
        self.kernel_gamma_label.setText(QCoreApplication.translate("MainWindow", u"Gamma (&gamma;)", None))
        self.apply_default_cost_btn.setText(QCoreApplication.translate("MainWindow", u"<-", None))
        self.default_cost_value.setText("")
        self.selected_param_label.setText(QCoreApplication.translate("MainWindow", u"Selected", None))
        self.kernel_cost_edit.setText("")
        self.kernel_degree_edit.setText("")
        self.kernel_cost_label.setText(QCoreApplication.translate("MainWindow", u"Cost (c<sub>0</sub>)", None))
        self.apply_default_gamma_btn.setText(QCoreApplication.translate("MainWindow", u"<-", None))
        self.default_gamma_value.setText("")
        self.default_param_label.setText(QCoreApplication.translate("MainWindow", u"Default", None))
        self.kernel_degree_label.setText(QCoreApplication.translate("MainWindow", u"Degree (d)", None))
        self.kernel_gamma_edit.setText("")
        self.apply_default_degree_btn.setText(QCoreApplication.translate("MainWindow", u"<-", None))
        self.default_degree_value.setText("")
        self.kernel_settings_sync_check.setText(QCoreApplication.translate("MainWindow", u"Sync settings globally", None))
        self.apply_settings_globally_btn.setText(QCoreApplication.translate("MainWindow", u"Apply current settings globally", None))
        self.compute_current_btn.setText(QCoreApplication.translate("MainWindow", u"Compute current", None))
        self.compute_all_btn.setText(QCoreApplication.translate("MainWindow", u"Compute all", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.raw_input_tab), QCoreApplication.translate("MainWindow", u"Input data", None))
        self.processed_kernels_label.setText(QCoreApplication.translate("MainWindow", u"Processed kernels", None))
        self.visualization_label.setText(QCoreApplication.translate("MainWindow", u"Visualization", None))
        self.proc_gamma_label.setText(QCoreApplication.translate("MainWindow", u"Gamma", None))
        self.proc_degree_value.setText("")
        self.proc_gamma_value.setText("")
        self.proc_method_value.setText("")
        self.proc_cost_label.setText(QCoreApplication.translate("MainWindow", u"Cost", None))
        self.proc_method_label.setText(QCoreApplication.translate("MainWindow", u"Method", None))
        self.proc_degree_label.setText(QCoreApplication.translate("MainWindow", u"Degree", None))
        self.proc_cost_value.setText("")
        self.processed_export_all_btn.setText(QCoreApplication.translate("MainWindow", u"Export all", None))
        self.processed_export_current_btn.setText(QCoreApplication.translate("MainWindow", u"Export current", None))
        self.processed_export_ids_btn.setText(QCoreApplication.translate("MainWindow", u"Export sample index", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.processed_tab), QCoreApplication.translate("MainWindow", u"Preprocessed data", None))
        self.precomp_kernels_label.setText(QCoreApplication.translate("MainWindow", u"Precomputed kernels", None))
        self.precomp_add_data_btn.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.precomp_visualization_label.setText(QCoreApplication.translate("MainWindow", u"Visualization", None))
        self.precomp_sym_label.setText(QCoreApplication.translate("MainWindow", u"Symmetrical", None))
        self.precomp_shape_label.setText(QCoreApplication.translate("MainWindow", u"Shape", None))
        self.precomp_psd_label.setText(QCoreApplication.translate("MainWindow", u"Positive semi-definite", None))
        self.precomp_shape_value.setText("")
        self.precomp_not_sym_icon.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.precomp_is_sym_icon.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.precomp_not_psd_icon.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.precomp_is_psd_icon.setText(QCoreApplication.translate("MainWindow", u"...", None))
#if QT_CONFIG(tooltip)
        self.reg_kernel_matrix_btn.setToolTip(QCoreApplication.translate("MainWindow", u"Transform the matrix to make it positive semi-definite (may not always be possible)", None))
#endif // QT_CONFIG(tooltip)
        self.reg_kernel_matrix_btn.setText(QCoreApplication.translate("MainWindow", u"Make PSD", None))
        self.precomp_export_all_btn.setText(QCoreApplication.translate("MainWindow", u"Export all valid matrices", None))
        self.precomp_export_current_btn.setText(QCoreApplication.translate("MainWindow", u"Export current", None))
        self.precomp_export_ids_btn.setText(QCoreApplication.translate("MainWindow", u"Export sample index", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.precomp_tab), QCoreApplication.translate("MainWindow", u"Precomputed kernels", None))
        self.progress_label.setText("")
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuInfo.setTitle(QCoreApplication.translate("MainWindow", u"Info", None))
    # retranslateUi

