#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：tools
@File ：get_data.py
@IDE  ：PyCharm
@Author ：skj
@Date ：6/2/21 2:29 PM
'''
from Utils import getIdNameFromString,getIdAndSession,packingIdAndSession
from exception import BussinessException,handle_exception
import fconfig as conf
import configclass as confclass
import os




def base_getData(patient_list,base_path,data_type,prefix,suffix):
    '''

    :param patient_list:
    :param base_path:基础路径
    :param data_type: 数据类型，reho，alff，fc等
    :param prefix:文件名前缀，例如ReHoMap，smRehoMap，szReHoMap等
    :param suffix:后缀，例如nii，csv，txt
    :return:

    '''
    path = base_path
    file_list = []
    # 遍历病人列表
    for patient in patient_list:
        # 进行病人id校验
        standard_id = getIdNameFromString(patient)
        if standard_id is None:
            handle_exception(BussinessException(f'===病人id：{patient}不合法，请确认修改后重新执行=='))
        else:
            id,session = getIdAndSession(standard_id)
            sub_id, sub_session = packingIdAndSession(id,session)
            patient_path = f'{path}/{sub_id}/{sub_session}'
            # 进行文件夹是否存在校验
            if not os.path.exists(patient_path):
                 handle_exception(BussinessException(f'病人{patient} 数据不存在'))
                 continue
            # 进行数据文件是否存在校验，并进行文件路径获取
            file_path = f'{patient_path}/{data_type}/{prefix}_{standard_id}.{suffix}'
          
            if not os.path.exists(file_path):
                handle_exception(BussinessException(f'病人{patient},{data_type} 数据不存在'))
            else:
                file_list.append(file_path)
    return file_list

def get_dicom(patient_list,city_type,list_type='sms5_bold_500ms_rest64'):
    if city_type == 'shenyang':
        city_path = conf.shenyangPath
    if city_type == 'nanjing':
        city_path = conf.nanjingPath
    path = city_path+'/raw_data'
    data_type='dicom'
    file_list = []
    # 遍历病人列表
    for patient in patient_list:
        # 进行病人id校验
        standard_id = getIdNameFromString(patient)
        if standard_id is None:
            handle_exception(BussinessException(f'===病人id：{patient}不合法，请确认修改后重新执行=='))
        else:
            id, session = getIdAndSession(standard_id)
            sub_id, sub_session = packingIdAndSession(id, session)
            patient_path = f'{path}/{sub_id}/{sub_session}'
            # 进行文件夹是否存在校验
            if not os.path.exists(patient_path):
                handle_exception(BussinessException(f'病人{patient} 数据不存在'))
                continue
            # 进行数据文件是否存校在验，并进行文件路径获取
            file_path = f'{patient_path}/{data_type}/{list_type}'
            if (not os.path.exists(file_path)) or (len(os.listdir(file_path)) == 0) :
                handle_exception(BussinessException(f'病人{patient},{list_type} 数据不存在'))
            else:
                file_list.append(file_path)
    return file_list


def get_reho(patient_list,city_type,reho_type='smReHo'):

    '''
    获取病人reho文件路径
    :param patient_list:
    :param city_type: 南京还是沈阳
    :param reho_type: reho数据类型(ReHo,smReHo,sReHo,mReHo,szReHo,zReHo)
    :return:文件路径列表
    '''
    if city_type == 'shenyang':
        city_path = conf.shenyangPath
    if city_type == 'nanjing':
        city_path = conf.nanjingPath
    path = city_path+'/preprocess'
    if reho_type not in confclass.preprocessDict.ReHo_Types:
        raise BussinessException(f'数据类型:{reho_type} 输入错误')
    file_list=base_getData(patient_list, path, confclass.preprocessDict.REHO, reho_type+'Map', 'nii')
    return file_list

def get_falff(patient_list,city_type,falff_type='fALFF'):

    '''
    获取病人falff文件路径
    :param patient_list:
    :param city_type: 南京还是沈阳
    :param falff_type: falff数据类型(fALFF,mfALFF,zfALFF)
    :return:文件路径列表
    '''
    if city_type == 'shenyang':
        city_path = conf.shenyangPath
    if city_type == 'nanjing':
        city_path = conf.nanjingPath
    path = city_path+'/preprocess'
    if falff_type not in confclass.preprocessDict.fALFF_Types:
        raise BussinessException(f'数据类型:{falff_type} 输入错误')
    file_list = base_getData(patient_list, path, confclass.preprocessDict.fALFF, falff_type+'Map', 'nii')
    return file_list

def get_alff(patient_list,city_type,alff_type='mALFF'):

    '''
    获取病人alff文件路径
    :param patient_list:
    :param city_type: 南京还是沈阳
    :param alff_type: alff数据类型(ALFF,mALFF,zALFF)
    :return:文件路径列表
    '''
    if city_type == 'shenyang':
        city_path = conf.shenyangPath
    if city_type == 'nanjing':
        city_path = conf.nanjingPath
    path = city_path+'/preprocess'
    if alff_type not in confclass.preprocessDict.ALFF_Types:
        raise BussinessException(f'数据类型:{alff_type} 输入错误')
    file_list = base_getData(patient_list, path, confclass.preprocessDict.ALFF, alff_type+'Map', 'nii')
    return file_list

def get_roi_fc(patient_list,city_type,roi_fc_prefix_type='ROICorrelation_FisherZ',roi_fc_suffix_type='mat'):
    '''
        获取病人fc文件路径(这里的fc指的是ROISignals_FunImgARWSDCF文件夹）
        :param patient_list:
        :param city_type: 南京还是沈阳
        :param roi_fc_prefix_type: ROISignals_FunImgARWSDCF数据类型(ROI_OrderKey,ROICorrelation_FisherZ,ROICorrelation，ROISignals)
        :param fc_suffix_type:文件格式类型（mat,tsv,txt)
        :return:文件路径列表
        '''
    if city_type == 'shenyang':
        city_path = conf.shenyangPath
    if city_type == 'nanjing':
        city_path = conf.nanjingPath
    path = city_path + '/preprocess'
    suffix_types = [ 'tsv','mat','txt']
    if roi_fc_prefix_type not in confclass.preprocessDict.ROI_FC_Types or roi_fc_suffix_type not in suffix_types:
        raise BussinessException(f'数据类型,输入错误')
    elif roi_fc_prefix_type==confclass.preprocessDict.ROI_FC_Types[0] and roi_fc_suffix_type != suffix_types[0]:
        raise BussinessException(f'数据类型{confclass.preprocessDict.ROI_FC_Types[0]},后缀输入错误')
    elif roi_fc_prefix_type in confclass.preprocessDict.ROI_FC_Types[1:] and roi_fc_suffix_type == suffix_types[0]:
        raise BussinessException(f'数据类型{confclass.preprocessDict.ROI_FC_Types[0]},后缀输入错误')
    else:
        file_list = base_getData(patient_list, path, confclass.preprocessDict.ROI_FC, roi_fc_prefix_type , roi_fc_suffix_type)
    return file_list

def get_fc(patient_list,city_type,fc_prefix_type='FC',fc_suffix_type='nii'):

    '''
    获取病人fc文件路径(这里的fc指的是FC_FunImgARWSDCF文件夹）
    :param patient_list:
    :param city_type: 南京还是沈阳
    :param fc_type: fc数据类型['FC','ROI_FC','ROI_Orderkey_FC','zFC']
    :return:文件路径列表
    '''
    if city_type == 'shenyang':
        city_path = conf.shenyangPath
    if city_type == 'nanjing':
        city_path = conf.nanjingPath
    path = city_path+'/preprocess'
    suffix_types = ['nii','tsv', 'mat', 'txt']
    if fc_prefix_type not in confclass.preprocessDict.FC_Types or fc_suffix_type not in suffix_types:
        raise BussinessException(f'数据类型:输入错误')
    elif fc_prefix_type in confclass.preprocessDict.FC_Types[:2] and fc_suffix_type != suffix_types[0]:
        raise BussinessException(f'数据类型:{fc_prefix_type} .后缀输入错误')
    elif fc_prefix_type==confclass.preprocessDict.FC_Types[2] and fc_suffix_type != suffix_types[1]:
        raise BussinessException(f'数据类型:{fc_prefix_type} .后缀输入错误')
    elif fc_prefix_type == confclass.preprocessDict.FC_Types[3] and fc_suffix_type != suffix_types[2:]:
        raise BussinessException(f'数据类型:{fc_prefix_type} .后缀输入错误')
    else:
        file_list = base_getData(patient_list, path, confclass.preprocessDict.FC, fc_prefix_type + 'Map', fc_suffix_type)
    return file_list


# try:
#     patient_list = get_fc(['NN_00000001_S001'],'nanjing','ROI_Orderkey_FC','tsv')
#     print(patient_list)
# except Exception as e:
#     print(e.message)



