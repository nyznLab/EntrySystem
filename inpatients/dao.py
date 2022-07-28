from inpatients.models import *
# 根据inpatient_id获取对象
def get_inpatient_info_byPK(inpatient_id):
    res = BInpatientInfo.objects.filter(pk = inpatient_id)
    print(res.count())
    if res.exists():
        return res[0]
    return None
def del_medical_advice_by_inpatientid(inpatient_id):
    res = BInpatientMedicalAdvice.objects.filter(inpatient_id = inpatient_id)
    if res.exists():
        res.delete()

def add_medical_advice(bInpatientMedicalAdvice):
    bInpatientMedicalAdvice.save()
    return bInpatientMedicalAdvice.id

def get_in_time_by_patientid(patient_id):
    res = BInpatientInfo.objects.filter(patient_id = patient_id).order_by('-in_time')
    if not res.exists():
        return 1
    else:
        return res[0].in_time+1
# 根据inpatient_id获取所有医嘱信息
def get_mecical_advice(inpatient_id):
    res = BInpatientMedicalAdvice.objects.filter(inpatient_id = inpatient_id)
    if not res.exists():
        return None,0
    else:
        return res,1

# 获取所有住院患者信息
def get_all_inpatient_info(types):
    # 进行联合查询,返回个人基本信息以及住院患者信息等
    res = BInpatientInfo.objects.all().select_related('patient').filter(inpatient_state__in = types)
    if res.exists():
        return res
    return None

# 获取住院患者详细信息
def get_inpatient_detail(inpatient_id):
    res = BInpatientInfo.objects.all().select_related('patient').filter(pk = inpatient_id)
    if res.exists():
        return res[0]
    return None

# 删除住院患者信息
def del_inpatient_by_pk(inpatient_id):
    res = BInpatientInfo.objects.filter(pk=inpatient_id)
    res.delete()
# 获取meidical字典表信息
def get_medical_dict():
    medical_dict = {}
    res = DMedicalAdvice.objects.all().values_list('medical_name','type')
    for ele in res:
        medical_dict[ele[0]] = ele[1]
    return medical_dict


# 添加一条数据到住院数据流水表
def add_inpatient_data(inpatient_id, data_type, file=None, data_date=None):
    bInpatientData = BInpatientData()
    bInpatientData.inpatient_id = inpatient_id
    bInpatientData.data_type = data_type
    bInpatientData.data_date = data_date
    bInpatientData.file = file
    bInpatientData.save()
    