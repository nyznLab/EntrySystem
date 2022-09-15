import ast
import json
import logging
import time

import scales.dao as scales_dao
import scales.xmlHandler as xmlHandler
import scales.cash as cash
import scales.config as config
import scales.ruleParser as ruleParser


# 更新scale_content
def update_scale_content(t_scales_content_model):
    # 取当前时间戳
    t_scales_content_model.create_time = int(time.time())
    # 取对应scale_definition_id的最大的版本号
    last_version = scales_dao.get_scale_content_version_by_id(t_scales_content_model.scale_definition_id)
    if last_version is None:
        # 如果没找到版本号则是第一个版本 返回1
        t_scales_content_model.scale_version = 1
    else:
        # 找到了版本号+1
        t_scales_content_model.scale_version = last_version + 1
    # 插入scale_content
    return scales_dao.insert_scale_content(t_scales_content_model)


# 更新scale_content的输入参数校验
def update_scales_content_validate(request):
    # 判断对应字段是不是传了空值进来
    scale_name = request.POST.get('scale_name')
    if scale_name is None:
        return "scale_name is None"
    scale_definition_id = request.POST.get('scale_definition_id')
    if scale_definition_id is None:
        return "scale_definition_id is None"
    scale_group = request.POST.get('scale_group')
    if scale_group is None:
        return "scale_group is None"
    scale_content = request.POST.get('scale_content')
    if scale_content is None:
        return "scale_content is None"
    try:
        # 使用xml解析scale_content 查看scale_content语法是不是合法
        handler = xmlHandler.loadScaleXML(scale_content)
    except BaseException:
        return "XML Illegal", None
    create_user = request.POST.get('create_user')
    if create_user is None:
        return "create_user is None", None
    return None, handler


# 取正确的scale_content
def get_right_scale_content(scale_id, patient_session_id):
    # 取患者做一半的量表的scale_content版本号
    version = scales_dao.get_version_of_history_scale(config.scaleId_Models_Map[str(scale_id)], patient_session_id)
    if version is None:
        # 没取到说明还没做过这个量表 用最新版本的量表
        scale_content_model = scales_dao.get_scale_content_by_id(scale_id)
        if scale_content_model is None:
            raise ValueError
        # 加载对应scale_content的xml
        handler = xmlHandler.loadScaleXML(scale_content_model.scale_content)
        if scale_id not in cash.scales_content_handler_dic.keys():
            # 同时如果 cash 中没有最新版本的则缓存到 cash 中
            cash.scales_content_handler_dic[scale_id] = {
                "scaleHandler": handler,
                "version": scale_content_model.scale_version,
            }
    else:
        # version 不是空的 先查缓存是否是对应版本
        if scale_id in cash.scales_content_handler_dic.keys() and \
                cash.scales_content_handler_dic[scale_id]["version"] == version:
            # 缓存中有对应版本 则直接返回缓存中的数据
            return cash.scales_content_handler_dic[scale_id]["scaleHandler"].scaleContent
        else:
            # 缓存中没有对应版本 从数据库中取并返回
            scale_content_model = scales_dao.get_scale_content_by_id_and_version(scale_id, version)
            if scale_content_model is None:
                raise ValueError
            handler = xmlHandler.loadScaleXML(scale_content_model.scale_content)
    return handler.scaleContent


# 从数据库中找到最后一个已完成题目的索引
def get_last_question_index_from_db(patient_session_id, scale_id):
    # 从数据库中把对应的记录找出来
    answer = scales_dao.get_scale_answers(config.scaleId_Models_Map[scale_id], patient_session_id)
    if answer is None:
        # 没查到记录说明以前没有做过这个量表 索引为0 将索引加载进缓存 同时返回
        cash.scales_answer_schedule[patient_session_id] = {
            scale_id: 0,
        }
        return 0
    # 否则说明以前答过这个量表 从1开始遍历对应字段是不是空字符串
    question_index = 1
    while hasattr(answer, "question{}".format(question_index)):
        if getattr(answer, "question{}".format(question_index)) is "":
            # 如果是空字符串则说明当前题目没有作答 当前索引-1就是最后一个已完成题目的索引
            if patient_session_id not in cash.scales_answer_schedule.keys():
                # 缓存中没有 则加载进缓存
                cash.scales_answer_schedule[patient_session_id] = {}
            # 缓存中有 则更新缓存
            cash.scales_answer_schedule[patient_session_id][scale_id] = question_index - 1
            return question_index - 1
        # 当前字段不是空字符串 说明没找到 继续找下一个字段
        question_index += 1
    # 找了个遍也没找到 返回0
    return 0


