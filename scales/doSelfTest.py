import ast
import json
import time

import scales.dao as scales_dao
import scales.xmlHandler as xmlHandler
import scales.cash as cash
import scales.config as config
import scales.ruleParser as ruleParser


def update_scale_content(t_scales_content_model):
    t_scales_content_model.create_time = int(time.time())
    last_version = scales_dao.get_scale_content_version_by_id(t_scales_content_model.scale_definition_id)
    if last_version is None:
        t_scales_content_model.scale_version = 1
    else:
        t_scales_content_model.scale_version = last_version + 1

    return scales_dao.insert_scale_content(t_scales_content_model)


def update_scales_content_validate(request):
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
        handler = xmlHandler.loadScaleXML(scale_content)
    except BaseException:
        return "XML Illegal", None
    create_user = request.POST.get('create_user')
    if create_user is None:
        return "create_user is None", None
    return None, handler


def get_right_scale_content(scale_id, patient_session_id):
    print(scale_id, patient_session_id)
    version = scales_dao.get_version_of_history_scale(config.scaleId_Models_Map[str(scale_id)], patient_session_id)
    print(version)
    if scale_id not in cash.scales_content_handler_dic.keys():
        scale_content_model = scales_dao.get_scale_content_by_id(scale_id)
        if scale_content_model is None:
            raise ValueError
        handler = xmlHandler.loadScaleXML(scale_content_model.scale_content)
        cash.scales_content_handler_dic[scale_id] = {
            "scaleHandler": handler,
            "version": scale_content_model.scale_version,
        }
    if cash.scales_content_handler_dic[scale_id]["version"] == version:
        return cash.scales_content_handler_dic[scale_id]["scaleHandler"].scaleContent
    scale_content_model = scales_dao.get_scale_content_by_id_and_version(scale_id, version)
    if scale_content_model is None:
        raise ValueError
    handler = xmlHandler.loadScaleXML(scale_content_model.scale_content)
    return handler.scaleContent


def get_last_question_index_from_db(patient_session_id, scale_id):
    answer = scales_dao.get_scale_answers(config.scaleId_Models_Map[scale_id], patient_session_id)
    if answer is None:
        cash.scales_answer_schedule[patient_session_id][scale_id] = 0
        return 0
    question_index = 1
    while hasattr(answer, "question{}".format(question_index)):
        if getattr(answer, "question{}".format(question_index)) is "":
            if patient_session_id not in cash.scales_answer_schedule.keys():
                cash.scales_answer_schedule[patient_session_id] = {}
            cash.scales_answer_schedule[patient_session_id][scale_id] = question_index - 1
            return question_index - 1
        question_index += 1
    return 0


def get_last_question_index(patient_session_id, scale_id):
    if patient_session_id in cash.scales_answer_schedule.keys():
        if scale_id in cash.scales_answer_schedule[patient_session_id].keys():
            return cash.scales_answer_schedule[patient_session_id][scale_id]
    return get_last_question_index_from_db(patient_session_id, scale_id)


def match_rules(rule, scale_id, patient_session_id):
    answer = scales_dao.get_scale_answers(config.scaleId_Models_Map[scale_id], patient_session_id)
    if answer is None:
        return False
    return call_match_rules(rule, answer)


def call_match_rules(rule, answer):
    rule_parser = ruleParser.RuleParser()
    # try:
    rule_parser.validate(ast.literal_eval(rule))
    # TODO 这里return false不方便定位错误，后面return false的同时把错误打印到日志文件里，目前先直接抛ERROR处理
    # except ValueError:
    #     return False
    return rule_parser.evaluate(answer, ast.literal_eval(rule))


def submit_scales_input_validate(request):
    patient_session_id = request.POST.get("patient_session_id")
    if patient_session_id is None:
        return "patient_session_id is None"
    scale_id = request.POST.get("scale_id")
    if scale_id is None:
        return "scale_id is None"
    doctor_id = request.POST.get('doctor_id')
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


def write_scale_answer(scale_id, patient_session_id, form_content, doctor_id):
    scales_dao.update_scales(config.scaleId_Models_Map[scale_id], patient_session_id, form_content, doctor_id, scale_id)


def write_scale_duration(patient_session_id, scale_id, duration):
    if patient_session_id in cash.scales_answer_schedule.keys():
        if scale_id not in cash.scales_answer_schedule[patient_session_id].keys():
            cash.scales_answer_schedule[patient_session_id][scale_id] = get_last_question_index_from_db(
                patient_session_id, scale_id)
    else:
        cash.scales_answer_schedule[patient_session_id] = {scale_id: get_last_question_index_from_db(
            patient_session_id, scale_id)}
    scales_dao.insert_scale_duration(patient_session_id, scale_id,
                                     cash.scales_answer_schedule[patient_session_id][scale_id], duration)
    cash.scales_answer_schedule[patient_session_id][scale_id] += 1


def complete_scale(scale_id, patient_session_id):
    scales_dao.update_rscales_state(patient_session_id, scale_id, config.Scale_Completed)


def not_complete_scale(scale_id, patient_session_id):
    scales_dao.update_rscales_state(patient_session_id, scale_id, config.Scale_Not_Completed)


def delete_scale_content(scale_id, version):
    return scales_dao.delete_scale_content(scale_id, version)


def redo_scale(scale_id, patient_session_id):
    if patient_session_id in cash.scales_answer_schedule.keys():
        if scale_id in cash.scales_answer_schedule[patient_session_id]:
            cash.scales_answer_schedule[patient_session_id].pop(scale_id)
    res = scales_dao.delete_scale_answers(config.scaleId_Models_Map[str(scale_id)], patient_session_id)
    if res is None:
        return False
    not_complete_scale(scale_id, patient_session_id)
    return True


def get_answer_by_index(scale_id, patient_session_id, question_index):
    res = scales_dao.get_answer_by_index(config.scaleId_Models_Map[str(scale_id)], patient_session_id,
                                         "question{}".format(question_index))
    return res


def get_patient_id(patient_session_id):
    return scales_dao.get_patient_id(patient_session_id)
