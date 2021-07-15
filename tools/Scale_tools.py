# 总分筛选条件分配(data为request.GET或request.POST)

def scales_condition_alloc(data, scales_name, search_dict, scale_class_name):
    ts_str = 'total_score'
    cp_str = '_compare'
    scale_class_name = scale_class_name.lower()
    get_name = scales_name+'_'+ts_str
    search_key = scale_class_name+'__'+ts_str
    if data.get(get_name):
        if int(data.get(scales_name+cp_str)) == 0:
            search_dict[search_key] = data[get_name]
        elif int(data.get(scales_name+cp_str)) == 1:
            search_dict[search_key] = data[get_name]
        else:
            search_dict[search_key] = data[get_name]