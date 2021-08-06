import Utils
import os
import time
import njftools as njt
import fconfig as conf
g = os.walk(r"F:\files1")
def judge_time_file(path, file, update_time):
  start_time = time.mktime(time.strptime('2020-06-12 00:00:00', "%Y-%m-%d %H:%M:%S"))
  end_time  = time.mktime(time.strptime('2020-09-23 00:00:00', "%Y-%m-%d %H:%M:%S"))
  # print(start_time , update_time , end_time)
  if start_time < update_time < end_time:
    return True
  return False

data_list = []

for path, dir_list, file_list in g:
  for file_name in file_list:
    local_time = os.stat(os.path.join(path, file_name)).st_mtime
    if judge_time_file(path, file_name, local_time):
      data_list.append([os.path.join(path, file_name)])

print(data_list)
name_list=[]
for i in range(len(data_list)):
    for j in range(len(data_list[i])):
        name= Utils.getIdNameFromString(data_list[i][j])
        name_list.append(name)
print(name_list)
name_list = list(set(name_list))
print(name_list)
njt.copyToFileSystemPreprocess(r'F:\files1',conf.nanjingPath,name_list)

