# 一级目录
basePath = r'/root/dataset/'
shenyangPath = basePath+'shenyang'
nanjingPath = basePath+'nanjing'

# 二级目录
secondDirectory = ['raw_data','intermediate','preprocess']

# 五级目录
fifthDirectory = {'raw_data':['snp','audio','video','dicom'],
                   'intermediate':['T1/3D','DTI','resting'],
                   'preprocess':['reho','alff','fc','falff','vbm','gca','fa','ft','cth']}

# 六级目录
sixDirectory = {'dicom':['T1/3D','DTI','resting'],
                 'resting':['FunImgARWDFC','FunImgARWDFCovs','FunImgARWS','FunImgARWSD','FunImgARWSDFC',
                           'FunImgARWDFCovs','FunImgARWDF','FunImg','Masks','FunImgA','FunImgAR',
                           'FunImgARW','RealignParameter','PicturesForChkNormalization','FunImgARWSDF','FunImgARWD']}

# 需要转成BIDS文件结构的目录
BIDSDict = {'func':'FunImg'}

# 浙江数据config
DTI = 'AxDTI'
three_D = 'Sag3DMPRAGE'
T_one = ''
