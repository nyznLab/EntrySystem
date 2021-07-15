##############量表得分规则计算接口#############
##############量表得分规则计算接口#############
##############量表得分规则计算接口#############
##############量表得分规则计算接口#############


# 中国人利手量表得分计算
def Handy_total_score(rPatientChineseHandy_object):
    if rPatientChineseHandy_object is None \
            or rPatientChineseHandy_object.hold_pen is None \
            or rPatientChineseHandy_object.hold_chopsticks is None \
            or rPatientChineseHandy_object.throw_things is None \
            or rPatientChineseHandy_object.brush_tooth is None \
            or rPatientChineseHandy_object.use_scissors is None \
            or rPatientChineseHandy_object.use_match is None:
        # 标志位,用于判断是否存在空值
        object_flag = True
        total_score = None
    else:
        six_item = int(rPatientChineseHandy_object.hold_pen) + int(rPatientChineseHandy_object.hold_chopsticks) + int(
            rPatientChineseHandy_object.throw_things) + \
                   int(rPatientChineseHandy_object.brush_tooth) + int(rPatientChineseHandy_object.use_scissors) + int(
            rPatientChineseHandy_object.use_match)

        if int(rPatientChineseHandy_object.hold_pen) == 2 or int(
                rPatientChineseHandy_object.hold_chopsticks) == 2 or int(rPatientChineseHandy_object.throw_things) == 2 \
                or int(rPatientChineseHandy_object.brush_tooth) == 2 or int(
            rPatientChineseHandy_object.use_scissors) == 2 or int(rPatientChineseHandy_object.use_match) == 2:
            total_score = 3
        elif six_item == 6:
            total_score = 1
        elif six_item == 0:
            total_score = 2
        else:
            total_score = 3
        object_flag = False

    return total_score, object_flag


# 汉密尔顿抑郁量表得分计算
def HAMD17_total_score(rPatientHamd17_object):
    if rPatientHamd17_object is None \
            or rPatientHamd17_object.depression is None \
            or rPatientHamd17_object.guilt is None \
            or rPatientHamd17_object.suicide is None \
            or rPatientHamd17_object.difficulty_sleeping is None \
            or rPatientHamd17_object.sleep_deep is None \
            or rPatientHamd17_object.sleep_deep is None \
            or rPatientHamd17_object.wake_early is None \
            or rPatientHamd17_object.work_interest is None \
            or rPatientHamd17_object.slow is None \
            or rPatientHamd17_object.intense is None \
            or rPatientHamd17_object.psycho_anxiety is None \
            or rPatientHamd17_object.somatic_anxiety is None \
            or rPatientHamd17_object.gastrointestinal_symptoms is None \
            or rPatientHamd17_object.systemic_symptoms is None \
            or rPatientHamd17_object.sexual_symptoms is None \
            or rPatientHamd17_object.hypochondria is None \
            or rPatientHamd17_object.lose_weight is None \
            or rPatientHamd17_object.self_awareness is None:
        object_flag = True
        total_score = None
    else:
        total_score = int(rPatientHamd17_object.depression) + int(rPatientHamd17_object.guilt) + int(
            rPatientHamd17_object.suicide) + int(rPatientHamd17_object.difficulty_sleeping) + \
                      int(rPatientHamd17_object.sleep_deep) + int(rPatientHamd17_object.wake_early) + int(
            rPatientHamd17_object.work_interest) + int(rPatientHamd17_object.slow) + \
                      int(rPatientHamd17_object.intense) + int(rPatientHamd17_object.psycho_anxiety) + int(
            rPatientHamd17_object.somatic_anxiety) + int(rPatientHamd17_object.gastrointestinal_symptoms) + \
                      int(rPatientHamd17_object.systemic_symptoms) + int(rPatientHamd17_object.sexual_symptoms) + int(
            rPatientHamd17_object.hypochondria) + int(rPatientHamd17_object.lose_weight) + \
                      int(rPatientHamd17_object.self_awareness)

        if total_score <= 68 and total_score >= 0:
            object_flag = False
        else:
            object_flag = True
            total_score = None
    return total_score, object_flag


# 汉密尔顿焦虑量表得分计算
def HAMA_total_score(rPatientHama_object):
    if rPatientHama_object is None \
            or rPatientHama_object.anxiety is None \
            or rPatientHama_object.nervous is None \
            or rPatientHama_object.fear is None \
            or rPatientHama_object.insomnia is None \
            or rPatientHama_object.cognitive_function is None \
            or rPatientHama_object.depression is None \
            or rPatientHama_object.somaticanxiety_muscle is None \
            or rPatientHama_object.somaticanxiety_sensory is None \
            or rPatientHama_object.cardiovascular_symptoms is None \
            or rPatientHama_object.respiratory_symptoms is None \
            or rPatientHama_object.gastrointestinal_symptoms is None \
            or rPatientHama_object.genitourinary_symptoms is None \
            or rPatientHama_object.plantnervous_symptoms is None \
            or rPatientHama_object.interview_behavior is None:
        object_flag = True
        total_score = None
    else:
        total_score = int(rPatientHama_object.anxiety) + int(rPatientHama_object.nervous) + int(
            rPatientHama_object.fear) + int(rPatientHama_object.insomnia) + int(
            rPatientHama_object.cognitive_function) + \
                      int(rPatientHama_object.depression) + int(rPatientHama_object.somaticanxiety_muscle) + int(
            rPatientHama_object.somaticanxiety_sensory) + int(rPatientHama_object.cardiovascular_symptoms) + \
                      int(rPatientHama_object.respiratory_symptoms) + int(
            rPatientHama_object.gastrointestinal_symptoms) + int(rPatientHama_object.genitourinary_symptoms) + int(
            rPatientHama_object.plantnervous_symptoms) + \
                      int(rPatientHama_object.interview_behavior)
        if total_score <= 56 and total_score >= 0:
            object_flag = False
        else:
            object_flag = True
            total_score = None
    return total_score, object_flag


