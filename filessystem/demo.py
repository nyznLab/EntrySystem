# 文件系统数据分发
import njftools as njt
import fconfig as conf

njt.copyToFileSystemRawData(r'/root/data/anonymized_data',conf.nanjingPath,'dicom')
njt.copyToFileSystemPreprocess(r'/root/data/results/Results',conf.nanjingPath,)

