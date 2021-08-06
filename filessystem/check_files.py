import os
import fconfig as conf
import configclass as confclass
from Utils import getIdNameFromString,getIdAndSession,packingIdAndSession
from exception import BussinessException,handle_exception

'''
检查dicom_quality:
序列不确定，先检查三个的：sms5_bold_500ms_rest64 960 ；t1_mprage_sag_iso_mww64CH 192 ；sms4_diff_2mm_PA_HARDI64 70 ；
'''
def check_dicom_save (patient_path,standard_id):
    data_type='dicom'
    flag=0
    file_path = f'{patient_path}/{data_type}'
    if not os.path.exists(file_path):
        handle_exception(BussinessException(f'病人{standard_id}:{data_type} 数据不存在'))
    elif (len(os.listdir(file_path)) != 0):
        flag=1
    return flag

def check_dicom_quality (patient_path,standard_id):
    data_type = 'dicom'
    count=0
    file_types=['sms5_bold_500ms_rest64','t1_mprage_sag_iso_mww64CH','sms4_diff_2mm_PA_HARDI64']
    number_types=[960,192,70]
    path = f'{patient_path}/{data_type}'
    if check_dicom_save(patient_path,standard_id):
        for i in range(3) :
            file_path=f'{path}/{file_types[i]}'
            if not os.path.exists(file_path):
                handle_exception(BussinessException(f'病人{standard_id} :{file_types[i]}数据不存在'))
            elif (len(os.listdir(file_path))==number_types[i]):
                count+=1
            else:
                handle_exception(BussinessException(f'病人{standard_id}:{file_types[i]} 数据不完整'))
    if count==3:
        return 1
    else:
        return 0


#检查reho文件夹六种reho文件是否均存在。
def check_reho_arwdcf_save(patient_path,standard_id):
    # reho_type=['ReHo','smReHo','sReHo','mReHo','szReHo','zReHo']
    count=0
    for type in confclass.preprocessDict.ReHo_Types:
        prefix=type+'Map'
        suffix='nii'
        file_path=f'{patient_path}/{confclass.preprocessDict.REHO}/{prefix}_{standard_id}.{suffix}'
        if not os.path.exists(file_path):
            handle_exception(BussinessException(f'病人{standard_id},{type} 数据不存在'))
        else:
            count+=1
    if (count==6):
        return 1
    else:
        return 0

#检查alff文件夹下三种文件类型是否均存在。
def check_alff_arwsd_save(patient_path,standard_id):
    #alff_type=['ALFF','mALFF','zALFF']
    count=0
    for type in confclass.preprocessDict.ALFF_Types:
        prefix=type+'Map'
        suffix='nii'
        file_path=f'{patient_path}/{confclass.preprocessDict.ALFF}/{prefix}_{standard_id}.{suffix}'
        if not os.path.exists(file_path):
            handle_exception(BussinessException(f'病人{standard_id},{type} 数据不存在'))
        else:
            count+=1
    if (count == 3):
        return 1
    else:
        return 0

#检查falff文件夹下三种文件类型是否均存在。
def check_falff_arwsd_save(patient_path,standard_id):
    #alff_type=['fALFF','mfALFF','zfALFF']
    count=0
    for type in confclass.preprocessDict.fALFF_Types:
        prefix=type+'Map'
        suffix='nii'
        file_path=f'{patient_path}/{confclass.preprocessDict.fALFF}/{prefix}_{standard_id}.{suffix}'
        if not os.path.exists(file_path):
            handle_exception(BussinessException(f'病人{standard_id},{type} 数据不存在'))
        else:
            count+=1
    if (count == 3):
        return 1
    else:
        return 0

#检查ROISignals_FunImgARWSDCF文件夹下三种文件类型和不同的文件格式是否均存在.
def check_fc_arwsdcf_save(patient_path,standard_id):
    #检查文件存在与否
    prefix_Types = ['ROI_OrderKey','ROICorrelation_FisherZ','ROICorrelation','ROISignals']
    suffix_Types = ['mat','txt']
    for prefix in prefix_Types[1:]:
        for suffix in suffix_Types:
            flag_0=False
            file_path= f'{patient_path}/{confclass.preprocessDict.ROI_FC}/{prefix}_{standard_id}.{suffix}'
            if not os.path.exists(file_path):
                handle_exception(BussinessException(f'病人{prefix}_{standard_id}.{suffix}文件数据不存在'))
            else:
                flag_0=True

    #检查ROI_Orderkey.tsv存在
        flag_1 = False
        prefix_ROI_Orderkey = 'ROI_Orderkey'
        suffix_ROI_Orderkey='tsv'
        file_path_ROI_Orderkey = f'{patient_path}/{confclass.preprocessDict.ROI_FC}/{prefix_ROI_Orderkey}_{standard_id}.{suffix_ROI_Orderkey}'
        if not os.path.exists(file_path_ROI_Orderkey):
            handle_exception(BussinessException(f'病人ROI_Orderkey_{standard_id}.tsv数据不存在'))
        else:
            flag_1 = True

    if (flag_0 and flag_1):
        return 1
    else:
        return 0

def check_voxel_wose_fc():
    #pass
    return 0
def check_audio_save():
    # pass
    return 0
def check_video_save():
    # pass
    return 0


def check_file_save(patient_list,city_type):
    '''
    检查文件是否存在：
        patient_list:
        city_type: 南京或沈阳
        data_type: 数据类型，reho，alff，fc,fallff等
    '''
    if city_type == 'shenyang':
        city_path = conf.shenyangPath
    if city_type == 'nanjing':
        city_path = conf.nanjingPath
    path_pre = city_path + '/preprocess'
    path_raw = city_path + '/raw_data'
    # 遍历病人列表
    for patient in patient_list:
        # 进行病人id校验
        standard_id = getIdNameFromString(patient)
        if standard_id is None:
            handle_exception(BussinessException(f'===病人id：{patient}不合法，请确认修改后重新执行=='))
        else:
            id, session = getIdAndSession(standard_id)
            sub_id, sub_session = packingIdAndSession(id, session)
            patient_path_pre = f'{path_pre}/{sub_id}/{sub_session}'
            patient_path_raw = f'{path_raw}/{sub_id}/{sub_session}'
            # 进行文件夹是否存在校验
            if not os.path.exists(patient_path_pre):
                handle_exception(BussinessException(f'病人{patient} 数据不存在'))
                continue
            # 进行数据文件是否存在校验
            dicom_save_flag = check_dicom_save(patient_path_raw, standard_id)
            dicom_quality_flag=check_dicom_quality(patient_path_raw, standard_id)
            reho_save_flag=check_reho_arwdcf_save(patient_path_pre,standard_id)
            fc_save_flag = check_fc_arwsdcf_save(patient_path_pre, standard_id)
            falff_save_flag = check_falff_arwsd_save(patient_path_pre, standard_id)
            alff_save_flag = check_alff_arwsd_save(patient_path_pre, standard_id)
            return dicom_save_flag,dicom_quality_flag,reho_save_flag,fc_save_flag,falff_save_flag,alff_save_flag

            #print( dicom_save_flag,dicom_quality_flag,reho_save_flag,alff_save_flag,falff_save_flag,fc_save_flag)



#检查
#check_file_save(['NN_00000001_S001'],'nanjing')