# 杨氏躁狂量表得分计算
def YMRS_total_score(rPatientYmrs_object):
    if rPatientYmrs_object is None \
            or rPatientYmrs_object.emotional_upsurge is None \
            or rPatientYmrs_object.vigorous_energy is None \
            or rPatientYmrs_object.sexual_desire is None \
            or rPatientYmrs_object.sleep is None \
            or rPatientYmrs_object.irritability is None \
            or rPatientYmrs_object.speech is None \
            or rPatientYmrs_object.language is None \
            or rPatientYmrs_object.thinking_content is None \
            or rPatientYmrs_object.aggressive_behavior is None \
            or rPatientYmrs_object.appearance is None \
            or rPatientYmrs_object.self_awareness is None:
        object_flag = True
        total_score = None
    else:
        total_score = int(rPatientYmrs_object.emotional_upsurge) + int(rPatientYmrs_object.vigorous_energy) + int(
            rPatientYmrs_object.sexual_desire) + int(rPatientYmrs_object.sleep) + \
                      int(rPatientYmrs_object.irritability) + int(rPatientYmrs_object.speech) + int(
            rPatientYmrs_object.language) + int(rPatientYmrs_object.thinking_content) + \
                      int(rPatientYmrs_object.aggressive_behavior) + int(rPatientYmrs_object.appearance) + int(
            rPatientYmrs_object.self_awareness)
        if total_score <= 60 and total_score >= 0:
            object_flag = False
        else:
            object_flag = True
            total_score = None
    return total_score, object_flag


# bprs简式精神量表得分计算
def Bprs_total_score(rPatientBprs_object):
    if rPatientBprs_object is None \
            or rPatientBprs_object.health_care is None \
            or rPatientBprs_object.anxious is None \
            or rPatientBprs_object.emocommunicat_barrier is None \
            or rPatientBprs_object.conceptual_disorder is None \
            or rPatientBprs_object.guilt_concept is None \
            or rPatientBprs_object.nervous is None \
            or rPatientBprs_object.look_act is None \
            or rPatientBprs_object.exaggerate is None \
            or rPatientBprs_object.mood_depression is None \
            or rPatientBprs_object.hostility is None \
            or rPatientBprs_object.suspicion is None \
            or rPatientBprs_object.hallucination is None \
            or rPatientBprs_object.slow_movement is None \
            or rPatientBprs_object.no_cooperation is None \
            or rPatientBprs_object.unusual_thinking is None \
            or rPatientBprs_object.feeling_flat is None \
            or rPatientBprs_object.excitement is None \
            or rPatientBprs_object.directional_disorder is None:
        object_flag = True
        total_score = None
    else:
        total_score = int(rPatientBprs_object.health_care) + int(rPatientBprs_object.anxious) + int(
            rPatientBprs_object.emocommunicat_barrier) + \
                      int(rPatientBprs_object.conceptual_disorder) + int(rPatientBprs_object.guilt_concept) + int(
            rPatientBprs_object.nervous) + \
                      int(rPatientBprs_object.look_act) + int(rPatientBprs_object.exaggerate) + int(
            rPatientBprs_object.mood_depression) + int(rPatientBprs_object.hostility) + \
                      int(rPatientBprs_object.suspicion) + int(rPatientBprs_object.hallucination) + int(
            rPatientBprs_object.slow_movement) + int(rPatientBprs_object.no_cooperation) + \
                      int(rPatientBprs_object.unusual_thinking) + int(rPatientBprs_object.feeling_flat) + int(
            rPatientBprs_object.excitement) + int(rPatientBprs_object.directional_disorder)
        if total_score <= 126 and total_score >= 0:
            object_flag = False
        else:
            object_flag = True
            total_score = None
    return total_score, object_flag


# 耶鲁布朗得分计算
def YBO_total_score(rPatientYbobsessiontable_object):
    if rPatientYbobsessiontable_object is None \
            or rPatientYbobsessiontable_object.forced_frequency is None \
            or rPatientYbobsessiontable_object.impediment_degree1 is None \
            or rPatientYbobsessiontable_object.impediment_degree2 is None \
            or rPatientYbobsessiontable_object.distress is None \
            or rPatientYbobsessiontable_object.fightforced_degree is None \
            or rPatientYbobsessiontable_object.control_ability1 is None \
            or rPatientYbobsessiontable_object.control_ability2 is None \
            or rPatientYbobsessiontable_object.compulsion_frequency is None \
            or rPatientYbobsessiontable_object.stopcompulsion_anxiety is None \
            or rPatientYbobsessiontable_object.stopforced_frequency is None:
        object_flag = True
        total_score = None
    else:
        total_score = int(rPatientYbobsessiontable_object.forced_frequency) + int(
            rPatientYbobsessiontable_object.impediment_degree1) + \
                      int(rPatientYbobsessiontable_object.impediment_degree2) + int(
            rPatientYbobsessiontable_object.distress) + int(rPatientYbobsessiontable_object.fightforced_degree) + \
                      int(rPatientYbobsessiontable_object.control_ability1) + int(
            rPatientYbobsessiontable_object.control_ability2) + int(
            rPatientYbobsessiontable_object.compulsion_frequency) + \
                      int(rPatientYbobsessiontable_object.stopcompulsion_anxiety) + int(
            rPatientYbobsessiontable_object.stopforced_frequency)
        if total_score <= 40 and total_score >= 0:
            object_flag = False
        else:
            object_flag = True
            total_score = None
    return total_score, object_flag