# 找到最后一个已完成题目的索引
def get_last_question_index(patient_session_id, scale_id):
    if patient_session_id in cash.scales_answer_schedule.keys():
        if scale_id in cash.scales_answer_schedule[patient_session_id].keys():
            # 如果缓存里面有 则返回缓存中的索引
            return cash.scales_answer_schedule[patient_session_id][scale_id]
    # 缓存中没有 只能取数据库中找
    return get_last_question_index_from_db(patient_session_id, scale_id)


# 匹配规则
def match_rules(rule, scale_id, patient_session_id):
    # 从数据库中取出回答历史
    answer = scales_dao.get_scale_answers(config.scaleId_Models_Map[scale_id], patient_session_id)
    # 找不到回答历史说明有问题 直接返回False
    if answer is None:
        return False
    # 调用规则匹配
    return call_match_rules(rule, answer)


def call_match_rules(rule, answer):
    # 实例化规则引擎对象
    rule_parser = ruleParser.RuleParser()
    # try:
    # 校验规则的合法性
    rule_parser.validate(ast.literal_eval(rule))
    # TODO 这里return false不方便定位错误，后面return false的同时把错误打印到日志文件里，目前先直接抛ERROR处理
    # except ValueError:
    #     return False
    # 计算规则
    return rule_parser.evaluate(answer, ast.literal_eval(rule))


# 提交题目答案输入参数校验
def submit_scales_input_validate(request):
    # 防止前端传空值进来
    patient_session_id = request.POST.get("patient_session_id")
    if patient_session_id is None:
        return "patient_session_id is None"
    scale_id = request.POST.get("scale_id")
    if scale_id is None:
        return "scale_id is None"
    doctor_id = request.session.get('doctor_id')
    if doctor_id is None:
        return "doctor_id is None"
    form_data = request.POST.get('data')
    if form_data is None:
        return "form_data is None"
    form_content = json.loads(form_data)
    for key in form_content.keys():
        if form_content[key] is None:
            return "{} is None".format(key)
    duration = request.POST.get('duration')
    if duration is None:
        return "duration is None"


# 写入题目答案
def write_scale_answer(scale_id, patient_session_id, form_content, doctor_id):
    scales_dao.update_scales(config.scaleId_Models_Map[scale_id], patient_session_id, form_content, doctor_id, scale_id)


# 写入题目响应时间
def write_scale_duration(patient_session_id, scale_id, duration):
    # 将题目索引加载进缓存
    if patient_session_id in cash.scales_answer_schedule.keys():
        if scale_id not in cash.scales_answer_schedule[patient_session_id].keys():
            cash.scales_answer_schedule[patient_session_id][scale_id] = get_last_question_index_from_db(
                patient_session_id, scale_id)
    else:
        cash.scales_answer_schedule[patient_session_id] = {scale_id: get_last_question_index_from_db(
            patient_session_id, scale_id)}
    # 缓存中的题目索引+1
    cash.scales_answer_schedule[patient_session_id][scale_id] += 1
    # 将响应时间插入数据库
    scales_dao.insert_scale_duration(patient_session_id, scale_id,
                                     cash.scales_answer_schedule[patient_session_id][scale_id], duration)


# 量表完成状态为已完成
def complete_scale(patient_session_id, scale_id):
    scales_dao.update_rscales_state(patient_session_id, scale_id, config.Scale_Completed)


# 量表完成状态为未完成
def not_complete_scale(scale_id, patient_session_id):
    scales_dao.update_rscales_state(patient_session_id, scale_id, config.Scale_Not_Completed)


# 删除某一个scale_content
def delete_scale_content(scale_id, version):
    return scales_dao.delete_scale_content(scale_id, version)


# 重做量表
def redo_scale(scale_id, patient_session_id):
    # 删除缓存中记录的已完成题号
    if patient_session_id in cash.scales_answer_schedule.keys():
        if scale_id in cash.scales_answer_schedule[patient_session_id]:
            cash.scales_answer_schedule[patient_session_id].pop(scale_id)
    # 将之前的答题记录删除
    res = scales_dao.delete_scale_answers(config.scaleId_Models_Map[str(scale_id)], patient_session_id)
    if res is None:
        # 之前没做过对应量表 不能重做
        return False
    # 将总分记录删掉
    scales_dao.delete_scale_scores(scale_id, patient_session_id)
    # 将量表完成状态置为未完成
    not_complete_scale(scale_id, patient_session_id)
    return True


