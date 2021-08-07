import os
# list=[]
# path1=r'F:\Raw\raw_data\NN_00000109_S001\10 gre_field_mapping_rest64'
# list.append(path1)
# path2=r'F:\Raw\raw_data\NN_00000109_S001\10 gre_field_mapping_rest64'
# for i in range(len(list)):
#     if path2==list[i]:
#         list[i]=list[i]+'_1'
#         path2=path2+'_2'
#         list.append(path2)
# print(list)

# path=r'F:\test3\nanjing\raw_data\sub_176\ses_2\dicom\ gre_field_mapping_rest64'
# print(len(os.listdir(path)))
#from filessystem.exception import handle_exception

# patient_list=['12','45','23']
# patientsIds=['12','11','33','222','343']
# for i in range(len(patient_list)):
#     for patient in patientsIds:
#         if (patient_list[i] == patient):
#             continue
#         else:
#             print('==病人id：{patient}文件不存在，无法分发===')
#             patient_list.remove(patient)
# print(patient_list)


#import os
#path1=r'E:\test\nanjing\raw_data\sub_1\ses_2\dicom'
#print(len(os.listdir(path1)))
#path2=r'F:\Raw\raw_data\NN_00000001_S002'
#print(len(os.listdir(path2)))
#写一个测试程序
#计算机分发后每人次的序列数量
xulie_list_fen=[]
number_xulie_list=[]
base_path=r'/root/Desktop/FenFa/RAWDATA_fenfa_test/nanjing/raw_data'
data_type='dicom'
dirs=os.listdir(base_path)
dirs.sort(key=lambda x: int(x.split('_')[1]))
for dir in dirs:
    patient_path=base_path+'/'+dir
    #print(patient_path)
    sessions=os.listdir(patient_path)
    sessions.sort(key=lambda x: int(x.split('_')[1]))
    for session in sessions:
        path=patient_path+'/'+session+'/'+'dicom'
        print(path)
        number_xulie=len(os.listdir(path))
        xulie_list_fen.append(number_xulie)
        lists=os.listdir(path)
        for list in lists:
            path_final=path+'/'+list
            number_xulie_files=len(os.listdir(path_final))
            number_xulie_list.append(number_xulie_files)
            #print('number_xulie: '+str(number_xulie)+"; "+'number_xulie_files:'+str(number_xulie_files)+'; ')

#print(number_xulie_list)

#写一个程序计算原始数据中的列表数量
xulie_list_raw=[]
base_path=r'/root/Desktop/FenFa/RAWDATA'
patients0=os.listdir(base_path)
patients0.sort(key=lambda x: str(x.split('_|_s')[0]))
#patients.sort(key=lambda x: str(x.split('_|_s|')[1]))
for patient in patients0:
    path=base_path+'/'+patient
    print(path)
    number_xulie=len(os.listdir(path))
    xulie_list_raw.append(number_xulie)
print(xulie_list_fen)
print(xulie_list_raw)
if xulie_list_fen==xulie_list_raw:
    print("测试完毕")


