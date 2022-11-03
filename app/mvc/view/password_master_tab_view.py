#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/11/2
#  Name: password_master_tab_view.py
#  Author: DoooReyn
#  Description:
from os.path import isfile

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QWidget, QTableWidgetItem

from conf import PasswordMasterService, Paths
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
        self._ui.btn_import.clicked.connect(self.onImportPassword)
        self._ui.tbl_passwords.itemChanged.connect(self.onTableItemEditTriggered)
        # self._ui.tbl_passwords.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def onImportPassword(self):
        where, filters = Gui.pickFiles("选取密码文件", Paths.documentAt(), '密码文件(*.csv)', False, self)
        if isfile(where):
            with open(where, 'r', encoding='utf-8') as f:
                for row, line in enumerate(f.readlines()):
                    params = line.split(',')
                    if row == 0:
                        continue
                    if len(params) < 3:
                        continue
                    comment, account, password = params[-3:]
                    self._model.add(account, comment, password)
            self.reloadTable(True)

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

    def keyReleaseEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Delete and self.focusWidget() == self._ui.tbl_passwords:
            self.onRemovePassword()
        super(PasswordMasterTabView, self).keyReleaseEvent(event)

    def onGeneratePassword(self):
        u, l, n, s = self.uppers(), self.lowers(), self.numbers(), self.specials()
        if u + l + n + s < 6:
            return Gui.popup('提示', '密码长度不得少于6位数', self)
        password = PasswordGenerator.generateEveryInLength(u, l, n, s)
        self._ui.edit_create_password.setText(password)

    def onCopyPassword(self):
        self._ui.edit_create_password.selectAll()
        self._ui.edit_create_password.copy()
        self._ui.edit_create_password.deselect()

    def onAddPassword(self):
        if len(self._ui.edit_create_account.text()) == 0:
            return Gui.popup('提示', '请提供账户信息', self)
        if len(self._ui.edit_create_comment.text()) == 0:
            return Gui.popup('提示', '请提供备注说明', self)
        self._addPassword()

    def onRemovePassword(self):
        row = self._ui.tbl_passwords.currentRow()
        self._ui.tbl_passwords.removeRow(row)
        self._model.remove(row)

    def _addPassword(self):
        account = self._ui.edit_create_account.text()
        comment = self._ui.edit_create_comment.text()
        password = self._ui.edit_create_password.text()
        self._ui.clearnEdits()
        self._model.add(account, comment, password)
        row = self._ui.tbl_passwords.rowCount()
        self._ui.tbl_passwords.insertRow(row)
        account_item = QTableWidgetItem(account)
        comment_item = QTableWidgetItem(comment)
        password_item = QTableWidgetItem(password)
        account_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        comment_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter)
        password_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self._ui.tbl_passwords.setItem(row, 0, account_item)
        self._ui.tbl_passwords.setItem(row, 1, comment_item)
        self._ui.tbl_passwords.setItem(row, 2, password_item)
        self._ui.tbl_passwords.verticalScrollBar().setSliderPosition(row)

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

    def onTableItemEditTriggered(self):
        item = self._ui.tbl_passwords.currentItem()
        if item is not None:
            row = item.row()
            account_dst = self._ui.tbl_passwords.item(row, 0).text()
            comment_dst = self._ui.tbl_passwords.item(row, 1).text()
            password_dst = self._ui.tbl_passwords.item(row, 2).text()
            self._model.set(row, account_dst, comment_dst, password_dst)

    def reloadTable(self, force: bool = False):
        if force or self._ui.tbl_passwords.rowCount() == 0:
            self._model.arrange()
            self._ui.tbl_passwords.clearContents()
            self._ui.tbl_passwords.setColumnCount(3)
            self._ui.tbl_passwords.setHorizontalHeaderLabels(['账户', '备注', '密码'])
            row = -1
            for row_info in self._model.passwords():
                if len(row_info) < 3:
                    continue
                row += 1
                self._ui.tbl_passwords.insertRow(row)
                account, comment, password = row_info
                account_decoded, comment_decoded, password_decoded = self._model.restore(account, comment, password)
                account_item = QTableWidgetItem(account_decoded)
                comment_item = QTableWidgetItem(comment_decoded)
                password_item = QTableWidgetItem(password_decoded)
                account_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                comment_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter)
                password_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self._ui.tbl_passwords.setItem(row, 0, account_item)
                self._ui.tbl_passwords.setItem(row, 1, comment_item)
                self._ui.tbl_passwords.setItem(row, 2, password_item)

    def canQuit(self):
        return True

    def onSave(self):
        self._model.save()

    def onHide(self):
        self._ui.showCheckPasswordPanel()
        self.onSave()

    def onFocusExit(self):
        self.onHide()

    def onExit(self):
        self.onHide()