# 获取总分（部分量表可能有多个总分）
def get_total_score(scale_id, patient_session_id):
    res = scales_dao.get_total_score(scale_id, patient_session_id)
    return res

# 根据题号取答案
def get_answer_by_index(scale_id, patient_session_id, question_index):
    res = scales_dao.get_answer_by_index(config.scaleId_Models_Map[str(scale_id)], patient_session_id,
                                         "question{}".format(question_index))
    return res


# 根据patient_session_id 取 patient_id
def get_patient_id(patient_session_id):
    return scales_dao.get_patient_id(patient_session_id)


# 处理计算总分的规则
def process_total_score_calculate_rules(calculate_rules):
    calculate_rules_list = str(calculate_rules).split("//")
    calculate_rules_dic = {}
    for calculate_rule in calculate_rules_list:
        calculate_rules_dic[str(calculate_rule).split(":")[0]] = str(calculate_rule).split(":")[1]
    return calculate_rules_dic


# 写入量表总分
def write_scale_total_scores(scale_definition_id, scale_answers_id, scale_content_id, calculate_rule_id,
                             patient_session_id, score_name, score_value, create_user):
    return scales_dao.insert_scale_total_score(
        scale_definition_id,
        scale_answers_id,
        scale_content_id,
        calculate_rule_id,
        patient_session_id,
        score_name,
        score_value,
        create_user,
    )


#  计算量表总分
def calculate_scale_score(patient_session_id, scale_id, user_id):
    score_dic = {}
    # 取答题记录
    scale_answer_obj = scales_dao.get_scale_answers(config.scaleId_Models_Map[str(scale_id)], patient_session_id)
    # 根据量表的version取scale_content_id
    scale_content = scales_dao.get_scale_content_by_id_and_version(scale_id, scale_answer_obj.version)
    if scale_content is not None:
        scale_content_id = scale_content.id
    # 取总分计算规则
    calculate_rules_obj = scales_dao.get_scale_calculate_rules_obj(scale_id, scale_content_id)
    if calculate_rules_obj is None:
        return
    # 处理总分计算规则
    calculate_rules_dic = process_total_score_calculate_rules(calculate_rules_obj["calculate_rule"])
    # 计算总分
    for score_name in calculate_rules_dic.keys():
        res = write_scale_total_scores(
            scale_id,
            scale_answer_obj.id,
            scale_content_id,
            calculate_rules_obj["id"],
            patient_session_id,
            score_name,
            call_match_rules(calculate_rules_dic[score_name], scale_answer_obj),
            user_id,
        )
        if res is None:
            logging.warning(f"calculate_scale_score of patient_session_id {patient_session_id} "
                            f"on scale {scale_id}"
                            f" error: {json.dumps(scale_answer_obj)}")
    return score_dic

# 自杀量表9，10，11，12题选不自杀选项，总分置0
def calculate_scale_score_bss(patient_session_id, scale_id, user_id):
    score_value = 0
    score_dic = {}
    # 取答题记录
    scale_answer_obj = scales_dao.get_scale_answers(config.scaleId_Models_Map[str(scale_id)], patient_session_id)
    # 根据量表的version取scale_content_id
    scale_content = scales_dao.get_scale_content_by_id_and_version(scale_id, scale_answer_obj.version)
    if scale_content is not None:
        scale_content_id = scale_content.id
    # 取总分计算规则
    calculate_rules_obj = scales_dao.get_scale_calculate_rules_obj(scale_id, scale_content_id)
    if calculate_rules_obj is None:
        return
    # 处理总分计算规则
    calculate_rules_dic = process_total_score_calculate_rules(calculate_rules_obj["calculate_rule"])
    # 写入总分
    for score_name in calculate_rules_dic.keys():
        res = write_scale_total_scores(
            scale_id,
            scale_answer_obj.id,
            scale_content_id,
            calculate_rules_obj["id"],
            patient_session_id,
            score_name,
            score_value,
            user_id,
        )
        if res is None:
            logging.warning(f"calculate_scale_score of patient_session_id {patient_session_id} "
                            f"on scale {scale_id}"
                            f" error: {json.dumps(scale_answer_obj)}")
    return score_dic

