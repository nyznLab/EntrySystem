# 文件系统数据分发
import njftools as njt
import fconfig as conf
#njt.copyToFileSystemRawData(r'/root/Desktop/Distribution_Test/RAWDATA',conf.nanjingPath,'dicom')

#njt.copyToFileSystemPreprocess(r'/root/Desktop/Distribution_Test/PREPROCESS',conf.nanjingPath)

import get_data as get
print(get.get_dicom(['NN_00000355_S001'],'nanjing',list_type='gre_field_mapping_rest64_2'))
print(get.get_reho(['NN_00000125_S001'],'nanjing',reho_type='smReHo'))
print(get.get_alff(['NN_00000155_S002'],'nanjing',alff_type='mALFF'))
print(get.get_falff(['NN_00000025_S001'],'nanjing',falff_type='fALFF'))
print(get.get_roi_fc(['NN_00000654_S002'],'nanjing',roi_fc_prefix_type='ROICorrelation_FisherZ',roi_fc_suffix_type='mat'))
