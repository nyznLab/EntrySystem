import patients.models as patients_models
import patients.dao as patients_dao
import scales.models as scales_models
import scales.dao as scales_dao

patient_session_id_min = 0
patient_session_id_max = 1500
scales_id_max = 32

for patient_session_id in range(patient_session_id_min,patient_session_id_max):
    patient_scales_list = scales_models.RPatientScales.objects.filter(patient_session_id=patient_session_id).all()
    for scales_id in range(1,scales_id_max+1):
        patient_scales_del_list = []
        patient_scales_save =[]
        del_count = 0
        del_num = 0
        patient_scales_list_same = patient_scales_list.filter(scale_id=scales_id).all()
        # 统计相同结果数量
        count = 0
        for temp in patient_scales_list_same:
            count += 1
        if count >2 :
            # 结果不止一条，如果有state=1的记录，删掉其他的
            for i in range(0,count):
                patient_scales_list_same_state = patient_scales_list_same.filter(state=1).all()
                # 如果有state = 1的记录，删掉其他的
                if patient_scales_list_same_state:
                    patient_scales_save = patient_scales_list_same_state.first()
                    del_count = 0
                    for temp in patient_scales_list_same:
                        if temp.id != patient_scales_save.id:
                            patient_scales_del_list.append(temp.id)
                            del_count += 1
                    # 删除
                    for id in patient_scales_del_list:
                        patient_scales_list_same.filter(id=id).delete()
                else:
                    # 如果没有，删至1条
                    patient_scales_save = patient_scales_list_same.first()
                    del_count = 0
                    for temp in patient_scales_list_same:
                        if temp.id != patient_scales_save.id:
                            patient_scales_del_list.append(temp.id)
                            del_count += 1
                    for id in patient_scales_del_list:
                        patient_scales_list_same.filter(id=id).delete()
        # 没啥用的分支，纯测试
        elif count == 2:
            if patient_scales_list_same[0].state == 1:
                patient_scales_list_same[1].delete()
            elif patient_scales_list_same[1].state == 1:
                patient_scales_list_same[0].delete()
            else:
                patient_scales_list_same[1].delete()




