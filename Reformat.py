#-*- coding: utf-8 -*-
__author__ = 'chengmin'
import sys
import os
import shutil
reload(sys)
sys.setdefaultencoding("utf-8")
import chardet
filefolder="newsentiment"
newpath=os.path.join(os.getcwd(),filefolder)
if not os.path.isdir(newpath):
    os.makedirs(newpath)

else:
    shutil.rmtree(newpath)
    os.makedirs(newpath)
filelist=os.listdir(os.getcwd())
for eachfile in filelist:
    if not "中文" in eachfile:
        continue
    A=[]
    with open(eachfile,"r")as fin:
        eachlines=fin.readlines()
        for each in eachlines:
            mytype=chardet.detect(each)["encoding"]
            print(mytype)
            a=each.decode(mytype).encode("utf-8").decode("utf-8")
            #mytype1=chardet.detect(a)["encoding"]
            #print(mytype1)
            print(a)
            A.append(a)
            #except:
                #pass
    #with open(os.path.join(newpath,eachfile),"w")as fout:
        #fout.writelines(A)