# 自杀意念及行为史
def Suicidal_total_score(rPatientSuicidal_object):
    suicide_ideation = None
    if rPatientSuicidal_object is None \
            or rPatientSuicidal_object.question1_lastweek is None \
            or rPatientSuicidal_object.question1_mostdepressed is None \
            or rPatientSuicidal_object.question2_lastweek is None \
            or rPatientSuicidal_object.question2_mostdepressed is None \
            or rPatientSuicidal_object.question3_lastweek is None \
            or rPatientSuicidal_object.question3_mostdepressed is None \
            or rPatientSuicidal_object.question4_lastweek is None \
            or rPatientSuicidal_object.question5_lastweek is None \
            or rPatientSuicidal_object.question4_mostdepressed is None \
            or rPatientSuicidal_object.question5_mostdepressed is None:
        object_flag = True
        total_score_lastweek = None
        total_score_mostdepressed = None
    #前五题非空
    else:
        flag_lastweek = int(rPatientSuicidal_object.question4_lastweek) + int(
            rPatientSuicidal_object.question5_lastweek)
        flag_mostdepressed = int(rPatientSuicidal_object.question4_mostdepressed) + int(
            rPatientSuicidal_object.question5_mostdepressed)
        if rPatientSuicidal_object.question6_lastweek is None \
                or rPatientSuicidal_object.question7_lastweek is None \
                or rPatientSuicidal_object.question8_lastweek is None \
                or rPatientSuicidal_object.question9_lastweek is None \
                or rPatientSuicidal_object.question10_lastweek is None \
                or rPatientSuicidal_object.question11_lastweek is None \
                or rPatientSuicidal_object.question12_lastweek is None \
                or rPatientSuicidal_object.question13_lastweek is None \
                or rPatientSuicidal_object.question14_lastweek is None \
                or rPatientSuicidal_object.question15_lastweek is None \
                or rPatientSuicidal_object.question16_lastweek is None \
                or rPatientSuicidal_object.question17_lastweek is None \
                or rPatientSuicidal_object.question18_lastweek is None \
                or rPatientSuicidal_object.question19_lastweek is None:
            object_flag_lastweek = True
            total_score_lastweek = None
        else:
            sum_lastweek = int(rPatientSuicidal_object.question6_lastweek) + int(
                rPatientSuicidal_object.question7_lastweek) + int(rPatientSuicidal_object.question8_lastweek) + \
                           int(rPatientSuicidal_object.question9_lastweek) + int(
                rPatientSuicidal_object.question10_lastweek) + int(rPatientSuicidal_object.question11_lastweek) + \
                           int(rPatientSuicidal_object.question12_lastweek) + int(
                rPatientSuicidal_object.question13_lastweek) + int(rPatientSuicidal_object.question14_lastweek) + \
                           int(rPatientSuicidal_object.question15_lastweek) + int(
                rPatientSuicidal_object.question16_lastweek) + int(rPatientSuicidal_object.question17_lastweek) + \
                           int(rPatientSuicidal_object.question18_lastweek) + int(
                rPatientSuicidal_object.question19_lastweek)

            total_score_lastweek = (sum_lastweek - 9) / 33 * 100
            if flag_lastweek == 2:
                object_flag_lastweek = False
            elif total_score_lastweek <= 100 and total_score_lastweek >= 0:
                object_flag_lastweek = False
            else:
                object_flag_lastweek = True
                total_score_lastweek = None
        # 另一分支
        if rPatientSuicidal_object.question6_mostdepressed is None \
                or rPatientSuicidal_object.question7_mostdepressed is None \
                or rPatientSuicidal_object.question8_mostdepressed is None \
                or rPatientSuicidal_object.question9_mostdepressed is None \
                or rPatientSuicidal_object.question10_mostdepressed is None \
                or rPatientSuicidal_object.question11_mostdepressed is None \
                or rPatientSuicidal_object.question12_mostdepressed is None \
                or rPatientSuicidal_object.question13_mostdepressed is None \
                or rPatientSuicidal_object.question14_mostdepressed is None \
                or rPatientSuicidal_object.question15_mostdepressed is None \
                or rPatientSuicidal_object.question16_mostdepressed is None \
                or rPatientSuicidal_object.question17_mostdepressed is None \
                or rPatientSuicidal_object.question18_mostdepressed is None \
                or rPatientSuicidal_object.question19_mostdepressed is None:
            object_flag_mostdepressed = True
            total_score_mostdepressed = None
        else:
            sum_mostdepressed = int(rPatientSuicidal_object.question6_mostdepressed) + int(
                rPatientSuicidal_object.question7_mostdepressed) + int(
                rPatientSuicidal_object.question8_mostdepressed) + \
                                int(rPatientSuicidal_object.question9_mostdepressed) + int(
                rPatientSuicidal_object.question10_mostdepressed) + int(
                rPatientSuicidal_object.question11_mostdepressed) + \
                                int(rPatientSuicidal_object.question12_mostdepressed) + int(
                rPatientSuicidal_object.question13_mostdepressed) + int(
                rPatientSuicidal_object.question14_mostdepressed) + \
                                int(rPatientSuicidal_object.question15_mostdepressed) + int(
                rPatientSuicidal_object.question16_mostdepressed) + int(
                rPatientSuicidal_object.question17_mostdepressed) + \
                                int(rPatientSuicidal_object.question18_mostdepressed) + int(
                rPatientSuicidal_object.question19_mostdepressed)
            total_score_mostdepressed = (sum_mostdepressed - 9) / 33 * 100
            if flag_mostdepressed == 2:
                object_flag_mostdepressed = False
            elif total_score_mostdepressed <= 100 and total_score_mostdepressed >= 0:
                object_flag_mostdepressed = False
            else:
                object_flag_mostdepressed = True
                total_score_mostdepressed = None
        object_flag = object_flag_lastweek and object_flag_mostdepressed
    if not object_flag:
        if total_score_lastweek is None and total_score_mostdepressed is None:
            suicide_ideation = 0
        else:
            suicide_ideation = 1
    return total_score_lastweek, total_score_mostdepressed, object_flag,suicide_ideation


