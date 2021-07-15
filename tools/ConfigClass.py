#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：entry_system
@File ：ConfigClass.py
@IDE  ：PyCharm
@Author ：skj
@Date ：1/26/21 8:39 PM
一些配置类
'''
class HospitalizedState(object):
    NOT_HOSPITALIZED = 0
    INPATIENT = 1
    OUT_HOSPITAL = 2

# 医嘱type类型
class MedicalType(object):
    # 药物
    DRUGS = 1
    # 常规护理
    NORMAL_NURSING = 1
    # 常规治疗
    NORMAL_TREATMENT = 2
    # 量表
    NORMAL_SCALES = 3
    # 电休克
    ECT = 4
    # 物理治疗
    PHYSICAL_TREATMENT = 5
    # 团体生物反馈治疗
    BIOFEEDBACK = 6
    # VR治疗
    VR = 7
    # 其他
    OTHER = 8