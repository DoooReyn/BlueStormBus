#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/30
#  Name: image_splitter_tab_model.py
#  Author: DoooReyn
#  Description:
from mvc.base.base_model import BaseModel


class ImageSplitterTabModel(BaseModel):
    def __init__(self):
        super(ImageSplitterTabModel, self).__init__()

        self.identifier = 'image_splitter'
        self._image_src_at = ''
        self._image_dst_at = ''

    @property
    def imageSrcAt(self):
        return self._image_src_at

    @imageSrcAt.setter
    def imageSrcAt(self, at):
        self._image_src_at = at

    @property
    def imageDstAt(self):
        return self._image_dst_at

    @imageDstAt.setter
    def imageDstAt(self, at):
        self._image_dst_at = at

    def format(self):
        return dict(
            identifier=self.identifier,
            image_src_at=self._image_src_at,
            image_dst_at=self._image_dst_at
        )
