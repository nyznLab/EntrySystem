from Utils import getMetaDataFromJSON,writeMetaDataToJSON,getIdAndSession,packingIdAndSession,\
    getIdNameFromString,getTrueSixthPath,createPath,updateMetaDataDict,get_rawdata_subpath
import fconfig as conf
import os    #处理文件和目录的模块：对目录或文件的新建，删除，查看文件属性，对文件以及目录的路径操作。
import shutil    #对os模块的补充，对文件进行移动、复制、打包、压缩、解压。
import re
from exception import BussinessException,handle_exception
import configclass


def updateMetaData(id,session,basePath): #元文件指Json文件。
    """
    更新metaData信息
    :param id:
    :param session:
    :param basePath: raw_data intermediate or preprocess 的路径
    :return:
    """
    """
    1.metaData文件是否存在，否则创建
    2.根据id读取元文件配置项，不存在直接创建相应的id，session信息
    3.存在的更新相应的id的list
    """
    createPath(basePath)
    metaDataFileName = basePath+'/'+'metaData.json'
    dataDict = {}
    if(os.path.exists(metaDataFileName)):
        dataDict = getMetaDataFromJSON(metaDataFileName)
    if(id in dataDict.keys()):
        if(session not in dataDict[id]):
            dataDict[id].append(session)
    else:
        dataDict[id] = [session]
    writeMetaDataToJSON(dataDict,metaDataFileName)

# 对病人列表编号进行格式校验
def check_patient_list(patient_list):
    aft_patient_list = []
    for ele in patient_list:
        standard_id = getIdNameFromString(ele)
        if standard_id==None:
            handle_exception(BussinessException(f'病人编号:{ele} 不符合规范'))
        else:
            aft_patient_list.append(standard_id)
    return aft_patient_list


# deprecated
def generateAllFile(baseType,id,session,basePath):
    fifthTypes = conf.fifthDirectory[baseType]
    for fifthType in fifthTypes:
        if fifthType in conf.sixDirectory.keys():
            sixTypes = conf.sixDirectory[fifthType]
            for sixType in sixTypes:
                dir = '{}/{}/{}/{}/{}'.format(basePath, str(id), str(session),fifthType,sixType)
                createPath(dir)
        else:
            dir = '{}/{}/{}/{}'.format(basePath, str(id), str(session), fifthType)
            createPath(dir)


def copyToFileSystemIntermediate(sourcePath,cityPath,fifthPathType):
    """
    :param cityPath:
    :param sourcePath:
    :param fifthPathType:包括func anat dwi三种
    :return:
    """
    baseType = 'intermediate_data'
    basePath = cityPath + '/' + baseType
    createPath(basePath)
    metaDataFileName = basePath + '/' + 'metaData.json'
    dataDict = {}
    if (os.path.exists(metaDataFileName)):
        dataDict = getMetaDataFromJSON(metaDataFileName)
    """
    1.intermeidate目录下的文件结构目录实际上是有多种的，包括id session信息存储在文件夹里面，或者是存储在文件里面；
    还包括某些文件夹或者某些文件是所有的病人所共有的（Masks，RealignParameter），需要分类进行处理
    2.共有文件夹的处理，存储下共有文件夹或者是文件的名字，存储下所有idName的信息，然后再去进行分发
    3.id session相关信息的存储，遍历imgType下的文件，假如他是一个file并且正则表达式符合NN_000000XXX_S00X，可以获取信息
    4.假如imgType==Results，那么直接调用preprocess的处理函数,假如imgType==FunImg,单独处理
    """
    # 共享文件夹或者是文件
    allPatientsShareFilesDict = {}
    # 所有的patient id session信息
    idNames = []
    firstPaths = os.listdir(sourcePath)   #返回sourcepath指定的文件夹包含的文件或文件夹的名字的列表。
    for firstPath in firstPaths:
        firstPathName = sourcePath+'/'+firstPath
        if(firstPath=='Results'):
            copyToFileSystemPreprocess(cityPath,firstPathName)
        #     需要转换成bids结构的文件目录
        elif(firstPath==conf.BIDSDict[fifthPathType]):
            # todo
            pass
        else:
            secondPaths = os.listdir(firstPathName)
            for secondPath in secondPaths:
                secondPathName = firstPathName+'/'+secondPath
                # 假如是文件，说明可能是共享文件或者是id信息存储在文件里面的情况
                if(os.path.isfile(secondPathName)):
                    # 不符合正则表达式，说明是所有病人共享文件
                    if(getIdNameFromString(secondPath)==None):
                        if (firstPath in allPatientsShareFilesDict.keys()):
                            allPatientsShareFilesDict[firstPath].append(secondPathName)
                        else:
                            allPatientsShareFilesDict[firstPath] = [secondPathName]
                    # 符合正则表达式，说明可以获取到id session信息
                    else:
                        idName = getIdNameFromString(secondPath)
                        idNames.append(idName)
                        id,session = getIdAndSession(getIdNameFromString(idName))
                        updateMetaDataDict(id, session, dataDict)
                        id,session = packingIdAndSession(id,session)
                        # generateAllFile(baseType, id, session, cityPath + '/' + baseType)
                        destPath = '{}/{}/{}/{}/{}/{}'.format(cityPath, baseType, str(id), str(session), fifthPathType+'_others',firstPath)
                        createPath(destPath)
                        shutil.copy(secondPathName, destPath)
                # 是目录,那么secondPath就是idName
                else:
                    idNames.append(secondPath)
                    id,session = getIdAndSession(getIdNameFromString(secondPath))
                    updateMetaDataDict(id, session, dataDict)
                    id,session = packingIdAndSession(id,session)
                    # generateAllFile(baseType, id, session, cityPath + '/' + baseType)
                    thirdPaths = os.listdir(secondPathName)
                    for ele in thirdPaths:
                        destPath = '{}/{}/{}/{}/{}/{}'.format(cityPath, baseType, str(id), str(session),
                                                           fifthPathType + '_others',firstPath)
                        createPath(destPath)
                        shutil.copy(secondPathName+'/'+ele, destPath)

    # 进行共享文件的处理
    for idName in idNames:
        id,session = getIdAndSession(getIdNameFromString(idName))
        id,session = packingIdAndSession(id,session)

        for k,v in allPatientsShareFilesDict.items():
            for ele in v:
                destPath = '{}/{}/{}/{}/{}/{}'.format(cityPath, baseType, str(id), str(session),
                                                      fifthPathType + '_others', k)
                createPath(destPath)
                shutil.copy(ele, destPath)
    writeMetaDataToJSON(dataDict,metaDataFileName)