# 33项轻躁狂
def ManicSymptom_total_score(rPatientManicsymptom_object):
    if rPatientManicsymptom_object is None \
            or rPatientManicsymptom_object.question3_1 is None \
            or rPatientManicsymptom_object.question3_2 is None \
            or rPatientManicsymptom_object.question3_3 is None \
            or rPatientManicsymptom_object.question3_4 is None \
            or rPatientManicsymptom_object.question3_5 is None \
            or rPatientManicsymptom_object.question3_6 is None \
            or rPatientManicsymptom_object.question3_7 is None \
            or rPatientManicsymptom_object.question3_8 is None \
            or rPatientManicsymptom_object.question3_9 is None \
            or rPatientManicsymptom_object.question3_10 is None \
            or rPatientManicsymptom_object.question3_11 is None \
            or rPatientManicsymptom_object.question3_12 is None \
            or rPatientManicsymptom_object.question3_13 is None \
            or rPatientManicsymptom_object.question3_14 is None \
            or rPatientManicsymptom_object.question3_15 is None \
            or rPatientManicsymptom_object.question3_16 is None \
            or rPatientManicsymptom_object.question3_17 is None \
            or rPatientManicsymptom_object.question3_18 is None \
            or rPatientManicsymptom_object.question3_19 is None \
            or rPatientManicsymptom_object.question3_20 is None \
            or rPatientManicsymptom_object.question3_21 is None \
            or rPatientManicsymptom_object.question3_22 is None \
            or rPatientManicsymptom_object.question3_23 is None \
            or rPatientManicsymptom_object.question3_24 is None \
            or rPatientManicsymptom_object.question3_25 is None \
            or rPatientManicsymptom_object.question3_26 is None \
            or rPatientManicsymptom_object.question3_27 is None \
            or rPatientManicsymptom_object.question3_28 is None \
            or rPatientManicsymptom_object.question3_29 is None \
            or rPatientManicsymptom_object.question3_30 is None \
            or rPatientManicsymptom_object.question3_31 is None \
            or rPatientManicsymptom_object.question3_32 is None \
            or rPatientManicsymptom_object.question3_33 is None:
        object_flag = True
        total_score = None
    else:
        total_score = int(rPatientManicsymptom_object.question3_1) + int(rPatientManicsymptom_object.question3_2) + int(
            rPatientManicsymptom_object.question3_3) + \
                      int(rPatientManicsymptom_object.question3_4) + int(rPatientManicsymptom_object.question3_5) + int(
            rPatientManicsymptom_object.question3_6) + \
                      int(rPatientManicsymptom_object.question3_7) + int(rPatientManicsymptom_object.question3_8) + int(
            rPatientManicsymptom_object.question3_9) + \
                      int(rPatientManicsymptom_object.question3_10) + int(
            rPatientManicsymptom_object.question3_11) + int(rPatientManicsymptom_object.question3_12) + \
                      int(rPatientManicsymptom_object.question3_13) + int(
            rPatientManicsymptom_object.question3_14) + int(rPatientManicsymptom_object.question3_15) + \
                      int(rPatientManicsymptom_object.question3_16) + int(
            rPatientManicsymptom_object.question3_17) + int(rPatientManicsymptom_object.question3_18) + \
                      int(rPatientManicsymptom_object.question3_19) + int(
            rPatientManicsymptom_object.question3_20) + int(rPatientManicsymptom_object.question3_21) + \
                      int(rPatientManicsymptom_object.question3_22) + int(
            rPatientManicsymptom_object.question3_23) + int(rPatientManicsymptom_object.question3_24) + \
                      int(rPatientManicsymptom_object.question3_25) + int(
            rPatientManicsymptom_object.question3_26) + int(rPatientManicsymptom_object.question3_27) + \
                      int(rPatientManicsymptom_object.question3_28) + int(
            rPatientManicsymptom_object.question3_29) + int(rPatientManicsymptom_object.question3_30) + \
                      int(rPatientManicsymptom_object.question3_31) + int(
            rPatientManicsymptom_object.question3_32) + int(rPatientManicsymptom_object.question3_33)
        if total_score <= 33 and total_score >= 0:
            object_flag = False
        else:
            object_flag = True
            total_score = None
    return total_score, object_flag


# 斯奈斯和汉密尔顿快乐
def happiness_total_score(rPatientHappiness_object):
    if rPatientHappiness_object is None \
            or rPatientHappiness_object.question1_answer is None \
            or rPatientHappiness_object.question2_answer is None \
            or rPatientHappiness_object.question3_answer is None \
            or rPatientHappiness_object.question4_answer is None \
            or rPatientHappiness_object.question5_answer is None \
            or rPatientHappiness_object.question6_answer is None \
            or rPatientHappiness_object.question7_answer is None \
            or rPatientHappiness_object.question8_answer is None \
            or rPatientHappiness_object.question9_answer is None \
            or rPatientHappiness_object.question10_answer is None \
            or rPatientHappiness_object.question11_answer is None \
            or rPatientHappiness_object.question12_answer is None \
            or rPatientHappiness_object.question13_answer is None \
            or rPatientHappiness_object.question14_answer is None:
        object_flag = True
        total_score = None
    else:
        total_score = int(rPatientHappiness_object.question1_answer) + int(
            rPatientHappiness_object.question2_answer) + int(rPatientHappiness_object.question3_answer) + \
                      int(rPatientHappiness_object.question4_answer) + int(
            rPatientHappiness_object.question5_answer) + int(rPatientHappiness_object.question6_answer) + \
                      int(rPatientHappiness_object.question7_answer) + int(
            rPatientHappiness_object.question8_answer) + int(rPatientHappiness_object.question9_answer) + \
                      int(rPatientHappiness_object.question10_answer) + int(
            rPatientHappiness_object.question11_answer) + int(rPatientHappiness_object.question12_answer) + \
                      int(rPatientHappiness_object.question13_answer) + int(rPatientHappiness_object.question14_answer)
        if total_score <= 56 and total_score >= 14:
            object_flag = False
        else:
            object_flag = True
            total_score = None
    return total_score, object_flag


# 快乐体验能力
def pleasure_total_score(rPatientPleasure_object):
    if rPatientPleasure_object.question1_answer is None \
            or rPatientPleasure_object.question2_answer is None \
            or rPatientPleasure_object.question3_answer is None \
            or rPatientPleasure_object.question3_answer is None \
            or rPatientPleasure_object.question4_answer is None \
            or rPatientPleasure_object.question5_answer is None \
            or rPatientPleasure_object.question6_answer is None \
            or rPatientPleasure_object.question7_answer is None \
            or rPatientPleasure_object.question8_answer is None \
            or rPatientPleasure_object.question9_answer is None \
            or rPatientPleasure_object.question10_answer is None \
            or rPatientPleasure_object.question11_answer is None \
            or rPatientPleasure_object.question12_answer is None \
            or rPatientPleasure_object.question13_answer is None \
            or rPatientPleasure_object.question14_answer is None \
            or rPatientPleasure_object.question15_answer is None \
            or rPatientPleasure_object.question16_answer is None \
            or rPatientPleasure_object.question17_answer is None \
            or rPatientPleasure_object.question18_answer is None:
        object_flag = True
        exception_total_score = None
        consume_total_score = None
    else:
        exception_total_score = int(rPatientPleasure_object.question1_answer) + int(
            rPatientPleasure_object.question4_answer) + int(rPatientPleasure_object.question6_answer) + \
                                int(rPatientPleasure_object.question8_answer) + int(
            rPatientPleasure_object.question10_answer) + int(rPatientPleasure_object.question11_answer) + \
                                int(rPatientPleasure_object.question13_answer) + int(
            rPatientPleasure_object.question15_answer) + int(rPatientPleasure_object.question16_answer) + \
                                int(rPatientPleasure_object.question18_answer)

        consume_total_score = int(rPatientPleasure_object.question2_answer) + int(
            rPatientPleasure_object.question3_answer) + int(rPatientPleasure_object.question5_answer) + \
                              int(rPatientPleasure_object.question7_answer) + int(
            rPatientPleasure_object.question9_answer) + int(rPatientPleasure_object.question12_answer) + \
                              int(rPatientPleasure_object.question14_answer) + int(
            rPatientPleasure_object.question17_answer)

        if exception_total_score <= 60 and exception_total_score >= 10 and consume_total_score >= 8 and consume_total_score <= 48:
            object_flag = False
        else:
            object_flag = True
            exception_total_score = None
            consume_total_score = None
    return exception_total_score, consume_total_score, object_flag


