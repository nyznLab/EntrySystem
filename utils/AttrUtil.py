#!/usr/bin/env python
# *_*coding:utf-8 *_*

# 对象属性赋值
class AttrUtil:

    @classmethod
    def set_attr(cls, request, model):
        for key in request.POST.keys():
            if hasattr(model, key) and request.POST.get(key).strip() != '':
                # 属性赋值
                setattr(model, key, request.POST.get(key))
            else:
                setattr(model, key, None)
        return model