def copyToFileSystemPreprocess(sourcePath,cityPath,patientList=None):
    '''
    进行预处理之后的文件分发，包括alff，reho，fc等,
    支持通过patient_list传递病人编号将文件夹中指定的病人数据拷贝过去
    :param cityPath: 拷贝到的文件目录下，沈阳还是南京的目录
    :param sourcePath: 源文件目录，需要包含两级目录,格式需满足，一级目录下均是文件夹，不包含具体文件
    :return:

    1.创建基础文件目录
    2.进行数据分发
        读取第一级目录，获取所有数据类型（alff，reho，fc等）
        读取第二级别目录，进行文件拷贝以及目标文件目录的创建
    3.支持根据病人列表进行目录拷贝
    '''
    # 进行patient_list的数据校验
    if patientList:
        patientList = check_patient_list(patientList)#返回的是一个标准的经过校验判断的病人编号。

    # 创建基础目录
    baseType = 'preprocess'
    basePath = f'{cityPath}/{baseType}'
    createPath(basePath)

    # 元文件的建立
    metaDataFileName = f'{basePath}/metaData.json'
    dataDict = {}
    if (os.path.exists(metaDataFileName)):
        dataDict = getMetaDataFromJSON(metaDataFileName)

    # 数据分发
    firstPaths = os.listdir(sourcePath)
    #获取除FC_FunImgARWSDCF之外的文件夹名；
    #遍历一级目录，preprocess有那些type类型,例如reho，alff等等
    for firstPath in firstPaths:
        if(firstPath==configclass.preprocessDict.FC):
            continue
        firstPathName = f'{sourcePath}/{firstPath}'
        try:
            files = os.listdir(firstPathName)
        except:
            handle_exception(BussinessException(f'===目录：{firstPathName}，需要为文件夹，请进行校验==='))
            continue
        # 进行文件拷贝
        if patientList is None:
            for file in files:
                try:
                    id, session, data_dict = get_id_session_by_filename(file,dataDict)
                    destPath = f'{basePath}/{id}/{session}/{firstPath}'
                    createPath(destPath)
                    shutil.copy(firstPathName + '/' + file, destPath)
                except BussinessException as e:
                    handle_exception(e)
        else:
            for file in files:
                if getIdNameFromString(file) in patientList:
                    id, session, dataDict = get_id_session_by_filename(file, dataDict)
                    destPath = f'{basePath}/{id}/{session}/{firstPath}'
                    createPath(destPath)
                    shutil.copy(firstPathName + '/' + file, destPath)
    writeMetaDataToJSON(dataDict,metaDataFileName)

