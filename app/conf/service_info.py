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
PngCompressorService = ServiceInfo('PngCompressor', 'PNG压缩', 'PNG图片批量压缩')
JpgCompressorService = ServiceInfo('JpgCompressor', 'JPG压缩', 'JPG图片批量压缩')
ImageTinifyService = ServiceInfo('ImageTinify', 'TinyPNG图片压缩', 'TinyPNG图片压缩')
ImageSplitterService = ServiceInfo('ImageSplitter', '图像分割', '图片分割工具')
TextureUnpackerService = ServiceInfo('TextureUnpacker', 'TexturePacker 拆图', 'TexturePacker 图集拆图工具')
SpineAtlasUnpackerService = ServiceInfo('SpineAtlasUnpacker', 'Spine Atlas 拆图', 'Spine骨骼动画图集拆图工具')
# - https://github.com/k4yt3x/video2x
LosslessUpscalerService = ServiceInfo('LosslessUpscaler', '无损放大', '无损放大工具')
# ---------------------------------------- 音频 ----------------------------------------
# - https://github.com/KrishnanSG/Audio-Compression
AudioCompressorService = ServiceInfo('AudioCompressor', '音频压缩', '音频压缩工具')
# - https://github.com/lamdav/AudioConverter
AudioConverterService = ServiceInfo('AudioConverter', '音频转换', '音频转换工具 ')
# ---------------------------------------- 生活 ----------------------------------------
# - 密码管理
PasswordMasterService = ServiceInfo('PasswordMaster', '密码管理器', '密码管理器：生成、存储、查找')
# - https://github.com/HFrost0/bilix
# - https://github.com/Nemo2011/bilibili-api
BilibiliAnimateService = ServiceInfo('BilibiliAnimate', 'B站追番提示', '小破站追番提示工具')
# - https://github.com/HFrost0/bilix
BilibiliDownloaderService = ServiceInfo('BilibiliDownloader', 'B站视频下载', '小破站视频下载工具')
# - https://github.com/suifengtec/subtitle-translator
SubtitleTranslatorService = ServiceInfo('SubtitleTranslator', '字幕翻译', '字幕翻译软件，翻译功能由谷歌翻译实现')
# - https://github.com/lincolnloop/python-qrcode
QrcodeService = ServiceInfo('Qrcode', '二维码生成', '二维码生成工具')
# - https://github.com/fandesfyf/JamTools
LANTransmitService = ServiceInfo('LANTransmit', '局域网文件传输', '局域网文件传输')
# - https://github.com/lturing/tacotronv2_wavernn_chinese
Text2SpeechService = ServiceInfo('Text2Speech', '文字转语音', '文字转语音')
# - https://github.com/PantsuDango/Dango-Translator
OcrTranslatorService = ServiceInfo('OcrTranslator', 'OCR翻译', 'OCR翻译')
# - 新华字典 https://github.com/pwxcoo/chinese-xinhua
XinHuaZiDianService = ServiceInfo('XinHuaZiDian', '新华字典', '📙 中华新华字典数据库。包括歇后语，成语，词语，汉字。')
# - 汉字转拼音 https://github.com/mozillazg/python-pinyin
PinyinService = ServiceInfo('Pinyin', '汉字转拼音', '汉字转拼音')
# - 壁纸
UnsplashWallpaperService = ServiceInfo('UnsplashWallpaper', 'Unsplash 随机壁纸', 'Unsplash 随机壁纸')
# - 闹钟
AlarmClockService = ServiceInfo('AlarmClock', '闹钟', '自定义闹钟')

# 导出接口
services = (
    MetaWatchDogService,
    PngCompressorService,
    JpgCompressorService,
    ImageSplitterService,
    TextureUnpackerService,
    SpineAtlasUnpackerService,
    LosslessUpscalerService,
    AudioConverterService,
    AudioCompressorService,
    PasswordMasterService,
    BilibiliAnimateService,
    BilibiliDownloaderService,
    SubtitleTranslatorService,
    QrcodeService,
    LANTransmitService,
    Text2SpeechService,
    OcrTranslatorService,
    XinHuaZiDianService,
    PinyinService,
    UnsplashWallpaperService,
    AlarmClockService,
)