# 儿童期成长经历
def growth_total_score(rPatientGrowth_object):
    if rPatientGrowth_object is None \
            or rPatientGrowth_object.question1_answer is None \
            or rPatientGrowth_object.question2_answer is None \
            or rPatientGrowth_object.question3_answer is None \
            or rPatientGrowth_object.question4_answer is None \
            or rPatientGrowth_object.question5_answer is None \
            or rPatientGrowth_object.question6_answer is None \
            or rPatientGrowth_object.question7_answer is None \
            or rPatientGrowth_object.question8_answer is None \
            or rPatientGrowth_object.question9_answer is None \
            or rPatientGrowth_object.question10_answer is None \
            or rPatientGrowth_object.question11_answer is None \
            or rPatientGrowth_object.question12_answer is None \
            or rPatientGrowth_object.question13_answer is None \
            or rPatientGrowth_object.question14_answer is None \
            or rPatientGrowth_object.question15_answer is None \
            or rPatientGrowth_object.question16_answer is None \
            or rPatientGrowth_object.question17_answer is None \
            or rPatientGrowth_object.question18_answer is None \
            or rPatientGrowth_object.question19_answer is None \
            or rPatientGrowth_object.question20_answer is None \
            or rPatientGrowth_object.question21_answer is None \
            or rPatientGrowth_object.question22_answer is None \
            or rPatientGrowth_object.question23_answer is None \
            or rPatientGrowth_object.question24_answer is None \
            or rPatientGrowth_object.question25_answer is None \
            or rPatientGrowth_object.question26_answer is None \
            or rPatientGrowth_object.question27_answer is None \
            or rPatientGrowth_object.question28_answer is None:
        object_flag = True
        emotional_abuse_total_score = None
        physical_abuse_total_score = None
        sexual_abuse_total_score = None
        emotional_ignorance_total_score = None
        physical_ignorance_total_score = None
    else:
        emotional_abuse_total_score = int(rPatientGrowth_object.question3_answer) + int(
            rPatientGrowth_object.question8_answer) + \
                                      int(rPatientGrowth_object.question14_answer) + int(
            rPatientGrowth_object.question18_answer) + \
                                      int(rPatientGrowth_object.question25_answer)
        physical_abuse_total_score = int(rPatientGrowth_object.question9_answer) + int(
            rPatientGrowth_object.question11_answer) + \
                                     int(rPatientGrowth_object.question12_answer) + int(
            rPatientGrowth_object.question15_answer) + \
                                     int(rPatientGrowth_object.question17_answer)
        sexual_abuse_total_score = int(rPatientGrowth_object.question20_answer) + int(
            rPatientGrowth_object.question21_answer) + \
                                   int(rPatientGrowth_object.question23_answer) + int(
            rPatientGrowth_object.question24_answer) + \
                                   int(rPatientGrowth_object.question27_answer)
        emotional_ignorance_total_score = int(rPatientGrowth_object.question5_answer) +int(rPatientGrowth_object.question7_answer) + \
                                          int(rPatientGrowth_object.question13_answer) + int(rPatientGrowth_object.question19_answer) + \
                                          int(rPatientGrowth_object.question28_answer)
        physical_ignorance_total_score = int(rPatientGrowth_object.question1_answer) + int(rPatientGrowth_object.question2_answer) + \
                                         int(rPatientGrowth_object.question4_answer) + int(rPatientGrowth_object.question6_answer) + \
                                         int(rPatientGrowth_object.question26_answer)

        if emotional_abuse_total_score >= 5 and emotional_abuse_total_score <= 25 and physical_abuse_total_score >= 5 and physical_abuse_total_score <= 25 \
                and sexual_abuse_total_score >= 5 and sexual_abuse_total_score <= 25 and emotional_ignorance_total_score >= 5 and emotional_ignorance_total_score <= 25 \
                and physical_ignorance_total_score >= 5 and physical_ignorance_total_score <= 25:
            object_flag = False
        else:
            object_flag = True
            emotional_abuse_total_score = None
            physical_abuse_total_score = None
            sexual_abuse_total_score = None
            emotional_ignorance_total_score = None
            physical_ignorance_total_score = None
    return emotional_abuse_total_score, physical_abuse_total_score, sexual_abuse_total_score, emotional_ignorance_total_score, physical_ignorance_total_score, object_flag


# 青少年生活事件量表
def AdolescentEvents_total_score(rPatientAdolescentEvents_object):
    if rPatientAdolescentEvents_object is None \
            or rPatientAdolescentEvents_object.question1_answer is None \
            or rPatientAdolescentEvents_object.question2_answer is None \
            or rPatientAdolescentEvents_object.question3_answer is None \
            or rPatientAdolescentEvents_object.question4_answer is None \
            or rPatientAdolescentEvents_object.question5_answer is None \
            or rPatientAdolescentEvents_object.question6_answer is None \
            or rPatientAdolescentEvents_object.question7_answer is None \
            or rPatientAdolescentEvents_object.question8_answer is None \
            or rPatientAdolescentEvents_object.question9_answer is None \
            or rPatientAdolescentEvents_object.question10_answer is None \
            or rPatientAdolescentEvents_object.question11_answer is None \
            or rPatientAdolescentEvents_object.question12_answer is None \
            or rPatientAdolescentEvents_object.question13_answer is None \
            or rPatientAdolescentEvents_object.question14_answer is None \
            or rPatientAdolescentEvents_object.question15_answer is None \
            or rPatientAdolescentEvents_object.question16_answer is None \
            or rPatientAdolescentEvents_object.question17_answer is None \
            or rPatientAdolescentEvents_object.question18_answer is None \
            or rPatientAdolescentEvents_object.question19_answer is None \
            or rPatientAdolescentEvents_object.question20_answer is None \
            or rPatientAdolescentEvents_object.question21_answer is None \
            or rPatientAdolescentEvents_object.question22_answer is None \
            or rPatientAdolescentEvents_object.question23_answer is None \
            or rPatientAdolescentEvents_object.question24_answer is None \
            or rPatientAdolescentEvents_object.question25_answer is None \
            or rPatientAdolescentEvents_object.question26_answer is None \
            or rPatientAdolescentEvents_object.question27_answer is None:
        object_flag = True
        total_score = None
    else:
        total_score = int(rPatientAdolescentEvents_object.question1_answer) + int(
            rPatientAdolescentEvents_object.question2_answer) + int(rPatientAdolescentEvents_object.question3_answer) + \
                      int(rPatientAdolescentEvents_object.question4_answer) + int(
            rPatientAdolescentEvents_object.question5_answer) + int(rPatientAdolescentEvents_object.question6_answer) + \
                      int(rPatientAdolescentEvents_object.question7_answer) + int(
            rPatientAdolescentEvents_object.question8_answer) + int(rPatientAdolescentEvents_object.question9_answer) + \
                      int(rPatientAdolescentEvents_object.question10_answer) + int(
            rPatientAdolescentEvents_object.question11_answer) + int(
            rPatientAdolescentEvents_object.question12_answer) + \
                      int(rPatientAdolescentEvents_object.question13_answer) + int(
            rPatientAdolescentEvents_object.question14_answer) + int(
            rPatientAdolescentEvents_object.question15_answer) + \
                      int(rPatientAdolescentEvents_object.question16_answer) + int(
            rPatientAdolescentEvents_object.question17_answer) + int(
            rPatientAdolescentEvents_object.question18_answer) + \
                      int(rPatientAdolescentEvents_object.question19_answer) + int(
            rPatientAdolescentEvents_object.question20_answer) + int(
            rPatientAdolescentEvents_object.question21_answer) + \
                      int(rPatientAdolescentEvents_object.question22_answer) + int(
            rPatientAdolescentEvents_object.question23_answer) + int(
            rPatientAdolescentEvents_object.question24_answer) + \
                      int(rPatientAdolescentEvents_object.question25_answer) + int(
            rPatientAdolescentEvents_object.question26_answer) + int(rPatientAdolescentEvents_object.question27_answer)
        if total_score >= 0 and total_score <= 135:
            object_flag = False
        else:
            object_flag = True
            total_score = None
    return total_score, object_flag