def copyToFileSystemRawData(sourcePath,cityPath,data_type,patientList = None):
    """
    分发匿名化之后的数据，即各种dicom文件
    :param sourcePath: 拷贝过来的原路径
    :param cityPath: 文件系统目录的city路径，就是根路径basePath+'shenyang' or basePath+'nanjing'
    :param data_type: 第五级目录(dicom，snp，audio ，video四种情况)
    :return:
    """
    """
    1.遍历根目录，获取到关于id，session信息
    2.更新metaData文件信息，进行数据校验
    3.目录生成
    4.进入到六级目录下进行数据拷贝
    """
    if patientList:
        patientList = check_patient_list(patientList)
    # 生成目录
    baseType = 'raw_data'
    basePath = f'{cityPath}/{baseType}'
    createPath(basePath)
    # 元文件
    metaDataFileName = f'{basePath}/metaData.json'
    dataDict = {}
    if (os.path.exists(metaDataFileName)):
        dataDict = getMetaDataFromJSON(metaDataFileName)

    # 遍历获取所有病人编号信息
    try:
        patientsIds = os.listdir(sourcePath)    #参数为需要列出的目录路径,返回指定路径下的文件和文件夹列表
    except:
        raise BussinessException(f'===目录：{sourcePath}，需要为文件夹，请进行校验===')

    #判断patient_list中的病人文件存不存在
    #pass

    # 遍历所有病人
    for patientId in patientsIds:
        # 有list列表，而且ptientid不list列表中，那么直接跳过不执行
        if patientList and getIdNameFromString(patientId) not in patientList:
            continue
        # 正常进行病人文件拷贝
        standard_id = getIdNameFromString(patientId) #函数判断病人的编号是否合法
        if standard_id is None:
            handle_exception(BussinessException(f'===病人id：{patientId}不合法，请确认修改后重新执行==='))
        else:
            try:
                id,session,dataDict = get_id_session_by_filename(patientId,dataDict)
            except BussinessException as e:
                handle_exception(e)
                continue
            patientdir = sourcePath + '/' + patientId
            patientdirs = os.listdir(patientdir)
            patientdirs.sort(key=lambda x: int(x.split(' ')[0]))
            subraw_data_path_list = []
            path_list=[]
            for dir in patientdirs:
                subraw_data_path = patientdir + '/' + dir

                subraw_data_path_list.append(subraw_data_path)
            #print(subraw_data_path_list)
            for i in range(len(subraw_data_path_list) - 1, -1, -1):
                if (subraw_data_path_list[i].split(' ')[1] == 'gre_field_mapping_rest64'):
                    continue
                elif (subraw_data_path_list[i - 1].split(' ')[1:] == subraw_data_path_list[i].split(' ')[1:] ) :
                    del subraw_data_path_list[i - 1]
                # else:
                #     continue
            for subraw_data_path in subraw_data_path_list:

                if (os.path.isfile(subraw_data_path)):
                    destPath = '{}/{}/{}/{}/{}'.format(cityPath, baseType, str(id), str(session), data_type)
                    createPath(destPath)
                    shutil.copy(subraw_data_path, destPath)
                else:
                    # 获取真正的文件系统的六级路径名
                    subraw_data_path_aft = get_rawdata_subpath(subraw_data_path)

                    for i in range(len(path_list)):
                        if (subraw_data_path_aft== path_list[i]):
                            subraw_data_path_aft = subraw_data_path_aft + '_2'
                    path_list.append(subraw_data_path_aft)

                    destPath = f'{cityPath}/{baseType}/{id}/{session}/{data_type}/{subraw_data_path_aft}'
                    files = os.listdir(subraw_data_path)
                    for file in files:
                        createPath(destPath)
                        shutil.copy(subraw_data_path + '/' + file, destPath)
    writeMetaDataToJSON(dataDict, metaDataFileName)

# 根据文件名获取封装的id，session
def get_id_session_by_filename(filename,data_dict):
    standard_id = getIdNameFromString(filename)
    # 进行异常处理，病人编号命名错误的情况
    if standard_id is None:
        raise BussinessException(f'===病人id：{filename}不合法，请确认修改后重新执行==')
    # 无异常正常执行
    id, session = getIdAndSession(standard_id)
    updateMetaDataDict(id, session, data_dict)
    id, session = packingIdAndSession(id, session)
    return  id,session,data_dict

# todo，文件删除问题
def deleteFromFileSystem(basePath,id,session,dataType):
    pass


# copyToFileSystemPreprocess(conf.nanjingPath, '/home/zxz/wdh/test_data',['NN_00000006_S001','NN_00000013_S001','NN_00000015_S005'])
#copyToFileSystemPreprocess(conf.nanjingPath, r'F:\propress')
# copyToFileSystemRawData(conf.nanjingPath, '/home/zxz/wdh/test_data/raw', 'dicom',patient_list=['NN_00000001_S001','NN_00000001_S004'])


