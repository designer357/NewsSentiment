#-*- coding:utf-8 -*-
__author__ = 'chengmin'
import os
from zhtools.langconv import *
import jieba
#import codecs
#import snownlp
import jieba.posseg as pseg
#import time
#t1=time.time()
filelist=os.listdir(os.getcwd())
cixing=["/x","/zg","/uj","/ul","/e","/d","/uz","/y"]#词列表为自己定义要过滤掉的词性
#f=codecs.open("Positive", 'r', encoding='utf-8',errors='ignore')
def LoadPositiveDict():
    PositiveDict={}
    f1=open("Positive.txt","r")
    for each in f1.readlines():
        if len(each.strip())>1:
            PositiveDict[each.strip()]= 1
    return PositiveDict
def LoadNegativeDict():
    NegativeDict={}
    f2=open("Negative.txt","r")
    for each in f2.readlines():
        if len(each.strip())>1:
            NegativeDict[each.strip()]= -1
    return NegativeDict

def ComputeSentiment(filename):
    """
    for eachfile in filelist:
        if os.path.isdir(eachfile):
            continue
        if '.py' in eachfile or'.txt' in eachfile:
            continue
        if 'Positive' in eachfile or 'Negative' in eachfile:
            continue
    """
    with open(filename)as fin:#读取文本
        #valstring=fin.read().decode("utf-8")
        valstring=fin.read()
        #print(valstring)
        valstring=valstring.decode("utf-8")
        vallist=valstring.split("###")
        vallist2=vallist[1].split('|')
        valstring2=vallist2[0]
        valstringlist=valstring2.strip().split('\t')
            #filter(lambda a:len(a)>1,)
        valstringlist=list(map(lambda a:a.strip(),valstringlist))
        valstringlist=list(filter(lambda a:len(a)>1,valstringlist))
        if len(valstringlist)>=5:
            valstringlist.pop(0)
            valstringlist.pop(0)
            valstringlist.pop(len(valstringlist)-1)
            valstringlist.pop(len(valstringlist)-1)
            valstringlist.pop(len(valstringlist)-1)
        valstring3=''.join(valstringlist)
        jieba.enable_parallel()
        words = pseg.cut(valstring3) #进行分词
        result1=""
        for w in words:
            w.word = Converter('zh-hans').convert(w.word)
            temp_word = (w.word).encode("utf-8")
            temp_flag = (w.flag).encode("utf-8")
            result1 = result1 + '#@' + str(temp_word)+"/"+str(temp_flag) #加词性标注
        resultlist1=result1.split('#@')
        resultlist1=list(filter(lambda a:len(a)>1,resultlist1))


        #print(resultlist1)
        templist=resultlist1[:]
        for segs in templist:
            for K in cixing:
                if K in segs:
                    resultlist1.remove(segs)
                    break
                else:
                    pass
        #print(resultlist1)#记录最终结果的变量
        #txtlist.extend(line_list)
        #with open("t_with_POS_tag.txt","w") as fout: #将结果保存到另一个文档中
            #fout.writelines(resultlist1)

        SentimentValue=0
        TotalCount=0
        PositiveDict=LoadPositiveDict()
        NegativeDict=LoadNegativeDict()
        for each in resultlist1:
            val=each.split('/')
            if val[0].strip() in PositiveDict:
                SentimentValue=SentimentValue + int(PositiveDict[val[0].strip()])
                TotalCount += 1
            if val[0].strip() in NegativeDict:
                SentimentValue=SentimentValue + int(NegativeDict[val[0].strip()])
                TotalCount += 1

        if TotalCount>0:
            NormalizedSentimentValue=float(SentimentValue)/TotalCount
        else:
            NormalizedSentimentValue=0
        return NormalizedSentimentValue


#import cProfile
#import pstats
#cProfile.run("ComputeSentiment(\"2010~2011\",\"萬科三季報：手握現金315億\")","result")
#p=pstats.Stats("result")
#cProfile.run("ComputeSentiment(\"2010~2011\",\"萬科三季報：手握現金315億\")")
#p.sort_stats('time', 'cum').print_stats(.5, "ComputeSentiment(\"2010~2011\",\"萬科三季報：手握現金315億\")")

#t2=time.time()
#print("分词及词性标注完成，耗时："+str(t2-t1)+"秒。") #反馈结果

