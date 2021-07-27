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
        return "XML Illegal"
    cash.scales_content_handler_dic[scale_definition_id] = handler
    create_user = request.POST.get('create_user')
    if create_user is None:
        return "create_user is None"
    return None


def get_scale_content_by_scale_id(scale_id):
    if scale_id in cash.scales_content_handler_dic.keys():
        return cash.scales_content_handler_dic[scale_id].scaleContent
    scale_content_model = scales_dao.get_scale_content_by_id(scale_id)
    if scale_content_model is None:
        raise ValueError
    handler = xmlHandler.loadScaleXML(scale_content_model.scale_content)
    cash.scales_content_handler_dic[scale_id] = handler
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
            print("question_index_from_chche {} ".format(cash.scales_answer_schedule[patient_session_id][scale_id]))
            return cash.scales_answer_schedule[patient_session_id][scale_id]
    return get_last_question_index_from_db(patient_session_id, scale_id)


def match_rules(rule, scale_id, patient_session_id):
    print(rule, patient_session_id, scale_id)
    answer = scales_dao.get_scale_answers(config.scaleId_Models_Map[scale_id], patient_session_id)
    print(answer)
    if answer is None:
        return False
    print("call_match_rules")
    return call_match_rules(rule, answer)


def call_match_rules(rule, answer):
    print("call_match_rules rule: {} answer {}".format(rule, answer))
    rule_parser = ruleParser.RuleParser()
    print("call_match_rules rule_parser")
    # try:
    rule_parser.validate(json.loads(rule))
    # except ValueError:
    #     return False
    print("rule_parser validate pass")
    return rule_parser.evaluate(answer, json.loads(rule))


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
    scales_dao.update_scales(config.scaleId_Models_Map[scale_id], patient_session_id, form_content, doctor_id)


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
