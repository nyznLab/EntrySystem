# 文件系统数据分发
import njftools as njt
import fconfig as conf
#njt.copyToFileSystemRawData(r'F:\Raw\raw_data',conf.nanjingPath,'dicom',['NN_00000001_S001'])
njt.copyToFileSystemPreprocess(r'F:\files1',conf.nanjingPath,['NN_00000001_S001'])

#文件路径的获取
# try:
#     patient_list = get_fc(['NN_00000001_S001'],'nanjing','ROI_Orderkey_FC','tsv')
#     print(patient_list)
# except Exception as e:
#     print(e.message)
# import get_data as get
# print(get.get_dicom(['NN_00000001_S001'],'nanjing',list_type=' gre_field_mapping_rest64_2'))
# print(get.get_reho(['NN_00000001_S001'],'nanjing',reho_type='smReHo'))
# print(get.get_falff(['NN_00000321_S001'],'nanjing',falff_type='fALFF'))
# print(get.get_alff(['NN_00000001_S001'],'nanjing',alff_type='mALFF'))
# print(get.get_roi_fc(['NN_00000001_S001'],'nanjing',roi_fc_prefix_type='ROICorrelation',roi_fc_suffix_type='txt'))
# print(get.get_fc(['NN_00000001_S001'],'nanjing',fc_prefix_type='FC',fc_suffix_type='nii'))
