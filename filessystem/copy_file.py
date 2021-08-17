import os
from shutil import copy

from filessystem.Utils import createPath
from filessystem.exception import BussinessException


def copyFile(sourcePath, destinationPath):
    for standard_id,sourcePath_list in sourcePath.items():
        if os.path.isdir(sourcePath_list):
            dir=sourcePath_list.split('/')[-1]
            print(dir)
            destPath=destinationPath+'/'+standard_id+'_'+dir
            createPath(destPath)
            for list in os.listdir(sourcePath_list):
                print(list)
                copy(sourcePath_list+'/'+list, destPath)
        elif os.path.isfile(sourcePath_list):
            copy(sourcePath_list, destinationPath)
        else:
            raise BussinessException(f'===目录：{sourcePath_list}不存在===')

