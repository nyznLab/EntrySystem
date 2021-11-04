import json  #Python里的json模块主要用于“Python数据与JSON格式的数据间相互转换”。JSON是一种独立于语言的文本格式，用于数据交换，可以在不同语言间交换数据。
import re  #正则表达式
import os  #用来判断文件或文件夹是否存在
def getMetaDataFromJSON(path):#从描述文件中获取元数据。
    """
    读取CSV数据，返回一个dict
    :param path:
    :return:
    """
    with open(path, 'r') as f:
        dict = json.load(f) #读取json文件，并且把json文件中的字符串格式转化为字典。
        return dict

def writeMetaDataToJSON(dataDict,path):#写列表文件的描述信息到描述文件中。
    """
    写入csv数据
    :param dataDict:
    :param path:
    :return:
    """
    with open(path, "w", encoding='utf-8') as f:
        json.dump(dataDict, f) #将python中的字典格式转化为json中的字符串格式。

def getIdAndSession(name): #从文件名中获取病人的编号id和复扫信息session
    """
    获取id，session信息
    :param name: 文件名NN_00000001_S001
    :return: id和session信息,返回sub_1 ses_1
    """
    try:
        eles = name.split('_')
        id = int(eles[1])
        session = int(eles[2][1:])
        return str(id),str(session)
    except Exception:
        print(f'==病人id:{name} ,格式错误==')

def packingIdAndSession(id,session): #根据编号和复扫号建立文件夹。
    return 'sub_'+str(id),'ses_'+str(session)

# 获取 standard id
def getIdNameFromString(name):
    """
    判断name是否符合NN_\d+_S\d\d\d
    :param name:
    :return:
    """
    pattern = re.compile(r"NN_\d+_S\d\d\d") #将一个字符串编译为字节代码。re指正则表达式模块
    res = pattern.findall(name) #正则表达式，匹配字符串。返回name中所有与pattern相匹配的全部字串,返回形式为数组
    return None if(len(res)==0) else res[0]
    #符合规范的话应该是返回一个正确的文件名，如：NN_00000001_S001

def getTrueSixthPath(dir_):
    if dir_.find('sms5_bold_500ms_rest64') != -1 and dir_[-len('sms5_bold_500ms_rest64'):] == 'sms5_bold_500ms_rest64':
        #find（）方法检查字符串中是否含有子字符串，如果指定 beg（开始） 和 end（结束） 范围，则检查是否包含在指定范围内，如果包含子字符串返回开始的索引值，否则返回-1。
        return 'bold'
    elif dir_.find('t1_mprage_sag_iso_mww64CH') != -1 and dir_[-len('t1_mprage_sag_iso_mww64CH'):] == 't1_mprage_sag_iso_mww64CH':
        return 't1'
    elif dir_.find('sms4_diff_2mm_PA_HARDI64') != -1 and dir_[-len('sms4_diff_2mm_PA_HARDI64'):] == 'sms4_diff_2mm_PA_HARDI64':
        return 'dti'
    else:
        return dir_

def get_rawdata_subpath(path):
    number = ' '
    return path[path.index(number)+1:] #先用split(' ')方法将字符串以" "开割形成一个字符串数组，然后再通过索引[1]取出所得数组中的第二个元素的值。

def createPath(path):
    """
    创建文件夹
    :param createpath:
    :return:
    """
    if(not os.path.exists(path)):
        os.makedirs(path)  # makedirs()用于递归创建路径。

def updateMetaDataDict(id,session,dataDict):   #更新描述文件中的信息，编号，复扫数
    '''
    更新dict
    :param id:
    :param session:
    :param dataDict:
    :return:
    '''
    if (id in dataDict.keys()):
        if (session not in dataDict[id]):
            dataDict[id].append(session)
    else:
        dataDict[id] = [session]
