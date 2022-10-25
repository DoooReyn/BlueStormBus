# -*- coding: utf-8 -*-

"""
@File    : Rcc.py
@Date    : 2022/9/27 11:47
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : qrc资源文件生成及映射工具
  - 输出文件：
    - ./resources.qrc
    - {project_dir}/app/conf/resources.py
    - {project_dir}/app/conf/res_map.py
"""

from os import listdir, sep, walk
from os.path import basename, dirname, isdir, isfile, join, relpath, splitext
from subprocess import Popen


class Config:
    """
    配置

    - 规范和约定
        - 资源名称分隔符使用下划线，例如： icon_app.ico, icon_help.svg
        - 资源前缀只会采用一级目录名称，后续将全部展平到一级目录下
    """

    # 当前目录
    PROGRAM_AT = dirname(__file__)

    # 资源目录
    RESOURCES_AT = join(PROGRAM_AT, '..', '..', 'resources')

    # qrc文件
    QRC_RAW_AT = join(PROGRAM_AT, 'resources.qrc')
    QRC_PY_AT = join(PROGRAM_AT, '..', '..', 'app', 'conf', 'resources.py')

    # 资源映射文件
    RES_MAP_AT = join(PROGRAM_AT, '..', '..', 'app', 'conf', 'res_map.py')

    # 文件编码
    ENCODING = 'utf-8'


class Qrc:
    """ qrc文件生成及映射工具 """

    def __init__(self):
        self._lines = []
        self._map = []

    def _appendLine(self, line: str):
        self._lines.append(line)

    def open(self):
        self._appendLine('<!DOCTYPE RCC>')
        self._appendLine('<RCC version="1.0">')
        self._map.append('class ResMap:')

    def openPrefix(self, prefix: str = None):
        if prefix is not None:
            self._appendLine('    <qresource prefix="%s">' % prefix.upper())
        else:
            self._appendLine('    <qresource>')

    def appendFile(self, prefix: str, file_path: str):
        file_alias = splitext(basename(file_path))[0].replace('-', '_', -1).upper()
        self._appendLine('        <file alias="%s">%s</file>' % (file_alias, file_path))
        if prefix == '':
            self._map.append('    %s = ":%s"' % (file_alias, '/'.join([file_alias])))
        else:
            self._map.append('    %s_%s = ":%s"' % (prefix, file_alias, '/'.join([prefix, file_alias])))

    def closePrefix(self):
        self._appendLine('    </qresource>')

    def close(self):
        self._appendLine('</RCC>')
        self.qrc()
        self.map()

    def qrc(self):
        self.saveAs(Config.QRC_RAW_AT, '\n'.join(self._lines) + '\n')

    def map(self):
        self.saveAs(Config.RES_MAP_AT, '\n'.join(self._map) + '\n')

    @staticmethod
    def saveAs(where: str, content: str):
        with open(where, 'w', encoding=Config.ENCODING) as sf:
            sf.write(content)

    @staticmethod
    def formatRes(where: str):
        return relpath(where, Config.PROGRAM_AT).replace(sep, '/')


if __name__ == '__main__':
    root = Config.RESOURCES_AT
    rel = join('..', root)
    plain_files = []

    # 生成 qrc、资源映射 文件
    qrc = Qrc()
    qrc.open()

    for entry in listdir(root):
        file_at = join(root, entry)
        if isdir(file_at):
            # 添加二级资源
            qrc.openPrefix(entry.upper())
            for sub, dirs, files in walk(file_at):
                for sub_entry in files:
                    qrc.appendFile(entry.upper(), qrc.formatRes(join(sub, sub_entry)))
            qrc.closePrefix()
        elif isfile(file_at):
            # 缓存一级资源，等待二级资源完成后再添加
            plain_files.append(file_at)

    if len(plain_files) > 0:
        # 添加一级资源
        qrc.openPrefix()
        [qrc.appendFile('', qrc.formatRes(p)) for p in plain_files]
        qrc.closePrefix()

    qrc.close()

    # qrc 转 py
    with open(Config.QRC_PY_AT, 'w', encoding=Config.ENCODING):
        cmd = 'pyside6-rcc %s -o %s' % (Config.QRC_RAW_AT, Config.QRC_PY_AT)
        Popen(cmd, cwd=Config.PROGRAM_AT)
        print('Done!')
