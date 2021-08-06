# conding=utf8
import os
import time
import njftools as njt
import fconfig as conf

def judge_time_file(path, file, update_time):
    start_time = time.mktime(time.strptime('2020-09-12 00:00:00', "%Y-%m-%d %H:%M:%S"))
    end_time = time.mktime(time.strptime('2020-10-21 00:00:00', "%Y-%m-%d %H:%M:%S"))
    # print(start_time , update_time , end_time)
    if start_time < update_time < end_time:
        return True
    return False

data_list = []

path=r"F:\Raw\raw_data"
g = os.listdir(path)
#print(g)
for file_name in g:
    local_time = os.stat(os.path.join(path, file_name)).st_mtime
    #os.stat()方法用于在给定的路径上执行一个系统stat的调用，os.stat().st_mtime：返回的是最后一次修改的时间；
    if judge_time_file(path, file_name, local_time):
        data_list.append(file_name)
        # data_list.append(
        #         [os.path.join(path, file_name), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(local_time))])
#data_list.sort(key=lambda x: x[1])
print(data_list)

njt.copyToFileSystemRawData(path,conf.nanjingPath,'dicom',data_list)










# for path, dir_list, file_list in g:
#     print(path)
#     print(dir_list)
#     print(file_list)
#     for file_name in file_list:
#         local_time = os.stat(os.path.join(path, file_name)).st_mtime
#         if judge_time_file(path, file_name, local_time):
#             data_list.append(
#                 [os.path.join(path, file_name), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(local_time))])
# data_list.sort(key=lambda x: x[1])
# print(*data_list, sep='\n')