# 认知情绪调节
def CognitiveEmotion_total_score(rPatientCognitiveEmotion_object):
    if rPatientCognitiveEmotion_object is None \
            or rPatientCognitiveEmotion_object.question1_answer is None \
            or rPatientCognitiveEmotion_object.question2_answer is None \
            or rPatientCognitiveEmotion_object.question3_answer is None \
            or rPatientCognitiveEmotion_object.question4_answer is None \
            or rPatientCognitiveEmotion_object.question5_answer is None \
            or rPatientCognitiveEmotion_object.question6_answer is None \
            or rPatientCognitiveEmotion_object.question7_answer is None \
            or rPatientCognitiveEmotion_object.question8_answer is None \
            or rPatientCognitiveEmotion_object.question9_answer is None \
            or rPatientCognitiveEmotion_object.question10_answer is None \
            or rPatientCognitiveEmotion_object.question11_answer is None \
            or rPatientCognitiveEmotion_object.question12_answer is None \
            or rPatientCognitiveEmotion_object.question13_answer is None \
            or rPatientCognitiveEmotion_object.question14_answer is None \
            or rPatientCognitiveEmotion_object.question15_answer is None \
            or rPatientCognitiveEmotion_object.question16_answer is None \
            or rPatientCognitiveEmotion_object.question17_answer is None \
            or rPatientCognitiveEmotion_object.question18_answer is None \
            or rPatientCognitiveEmotion_object.question19_answer is None \
            or rPatientCognitiveEmotion_object.question20_answer is None \
            or rPatientCognitiveEmotion_object.question21_answer is None \
            or rPatientCognitiveEmotion_object.question22_answer is None \
            or rPatientCognitiveEmotion_object.question23_answer is None \
            or rPatientCognitiveEmotion_object.question24_answer is None \
            or rPatientCognitiveEmotion_object.question25_answer is None \
            or rPatientCognitiveEmotion_object.question26_answer is None \
            or rPatientCognitiveEmotion_object.question27_answer is None \
            or rPatientCognitiveEmotion_object.question28_answer is None \
            or rPatientCognitiveEmotion_object.question29_answer is None \
            or rPatientCognitiveEmotion_object.question30_answer is None \
            or rPatientCognitiveEmotion_object.question31_answer is None \
            or rPatientCognitiveEmotion_object.question32_answer is None \
            or rPatientCognitiveEmotion_object.question33_answer is None \
            or rPatientCognitiveEmotion_object.question34_answer is None \
            or rPatientCognitiveEmotion_object.question35_answer is None \
            or rPatientCognitiveEmotion_object.question36_answer is None:
        object_flag = True
        total_score = None
        blame_self = None
        blame_others = None
        meditation = None
        catastrophization = None
        accepted = None
        positive_refocus = None
        program_refocus = None
        positive_evaluation = None
        rational_analysis = None
    else:

        blame_self = int(rPatientCognitiveEmotion_object.question1_answer) + int(
            rPatientCognitiveEmotion_object.question2_answer) + \
                     int(rPatientCognitiveEmotion_object.question3_answer) + int(
            rPatientCognitiveEmotion_object.question4_answer)

        blame_others = int(rPatientCognitiveEmotion_object.question5_answer) + int(
            rPatientCognitiveEmotion_object.question6_answer) + \
                       int(rPatientCognitiveEmotion_object.question7_answer) + int(
            rPatientCognitiveEmotion_object.question8_answer)

        meditation = int(rPatientCognitiveEmotion_object.question9_answer) + int(
            rPatientCognitiveEmotion_object.question10_answer) + \
                     int(rPatientCognitiveEmotion_object.question11_answer) + int(
            rPatientCognitiveEmotion_object.question12_answer)

        catastrophization = int(rPatientCognitiveEmotion_object.question13_answer) + int(
            rPatientCognitiveEmotion_object.question14_answer) + \
                            int(rPatientCognitiveEmotion_object.question15_answer) + int(
            rPatientCognitiveEmotion_object.question16_answer)

        accepted = int(rPatientCognitiveEmotion_object.question17_answer) + int(
            rPatientCognitiveEmotion_object.question18_answer) + \
                   int(rPatientCognitiveEmotion_object.question19_answer) + int(
            rPatientCognitiveEmotion_object.question20_answer)

        positive_refocus = int(rPatientCognitiveEmotion_object.question21_answer) + int(
            rPatientCognitiveEmotion_object.question22_answer) + \
                           int(rPatientCognitiveEmotion_object.question23_answer) + int(
            rPatientCognitiveEmotion_object.question24_answer)

        program_refocus = int(rPatientCognitiveEmotion_object.question25_answer) + int(
            rPatientCognitiveEmotion_object.question26_answer) + \
                          int(rPatientCognitiveEmotion_object.question27_answer) + int(
            rPatientCognitiveEmotion_object.question28_answer)

        positive_evaluation = int(rPatientCognitiveEmotion_object.question29_answer) + int(
            rPatientCognitiveEmotion_object.question30_answer) + \
                              int(rPatientCognitiveEmotion_object.question31_answer) + int(
            rPatientCognitiveEmotion_object.question32_answer)

        rational_analysis = int(rPatientCognitiveEmotion_object.question33_answer) + int(
            rPatientCognitiveEmotion_object.question34_answer) + \
                            int(rPatientCognitiveEmotion_object.question35_answer) + int(
            rPatientCognitiveEmotion_object.question36_answer)

        total_score = blame_self + blame_others + meditation + catastrophization + accepted + positive_refocus + program_refocus + \
                      positive_evaluation + rational_analysis

        if blame_self >= 4 and blame_self <= 20 and blame_others >= 4 and blame_others <= 20 and meditation >= 4 and meditation <= 20 \
                and catastrophization >= 4 and catastrophization <= 20 and accepted >= 4 and accepted <= 20 and positive_refocus >= 4 and positive_refocus <= 20 \
                and program_refocus >= 4 and program_refocus <= 20 and positive_evaluation >= 4 and positive_evaluation <= 20 and rational_analysis >= 4 and rational_analysis <= 20 \
                and total_score >= 36 and total_score <= 180:
            object_flag = False
        else:
            object_flag = True
            total_score = None
            blame_self = None
            blame_others = None
            meditation = None
            catastrophization = None
            accepted = None
            positive_refocus = None
            program_refocus = None
            positive_evaluation = None
            rational_analysis = None
    return total_score, blame_self, blame_others, meditation, catastrophization, accepted, positive_refocus, program_refocus, positive_evaluation, rational_analysis, object_flag


