import patients.models as models


# 分配patient_id
def patient_Id_assignment():
    patient_res = models.BPatientBaseInfo.objects.order_by('-id')
    if patient_res.count() == 0:
        return 1
    patient_id = patient_res[0].id + 1
    return patient_id


# 分配复扫id
def patient_session_id_assignment(patient_id):
    patient_session_res = models.DPatientDetail.objects.filter(patient_id=patient_id).order_by('-session_id')
    if patient_session_res.count() == 0:
        session_id = 1
    else:
        session_id = patient_session_res[0].session_id + 1
    standard_id = generate_standard_id(patient_id, session_id)
    return patient_id, session_id, standard_id


# 生成标准id
def generate_standard_id(patient_id, session_id):
    standard_id = 'NN_' + str(patient_id).zfill(8) + '_S' + str(session_id).zfill(3)
    return standard_id


# 根据标准id拆分为patient_id，以及session_id
def getIdAndSession(name):
    """
    获取id，session信息
    :param name: 文件名NN_00000001_S001
    :return: id和session信息,返回sub_1 ses_1
    """
    try:
        eles = name.split('_')
        id = int(eles[1])
        session = int(eles[2][1:])
        return str(id), str(session)
    except Exception:
        print("==病人id格式错误==")


def pack_patient_id(patient_id):
    return 'NN_' + str(patient_id).zfill(8)
