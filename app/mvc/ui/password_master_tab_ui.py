#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/11/2
#  Name: password_master_tab_ui.py
#  Author: DoooReyn
#  Description:
from PySide6.QtCore import Qt
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QSpinBox, QPushButton, QTableWidget, QGridLayout, \
    QWidget

from mvc.helper.password_generator import PasswordGenerator


class PasswordMasterTabUI(object):
    class Panels:
        InputPassword = 0
        CheckPassword = 1
        MainPassword = 2

    def __init__(self):
        password_validator = QRegularExpressionValidator('[a-zA-Z0-9]+$')
        self.panel_input_password = QWidget()
        self.lab_input_password = QLabel('你尚未创建密码库，请输入主密码以创建:')
        self.edit_input_password = QLineEdit('')
        self.edit_input_password.setValidator(password_validator)
        self.edit_input_password.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)
        self.layout_input_password = QVBoxLayout()
        self.layout_input_password.addWidget(self.lab_input_password)
        self.layout_input_password.addWidget(self.edit_input_password)
        self.layout_input_password.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.panel_input_password.setLayout(self.layout_input_password)

        self.panel_check_password = QWidget()
        self.lab_check_password = QLabel('该操作需要验证主密码:')
        self.edit_check_password = QLineEdit('')
        self.edit_check_password.setValidator(password_validator)
        self.edit_check_password.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)
        self.layout_check_password = QVBoxLayout()
        self.layout_check_password.addWidget(self.lab_check_password)
        self.layout_check_password.addWidget(self.edit_check_password)
        self.layout_check_password.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.panel_check_password.setLayout(self.layout_check_password)

        self.panel_main_password = QWidget()
        self.lab_lower = QLabel('小写')
        self.lab_upper = QLabel('大写')
        self.lab_number = QLabel('数字')
        self.lab_special = QLabel(f'特殊字符 {PasswordGenerator.specials}')
        self.spin_lower = QSpinBox()
        self.spin_upper = QSpinBox()
        self.spin_number = QSpinBox()
        self.spin_special = QSpinBox()
        self.spin_lower.setValue(4)
        self.spin_upper.setValue(4)
        self.spin_number.setValue(4)
        self.spin_special.setValue(4)
        self.spin_lower.setRange(0, 25)
        self.spin_upper.setRange(0, 25)
        self.spin_number.setRange(0, 25)
        self.spin_special.setRange(0, 25)
        self.lab_create_comment = QLabel('备注')
        self.edit_create_comment = QLineEdit('')
        self.lab_create_password = QLabel('密码')
        self.edit_create_password = QLineEdit('')
        self.edit_create_password.setReadOnly(True)
        self.edit_create_password.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.btn_create_password = QPushButton('生成')
        self.btn_copy_password = QPushButton('复制')
        self.btn_add_password = QPushButton('保存')
        self.lab_passwords = QLabel('密码本')
        self.tbl_passwords = QTableWidget()
        self.layout_main_password = QGridLayout()
        self.layout_main_password.addWidget(self.lab_lower, 0, 0, 1, 1)
        self.layout_main_password.addWidget(self.spin_lower, 0, 1, 1, 1)
        self.layout_main_password.addWidget(self.lab_upper, 0, 2, 1, 1)
        self.layout_main_password.addWidget(self.spin_upper, 0, 3, 1, 1)
        self.layout_main_password.addWidget(self.lab_number, 0, 4, 1, 1)
        self.layout_main_password.addWidget(self.spin_number, 0, 5, 1, 1)
        self.layout_main_password.addWidget(self.lab_special, 0, 6, 1, 1)
        self.layout_main_password.addWidget(self.spin_special, 0, 7, 1, 1)
        self.layout_main_password.addWidget(self.lab_create_password, 1, 0, 1, 1)
        self.layout_main_password.addWidget(self.edit_create_password, 1, 1, 1, 8)
        self.layout_main_password.addWidget(self.btn_create_password, 1, 9, 1, 1)
        self.layout_main_password.addWidget(self.btn_copy_password, 1, 10, 1, 1)
        self.layout_main_password.addWidget(self.btn_add_password, 1, 11, 1, 1)
        self.layout_main_password.addWidget(self.lab_create_comment, 2, 0, 1, 1)
        self.layout_main_password.addWidget(self.edit_create_comment, 2, 1, 1, 11)
        self.layout_main_password.addWidget(self.lab_passwords, 3, 0, 1, 1)
        self.layout_main_password.addWidget(self.tbl_passwords, 4, 0, 1, 12)
        self.panel_main_password.setLayout(self.layout_main_password)
        self.layout_main_password.setColumnStretch(8, 1)
        self.layout_main_password.setRowStretch(4, 1)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.panel_input_password)
        self.layout.addWidget(self.panel_check_password)
        self.layout.addWidget(self.panel_main_password)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.panels = (self.panel_input_password, self.panel_check_password, self.panel_main_password,)

    def showInputPasswordPanel(self):
        self.showPanel(PasswordMasterTabUI.Panels.InputPassword)

    def showCheckPasswordPanel(self):
        self.showPanel(PasswordMasterTabUI.Panels.CheckPassword)

    def showMainPasswordPanel(self):
        self.showPanel(PasswordMasterTabUI.Panels.MainPassword)

    def showPanel(self, panel_code: int):
        for index, panel in enumerate(self.panels):
            panel.setVisible(panel_code == index)