# 简式父母
def SEmbu_total_score(rPatientSembu_object):
    if rPatientSembu_object is None \
            or rPatientSembu_object.question1_mother is None \
            or rPatientSembu_object.question2_mother is None \
            or rPatientSembu_object.question3_mother is None \
            or rPatientSembu_object.question4_mother is None \
            or rPatientSembu_object.question5_mother is None \
            or rPatientSembu_object.question6_mother is None \
            or rPatientSembu_object.question7_mother is None \
            or rPatientSembu_object.question8_mother is None \
            or rPatientSembu_object.question9_mother is None \
            or rPatientSembu_object.question10_mother is None \
            or rPatientSembu_object.question11_mother is None \
            or rPatientSembu_object.question12_mother is None \
            or rPatientSembu_object.question13_mother is None \
            or rPatientSembu_object.question14_mother is None \
            or rPatientSembu_object.question15_mother is None \
            or rPatientSembu_object.question16_mother is None \
            or rPatientSembu_object.question17_mother is None \
            or rPatientSembu_object.question18_mother is None \
            or rPatientSembu_object.question19_mother is None \
            or rPatientSembu_object.question20_mother is None \
            or rPatientSembu_object.question21_mother is None \
            or rPatientSembu_object.question1_father is None \
            or rPatientSembu_object.question2_father is None \
            or rPatientSembu_object.question3_father is None \
            or rPatientSembu_object.question4_father is None \
            or rPatientSembu_object.question5_father is None \
            or rPatientSembu_object.question6_father is None \
            or rPatientSembu_object.question7_father is None \
            or rPatientSembu_object.question8_father is None \
            or rPatientSembu_object.question9_father is None \
            or rPatientSembu_object.question10_father is None \
            or rPatientSembu_object.question11_father is None \
            or rPatientSembu_object.question12_father is None \
            or rPatientSembu_object.question13_father is None \
            or rPatientSembu_object.question14_father is None \
            or rPatientSembu_object.question15_father is None \
            or rPatientSembu_object.question16_father is None \
            or rPatientSembu_object.question17_father is None \
            or rPatientSembu_object.question18_father is None \
            or rPatientSembu_object.question19_father is None \
            or rPatientSembu_object.question20_father is None \
            or rPatientSembu_object.question21_father is None:
        object_flag = True
        refusal_mother = None
        refusal_father = None
        emotional_warmth_mother = None
        emotional_warmth_father = None
        overprotection_mother = None
        overprotection_father = None
    else:
        refusal_mother_total = int(rPatientSembu_object.question1_mother) + int(
            rPatientSembu_object.question2_mother) + int(rPatientSembu_object.question3_mother) + \
                               int(rPatientSembu_object.question4_mother) + int(
            rPatientSembu_object.question5_mother) + int(rPatientSembu_object.question6_mother)

        refusal_father_total = int(rPatientSembu_object.question1_father) + int(
            rPatientSembu_object.question2_father) + int(rPatientSembu_object.question3_father) + \
                               int(rPatientSembu_object.question4_father) + int(
            rPatientSembu_object.question5_father) + int(rPatientSembu_object.question6_father)

        emotional_warmth_mother_total = int(rPatientSembu_object.question7_mother) + int(
            rPatientSembu_object.question8_mother) + int(rPatientSembu_object.question9_mother) + \
                                        int(rPatientSembu_object.question10_mother) + int(
            rPatientSembu_object.question11_mother) + int(rPatientSembu_object.question12_mother) + \
                                        int(rPatientSembu_object.question13_mother)

        emotional_warmth_father_total = int(rPatientSembu_object.question7_father) + int(
            rPatientSembu_object.question8_father) + int(rPatientSembu_object.question9_father) + \
                                        int(rPatientSembu_object.question10_father) + int(
            rPatientSembu_object.question11_father) + int(rPatientSembu_object.question12_father) + \
                                        int(rPatientSembu_object.question13_father)

        overprotection_mother_total = int(rPatientSembu_object.question14_mother) + int(
            rPatientSembu_object.question15_mother) + int(rPatientSembu_object.question16_mother) + \
                                      int(rPatientSembu_object.question17_mother) + int(
            rPatientSembu_object.question18_mother) + int(rPatientSembu_object.question19_mother) + \
                                      int(rPatientSembu_object.question20_mother) + int(
            rPatientSembu_object.question21_mother)

        overprotection_father_total = int(rPatientSembu_object.question14_father) + int(
            rPatientSembu_object.question15_father) + int(rPatientSembu_object.question16_father) + \
                                      int(rPatientSembu_object.question17_father) + int(
            rPatientSembu_object.question18_father) + int(rPatientSembu_object.question19_father) + \
                                      int(rPatientSembu_object.question20_father) + int(
            rPatientSembu_object.question21_father)

        if refusal_mother_total >= 6 and refusal_mother_total <= 24 and refusal_father_total >= 6 and refusal_father_total <= 24 \
                and emotional_warmth_mother_total >= 7 and emotional_warmth_mother_total <= 28 and emotional_warmth_father_total >= 7 \
                and emotional_warmth_father_total <= 28 and overprotection_mother_total >= 8 and overprotection_mother_total <= 32 \
                and overprotection_father_total >= 8 and overprotection_father_total <= 32:
            object_flag = False
            refusal_mother = refusal_mother_total / 6
            refusal_father = refusal_father_total / 6
            emotional_warmth_mother = emotional_warmth_mother_total / 7
            emotional_warmth_father = emotional_warmth_father_total / 7
            overprotection_mother = overprotection_mother_total / 8
            overprotection_father = overprotection_father_total / 8
        else:
            object_flag = True
            refusal_mother = None
            refusal_father = None
            emotional_warmth_mother = None
            emotional_warmth_father = None
            overprotection_mother = None
            overprotection_father = None
    return refusal_mother, refusal_father, emotional_warmth_mother, emotional_warmth_father, overprotection_mother, overprotection_father, object_flag


