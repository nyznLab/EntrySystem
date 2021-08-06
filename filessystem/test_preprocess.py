import os
base_path=r'E:\test\nanjing\preprocess'
base_lists=os.listdir(base_path)
flag=False
for base_list in base_lists:
    flag = False
    patient_path=base_path+'\\'+base_list
    sessions=os.listdir(patient_path)
    for session in sessions:
        prepro_list_path=patient_path+'\\'+session
        prepro_lists=os.listdir(prepro_list_path)
        print(prepro_lists)
        # for prepro_list in prepro_lists:
        #     path=prepro_list_path+'\\'+prepro_list
        list_number=[3,3,6,7]
        count=0
        for i in range(len(prepro_lists)):
            path = prepro_list_path + '\\' + prepro_lists[i]
            if len(os.listdir(path))!=list_number[i]:
                print(prepro_lists[i]+'序列数量异常')
            else:
                count+=1
        if(count==4):
            flag=True
    print(flag)
print(flag)