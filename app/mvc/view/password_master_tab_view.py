#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/11/2
#  Name: password_master_tab_view.py
#  Author: DoooReyn
#  Description:
from PySide6.QtWidgets import QWidget

from conf import PasswordMasterService
from helper import Gui
from mvc.base.base_tab_view import BaseTabView
from mvc.helper.password_generator import PasswordGenerator
from mvc.model.password_master_tab_model import PasswordMasterTabModel
from mvc.ui.password_master_tab_ui import PasswordMasterTabUI


class PasswordMasterTabView(BaseTabView):
    def __init__(self, parent: QWidget = None):
        super(PasswordMasterTabView, self).__init__(PasswordMasterService, parent)

        self._ui = PasswordMasterTabUI()
        self._model = PasswordMasterTabModel()
        self._model.inited.connect(self.onInited)
        self._model.sync()

    def onInited(self):
        self.setupUi()
        self.setupSignals()

    def setupUi(self):
        self.setLayout(self._ui.layout)
        if self._model.hasMaster():
            self._ui.showCheckPasswordPanel()
        else:
            self._ui.showInputPasswordPanel()

    def setupSignals(self):
        self._ui.edit_input_password.returnPressed.connect(self.onCheckMasterWhenCreate)
        self._ui.edit_check_password.returnPressed.connect(self.onCheckMasterWhenOperates)
        self._ui.edit_create_password.textChanged.connect(self.onPasswordChanged)
        self._ui.btn_create_password.clicked.connect(self.onGeneratePassword)
        self._ui.btn_copy_password.clicked.connect(self.onCopyPassword)
        self._ui.btn_add_password.clicked.connect(self.onAddPassword)

    def onPasswordChanged(self):
        has = not not self._ui.edit_create_password.text()
        self._ui.btn_add_password.setEnabled(has)
        self._ui.btn_copy_password.setEnabled(has)

    def uppers(self):
        return self._ui.spin_upper.value()

    def lowers(self):
        return self._ui.spin_lower.value()

    def numbers(self):
        return self._ui.spin_number.value()

    def specials(self):
        return self._ui.spin_special.value()

    def password(self):
        return self._ui.edit_create_password.text()

    def onGeneratePassword(self):
        u, l, n, s = self.uppers(), self.lowers(), self.numbers(), self.specials()
        if u + l + n + s < 6:
            return Gui.popup('提示', '密码长度不得少于6位数', self)
        password = PasswordGenerator.generateEveryInLength(u, l, n, s)
        self._ui.edit_create_password.setText(password)

    def onCopyPassword(self):
        self._ui.edit_create_password.copy()

    def onAddPassword(self):
        comment = self._ui.edit_create_comment.text()
        if len(comment) == 0:
            return Gui.popup('提示', '请为密码提供备注说明', self)
        if self._model.hasPassword(comment):
            return Gui.popup('提示', '已存在相同的备注说明', self)
        self._model.addPassword(comment, self.password())

    def onCheckMasterWhenCreate(self):
        self._model.setMasterPassword(self._ui.edit_input_password.text())
        self._model.save()
        self._ui.showMainPasswordPanel()
        self.reloadTable()

    def onCheckMasterWhenOperates(self):
        if self._model.isValidMaster(self._ui.edit_check_password.text()):
            self._ui.showMainPasswordPanel()
            self.reloadTable()
        else:
            self._ui.edit_check_password.clear()
            self._ui.edit_check_password.setPlaceholderText('密码错误，请重新输入')

    def reloadTable(self):
        # TODO 自动加载数据源
        pass

    def canQuit(self):
        return True

    def onSave(self):
        self._model.save()
