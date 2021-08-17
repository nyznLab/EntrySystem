# 文件系统数据分发
import njftools as njt
import fconfig as conf

#njt.copyToFileSystemRawData(r'/root/data/anonymized_data',conf.nanjingPath,'dicom')
#njt.copyToFileSystemPreprocess(r'/root/data/results/Results',conf.nanjingPath,)
#njt.copyToFileSystemRawData(r'F:\Raw\raw_data',conf.nanjingPath,'dicom',['NN_00000346_S001'])
import get_data as get
from filessystem.copy_file import copyFile

path1=get.get_dicom(['NN_00000001_S001','NN_00000080_S004'],'nanjing')
path2=get.get_alff(['NN_00000001_S001','NN_00000002_S001'],'nanjing')
path3=get.get_falff(['NN_00000001_S001','NN_00000002_S001'],'nanjing')
path4=get.get_reho(['NN_00000001_S001','NN_00000002_S001'],'nanjing')
path5=get.get_roi_fc(['NN_00000001_S001','NN_00000002_S001'],'nanjing')


copyFile(path1,r'E:\file_test')
copyFile(path2,r'E:\file_test')
copyFile(path3,r'E:\file_test')
copyFile(path4,r'E:\file_test')
copyFile(path5,r'E:\file_test')