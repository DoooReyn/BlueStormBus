# -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/26
#  Name: service_info.py
#  Author: DoooReyn
#  Description: 服务信息


class AutoIncreaseId:
    def __init__(self):
        self._id = 0

    def get(self):
        self._id += 1
        return self._id


class ServiceInfo:
    ID = AutoIncreaseId()

    def __init__(self, key: str, title: str, tooltip: str, multi_allowed: bool = False):
        self.key = key
        self.title = title
        self.tooltip = tooltip
        self.multi_allowed = multi_allowed
        self.id = f'{key}_{ServiceInfo.ID.get()}'

    def __str__(self):
        return f"<{self.id}> [{self.key}] {self.title}"

    def __repr__(self):
        return self.__str__()


AllService = ServiceInfo('all_service', '服务列表', '服务集合')
MetaWatchDogService = ServiceInfo('MetaWatchDog', 'Meta文件监控', 'Cocos Creator Meta 文件监控')
PngCompressorService = ServiceInfo('PngCompressor', 'PNG压缩', 'PNG批量压缩 <Progress>')
JpgCompressorService = ServiceInfo('JpgCompressor', 'JPG压缩', 'JPG批量压缩 <Progress>')
ImageSplitterService = ServiceInfo('ImageSplitter', '图像分割', '图片分割工具 <Progress>')
