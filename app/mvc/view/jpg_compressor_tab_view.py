#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/11/2
#  Name: jpg_compressor_tab_view.py
#  Author: DoooReyn
#  Description:
from os import walk
from os.path import isdir, splitext, dirname, join
from typing import Optional

from PySide6.QtCore import QPoint, QSize
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget, QListWidgetItem, QMenu

from conf import JpgCompressorService, Paths
from helper import Gui
from mvc.base.base_tab_view import BaseTabView
from mvc.helper.compress_file_item import CompressFileItem
from mvc.helper.compress_file_status import CompressFileStatus
from mvc.helper.jpg_compress_thread import JpgCompressThread
from mvc.model.jpg_compressor_tab_model import JpgCompressorTabModel
from mvc.ui.jpg_compressor_tab_ui import JpgCompressorTabUI


class JpgCompressorTabView(BaseTabView):
    def __init__(self, parent: QWidget = None):
        super(JpgCompressorTabView, self).__init__(JpgCompressorService, parent)

        self._files = dict()
        self._thread: Optional[JpgCompressThread] = None
        self._ui = JpgCompressorTabUI()
        self._model = JpgCompressorTabModel()
        self._model.inited.connect(self.onInited)
        self._model.sync()

    def onInited(self):
        self.setupUi()
        self.setupSignals()

    def setupUi(self):
        self.setLayout(self._ui.layout)
        self._ui.edit_output.setText(self._model.output)
        self._ui.spin_quality.setValue(self._model.quality)
        self._ui.slider_quality.setValue(self._model.quality)
        self._ui.check_strip.setChecked(self._model.strip)
        self._ui.check_clean.setChecked(self._model.clean)

    def setupSignals(self):
        self._ui.spin_quality.valueChanged.connect(self.onSpinQualityValueChanged)
        self._ui.slider_quality.valueChanged.connect(self.onSliderQualityValueChanged)
        self._ui.check_strip.stateChanged.connect(self.onStripStateChanged)
        self._ui.check_clean.stateChanged.connect(self.onCleanStateChanged)
        self._ui.edit_output.textChanged.connect(self.onOutputDirChanged)
        self._ui.btn_start.clicked.connect(self.run)
        self._ui.btn_output.clicked.connect(self.onSelectOutputDir)
        self._ui.btn_clear.clicked.connect(self.onClearFiles)
        self._ui.btn_add_dir.clicked.connect(self.onPickFilesFromDir)
        self._ui.btn_add_files.clicked.connect(self.onPickFilesFromFiles)
        self._ui.list_files.customContextMenuRequested.connect(self.onFileListContextMenuRequested)

    def onFileListContextMenuRequested(self, pos: QPoint):
        """文件列表右键菜单"""

        if self.running:
            # 运行中禁用右键菜单
            return

        # 打开源图像
        pop_menu = QMenu()
        act_open_src = QAction('打开源图像', self._ui.list_files)
        act_open_src.triggered.connect(self.onOpenFiles)
        pop_menu.addAction(act_open_src)

        # 打开源图像和目标图像
        if len(self._ui.list_files.selectedItems()) == 1:
            item = self.getCurrentFileItem()
            if item.compressed:
                act_open_dst = QAction('打开源图像和目标图像', self._ui.list_files)
                act_open_dst.triggered.connect(self.onCompareFile)
                pop_menu.addAction(act_open_dst)

        # 移除
        act_del = QAction('移除', self._ui.list_files)
        act_del.triggered.connect(self.onRemoveFiles)
        pop_menu.addAction(act_del)

        # 显示右键菜单
        pop_menu.exec_(self._ui.list_files.mapToGlobal(pos))

    def onOpenFiles(self):
        for item in self._ui.list_files.selectedItems():
            w = self.getFileItemByFileListItem(item)
            Gui.openExternalUrl(Paths.fromLocalFile(w.src_at))

    def onRemoveFiles(self):
        for item in self._ui.list_files.selectedItems():
            self.removeFileListItem(item)

    def onCompareFile(self):
        item = self.getCurrentFileItem()
        if item is not None:
            Gui.openExternalUrl(Paths.fromLocalFile(item.src_at))
            Gui.openExternalUrl(Paths.fromLocalFile(item.dst_at))

    def onClearFiles(self):
        self._files.clear()
        self._ui.list_files.clear()

    def onPickFilesFromDir(self):
        where = Gui.pickDirectory('选取文件所在目录', Paths.documentAt(), self)
        if where and isdir(where):
            for root, dirs, files in walk(where):
                for f in files:
                    name, ext = splitext(f)
                    if ext.lower() in ('.jpeg', '.jpg'):
                        filepath = join(root, f)
                        self.appendFileListItem(where, filepath)

    def onPickFilesFromFiles(self):
        files, filters = Gui.pickFiles('选取文件', Paths.documentAt(), '图像(*.jpg *jpeg)', True, self)
        if len(files) > 0:
            [self.appendFileListItem(dirname(f), f) for f in files]

    def onSelectOutputDir(self):
        where = Gui.pickDirectory('选取输出目录', self._model.output, self)
        if where and isdir(where):
            where = Paths.toLocalFile(where)
            self._ui.edit_output.setText(where)

    def appendFileListItem(self, src_dir_at: str, src_file_at: str):
        src_file_at = Paths.toLocalFile(src_file_at)
        if src_file_at not in self._files:
            file_status = self._files[src_file_at] = CompressFileStatus(src_dir_at, src_file_at)
            file_item = CompressFileItem(file_status)
            item = QListWidgetItem(self._ui.list_files)
            item.setSizeHint(QSize(0, 36))
            self._ui.list_files.setItemWidget(item, file_item)
            self._ui.list_files.addItem(item)

    def onOutputDirChanged(self):
        self._model.output = Paths.toLocalFile(self._ui.edit_output.text())
        print(self._model.output)

    def onSpinQualityValueChanged(self):
        self._model.quality = self._ui.spin_quality.value()
        self._ui.slider_quality.setValue(self._model.quality)

    def onSliderQualityValueChanged(self):
        self._model.quality = self._ui.slider_quality.value()
        self._ui.spin_quality.setValue(self._model.quality)

    def onStripStateChanged(self):
        self._model.strip = self._ui.check_strip.isChecked()

    def onCleanStateChanged(self):
        self._model.clean = self._ui.check_clean.isChecked()

    def getFileItemByFileListItem(self, item: QListWidgetItem) -> CompressFileItem:
        return self._ui.list_files.itemWidget(item)

    def getFileItemByRow(self, row: int) -> Optional[CompressFileItem]:
        item = self._ui.list_files.item(row)
        if item:
            return self.getFileItemByFileListItem(item)

    def getCurrentFileItem(self) -> Optional[CompressFileItem]:
        row = self._ui.list_files.currentRow()
        if row >= 0:
            return self.getFileItemByRow(row)

    def removeFileListItem(self, item: QListWidgetItem):
        w = self.getFileItemByFileListItem(item)
        del self._files[w.src_at]
        self._ui.list_files.takeItem(self._ui.list_files.row(item))

    def getAllListFileItems(self):
        file_items = []
        for i in range(self._ui.list_files.count()):
            file_items.append(self.getFileItemByRow(i))
        return file_items

    def canQuit(self):
        return not self.running

    def run(self):
        if not self._model.output:
            return Gui.popup('提示', '未选取输出目录', parent=self)

        if self._ui.list_files.count() <= 0:
            return Gui.popup('提示', '未选取文件', parent=self)

        super(JpgCompressorTabView, self).run()
        self._ui.setStatefulWidgetsEnabled(False)
        self._thread = JpgCompressThread(0.1,
                                         self._model.output,
                                         self._model.clean,
                                         self._model.strip,
                                         self._model.quality,
                                         self.getAllListFileItems(),
                                         on_complete=self.stop)
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        if self._thread is not None:
            self._thread.stop()
            self._thread = None
        self._ui.setStatefulWidgetsEnabled(True)
        super(JpgCompressorTabView, self).stop()

    def onSave(self):
        self._model.save()