# 自动思维问卷
def ATQ_total_score(rPatientAtq_object):
    if rPatientAtq_object is None \
            or rPatientAtq_object.question1_answer is None \
            or rPatientAtq_object.question2_answer is None \
            or rPatientAtq_object.question3_answer is None \
            or rPatientAtq_object.question4_answer is None \
            or rPatientAtq_object.question5_answer is None \
            or rPatientAtq_object.question6_answer is None \
            or rPatientAtq_object.question7_answer is None \
            or rPatientAtq_object.question8_answer is None \
            or rPatientAtq_object.question9_answer is None \
            or rPatientAtq_object.question10_answer is None \
            or rPatientAtq_object.question11_answer is None \
            or rPatientAtq_object.question12_answer is None \
            or rPatientAtq_object.question13_answer is None \
            or rPatientAtq_object.question14_answer is None \
            or rPatientAtq_object.question15_answer is None \
            or rPatientAtq_object.question16_answer is None \
            or rPatientAtq_object.question17_answer is None \
            or rPatientAtq_object.question18_answer is None \
            or rPatientAtq_object.question19_answer is None \
            or rPatientAtq_object.question20_answer is None \
            or rPatientAtq_object.question21_answer is None \
            or rPatientAtq_object.question22_answer is None \
            or rPatientAtq_object.question23_answer is None \
            or rPatientAtq_object.question24_answer is None \
            or rPatientAtq_object.question25_answer is None \
            or rPatientAtq_object.question26_answer is None \
            or rPatientAtq_object.question27_answer is None \
            or rPatientAtq_object.question28_answer is None \
            or rPatientAtq_object.question29_answer is None \
            or rPatientAtq_object.question30_answer is None:
        object_flag = True
        total_score = None
    else:
        total_score = int(rPatientAtq_object.question1_answer) + int(rPatientAtq_object.question2_answer) + int(
            rPatientAtq_object.question3_answer) + \
                      int(rPatientAtq_object.question4_answer) + int(rPatientAtq_object.question5_answer) + int(
            rPatientAtq_object.question6_answer) + \
                      int(rPatientAtq_object.question7_answer) + int(rPatientAtq_object.question8_answer) + int(
            rPatientAtq_object.question9_answer) + \
                      int(rPatientAtq_object.question10_answer) + int(rPatientAtq_object.question11_answer) + int(
            rPatientAtq_object.question12_answer) + \
                      int(rPatientAtq_object.question13_answer) + int(rPatientAtq_object.question14_answer) + int(
            rPatientAtq_object.question15_answer) + \
                      int(rPatientAtq_object.question16_answer) + int(rPatientAtq_object.question17_answer) + int(
            rPatientAtq_object.question18_answer) + \
                      int(rPatientAtq_object.question19_answer) + int(rPatientAtq_object.question20_answer) + int(
            rPatientAtq_object.question21_answer) + \
                      int(rPatientAtq_object.question22_answer) + int(rPatientAtq_object.question23_answer) + int(
            rPatientAtq_object.question24_answer) + \
                      int(rPatientAtq_object.question25_answer) + int(rPatientAtq_object.question26_answer) + int(
            rPatientAtq_object.question27_answer) + \
                      int(rPatientAtq_object.question28_answer) + int(rPatientAtq_object.question29_answer) + int(
            rPatientAtq_object.question30_answer)
        if total_score >= 30 and total_score <= 150:
            object_flag = False
        else:
            object_flag = True
            total_score = None
    return total_score, object_flag


def PHQ_total_score(RPatientPhq_obj):
    total_score = 0
    for each_score in RPatientPhq_obj.__dict__:
        if len(each_score.split('_')) > 1:
            if each_score.split('_')[1] == 'answer':
                total_score = total_score + int(getattr(RPatientPhq_obj, each_score))
    return total_score


def GAD_total_score(RPatientGad_obj):
    total_score = 0
    for each_score in RPatientGad_obj.__dict__:
        if len(each_score.split('_')) > 1:
            if each_score.split('_')[1] == 'answer':
                total_score = total_score + int(getattr(RPatientGad_obj, each_score))
    return total_score


def PSS_total_score(RPatientPss_obj):
    for each_score in RPatientPss_obj.__dict__:
        if each_score is None:
            total_score = None
            break
    else:
        total_score= int(RPatientPss_obj.question1_answer) + int(RPatientPss_obj.question2_answer)+\
                     int(RPatientPss_obj.question3_answer) + int(RPatientPss_obj.question8_answer)+\
                     int(RPatientPss_obj.question11_answer) + int(RPatientPss_obj.question14_answer)+\
                     int(RPatientPss_obj.question4_answer) + int(RPatientPss_obj.question5_answer)+ \
                     int(RPatientPss_obj.question6_answer) + int(RPatientPss_obj.question7_answer) + \
                     int(RPatientPss_obj.question9_answer) + int(RPatientPss_obj.question10_answer) + \
                     int(RPatientPss_obj.question12_answer) + int(RPatientPss_obj.question13_answer) -14
    if total_score<=0 and total_score>=56:
        total_score=None
    return total_score


def ISI_total_score(RPatientInsomnia_obj):
    total_score = 0
    for each_score in RPatientInsomnia_obj.__dict__:
        if len(each_score.split('_')) > 1:
            if each_score.split('_')[1] == 'answer':
                total_score = total_score + int(getattr(RPatientInsomnia_obj, each_score))
    return total_score
