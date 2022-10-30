# -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/26
#  Name: service_info.py
#  Author: DoooReyn
#  Description: 服务信息
from conf.auto_increase_id import AutoIncreaseId


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


# ---------------------------------------- 全部 ----------------------------------------
AllService = ServiceInfo('all_service', '服务列表', '服务集合')
# ---------------------------------------- 插件 ----------------------------------------
MetaWatchDogService = ServiceInfo('MetaWatchDog', 'Meta文件监控', 'Cocos Creator Meta 文件监控')
# ---------------------------------------- 图片 ----------------------------------------
PngCompressorService = ServiceInfo('PngCompressor', 'PNG压缩', 'PNG批量压缩')
JpgCompressorService = ServiceInfo('JpgCompressor', 'JPG压缩', 'JPG批量压缩')

ImageSplitterService = ServiceInfo('ImageSplitter', '图像分割', '图片分割工具')
# - https://github.com/k4yt3x/video2x
LosslessUpscalerService = ServiceInfo('LosslessUpscaler', '无损放大', '无损放大工具')
# ---------------------------------------- 音频 ----------------------------------------
# - https://github.com/KrishnanSG/Audio-Compression
AudioCompressorService = ServiceInfo('AudioCompressor', '音频压缩', '音频压缩工具')
# - https://github.com/lamdav/AudioConverter
AudioConverterService = ServiceInfo('AudioConverter', '音频转换', '音频转换工具 ')
# ---------------------------------------- 娱乐 ----------------------------------------
# - https://github.com/HFrost0/bilix
# - https://github.com/Nemo2011/bilibili-api
BilibiliAnimateService = ServiceInfo('AudioCompressor', '音频压缩', '音频压缩工具')
# ---------------------------------------- 生活 ----------------------------------------
# - https://github.com/lincolnloop/python-qrcode
QrcodeService = ServiceInfo('Qrcode', '二维码生成', '二维码生成工具')

# 导出接口
services = (
    MetaWatchDogService, PngCompressorService, JpgCompressorService, ImageSplitterService, LosslessUpscalerService,
    AudioConverterService, AudioCompressorService,
    BilibiliAnimateService,
    QrcodeService
)

__all__ = [
    "services",
    "ServiceInfo",
    "AllService",
    "MetaWatchDogService", "PngCompressorService", "JpgCompressorService", "ImageSplitterService", "LosslessUpscalerService",
    "AudioConverterService", "AudioCompressorService",
    "BilibiliAnimateService",
    "QrcodeService"
]
