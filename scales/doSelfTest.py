import os
import time

import scales.dao as scales_dao
import scales.xmlHandler as xmlHandler
import scales.cash as cash
import scales.config as config


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
    except KeyError:
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
        return 0
    question_index = 1
    while hasattr(answer, "question{}".format(question_index)):
        if getattr(answer, "question{}".format(question_index)) is None:
            return question_index
        question_index += 1
    return 0


def get_last_question_index(patient_session_id, scale_id):
    if patient_session_id in cash.scales_answer_schedule.keys():
        if scale_id in cash.scales_answer_schedule[patient_session_id].keys():
            return cash.scales_answer_schedule[patient_session_id][scale_id]
    return get_last_question_index_from_db(patient_session_id, scale_id)


def match_rules(rule, patient_session_id, scale_id):
    answer = scales_dao.get_scale_answers(config.scaleId_Models_Map[scale_id], patient_session_id)
    if answer is None:
        return False

    return False
