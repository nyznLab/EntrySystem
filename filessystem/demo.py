# 文件系统数据分发
import njftools as njt
import fconfig as conf
njt.copyToFileSystemRawData(r'F:\Raw\raw_data',conf.nanjingPath,'dicom')
njt.copyToFileSystemPreprocess(r'F:\files1',conf.nanjingPath)