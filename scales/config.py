import scales.models as models

# scale_definition --- models 的映射关系
scaleId_Models_Map = {
    '11': models.TScaleYbo,
    '12': models.TScaleBss,
    '13': models.TScaleHcl,
    '14': models.TScaleShapes,
    '15': models.TScaleTeps,
    '16': models.TScaleCtqsf,
    '17': models.TScaleCerqc,
    '18': models.TScaleAslec,
    '19': models.TScaleSembu,
    '20': models.TScaleAtq,
    '29': models.TScalePhq,
    '30': models.TScaleGad,
    '31': models.TScaleInsomnia,
    '32': models.TScalePss,
    '34': models.TScalePhoneAbuse,
}

self_scale_question_count = {
    '11': 10,
    '12': 40,
    '13': 46,
    '14': 14,
    '15': 18,
    '16': 29,
    '17': 36,
    '18': 27,
    '19': 7,
    '20': 30,
    '29': 9,
    '30': 7,
    '31': 7,
    '32': 14,
    '34': 99,
}




# 量表完成状态常量
Scale_Completed = 1
Scale_Not_Completed = 0

# 逻辑删除标志常量
Del_Yse = 1
Del_No = 0
