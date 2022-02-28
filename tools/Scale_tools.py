# 总分筛选条件分配
"""
Parameters
    data: QueryDict
        request.GET或request.POST中的请求参数与值
    scales_name: str
        量表名（自命名，与前台保持一致）
    search_dict: dict
        搜索条件
    scale_class_name: str
        量表模型类名
Returns
    Nothing
"""
def scales_condition_alloc(data, scales_name, search_dict, scale_class_name):
    ts_str = 'total_score'
    cp_str = '_compare'
    scale_class_name = scale_class_name.lower()
    get_name = scales_name + '_' + ts_str
    search_key = scale_class_name + '__' + ts_str
    if data.get(get_name):
        if int(data.get(scales_name + cp_str)) == 0:
            search_dict[search_key] = data[get_name]
        elif int(data.get(scales_name + cp_str)) == 1:
            search_dict[search_key + '__gte'] = data[get_name]
        else:
            search_dict[search_key + '__lte'] = data[get_name]


def scales_condition_allocation(data, condition, scales_name_models_dict):
    # for name, model_name in scales_name_models_dict.items():
    #     pass

    if data.getlist('scale_id') and data.getlist('scale_total_score_name') and data.getlist('scale_total_score') and data.getlist('scales_total_score_compare'):

        pass