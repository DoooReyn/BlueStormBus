#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/25
#  Name: decorator.py
#  Author: DoooReyn
#  Description: 装饰器

class Decorator:
    """装饰器"""

    @staticmethod
    def singleton(cls):
        """单例"""
        _instance = {}

        def _singleton(*args, **kargs):
            if cls not in _instance:
                _instance[cls] = cls(*args, **kargs)
            return _instance[cls]

        return _singleton
