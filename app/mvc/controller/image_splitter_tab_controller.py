#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/30
#  Name: image_splitter_tab_controller.py
#  Author: DoooReyn
#  Description:
from mvc.base.base_controller import BaseController
from mvc.model.image_splitter_tab_model import ImageSplitterTabModel


class ImageSplitterTabController(BaseController):
    def __init__(self, model: ImageSplitterTabModel):
        super(ImageSplitterTabController, self).__init__(model)
        self.model = model

    def imageSrcAt(self):
        return self.model.imageSrcAt

    def imageDstAt(self):
        return self.model.imageDstAt

    def setImageSrcAt(self, at: str):
        self.model.imageSrcAt = at

    def setImageDstAt(self, at: str):
        self.model.imageDstAt = at
