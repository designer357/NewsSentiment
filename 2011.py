#-*- coding:utf-8 -*-
__author__ = 'chengmin'
try:
    import psyco
    psyco.full()
except ImportError:
    pass # psyco not installed so continue as usual
import os
import chardet
import time
from zhtools.langconv import *
import Sentiment
import os
from zhtools.langconv import *
import jieba
#import codecs
#import snownlp
import jieba.posseg as pseg
import time
#t1=time.time()
filelist=os.listdir(os.getcwd())
cixing=["/x","/zg","/uj","/ul","/e","/d","/uz","/y"]#词列表为自己定义要过滤掉的词性
#f=codecs.open("Positive", 'r', encoding='utf-8',errors='ignore')
#from multiprocessing import Pool
#from multiprocessing import Process, Queue
def Worker1(eachfolder,sentiment_value,list_name,title_weight,dict_name):
    print("Process ID# %s" % (os.getpid()))
    eachfolder_size=len(os.listdir(os.path.join(os.getcwd(),eachfolder)))

    for eachfile in os.listdir(os.path.join(os.getcwd(),eachfolder)):
        eachfolder_size-=1
        print(str(eachfolder_size)+"left.....................^_^")
        try:
            with open(os.path.join(os.path.join(os.getcwd(),eachfolder),eachfile),"r")as fin2:#unicode step1: rb
                eachlines=fin2.readlines()
                #print(eachlines)
                if len(eachlines)==0:
                    continue
                if 1>0:
                    list_temp = list(map(lambda a:int(a),[v for i,v in dict_name.items()]))
                    #print(list_temp)
                    if max(list_temp)<2:
                        continue
                    else:
                        #print("ada")
                        y_indexes=[i for i,v in enumerate(list_name) if int(dict_name[v])<=max(list_temp) and int(dict_name[v])>=2]
                        for y in y_indexes:
                            sentiment_value[list_name[y]]=sentiment_value[list_name[y]]+float(ComputeSentiment(eachfolder,eachfile))
                else:
                    pass
        except:
            continue
    return sentiment_value
    #print "Parent Process ID# %s" % (os.getppid())
    #print "%s will sleep for %s seconds" % (name, seconds)
#def offer(queue):
    #queue.put("Hello World")


def LoadPositiveDict():
    PositiveDict={}
    with open(os.path.join(os.getcwd(),"Positive.txt"))as f:
        for each in f.readlines():
            if len(each.strip())>1:
                PositiveDict[each.strip()]= 1
    return PositiveDict
def LoadNegativeDict():
    NegativeDict={}
    with open(os.path.join(os.getcwd(),"Negative.txt"))as f:
        for each in f.readlines():
            if len(each.strip())>1:
                NegativeDict[each.strip()]= 1
    return NegativeDict

def ComputeSentiment(filefolder,filename):
    """
    for eachfile in filelist:
        if os.path.isdir(eachfile):
            continue
        if '.py' in eachfile or'.txt' in eachfile:
            continue
        if 'Positive' in eachfile or 'Negative' in eachfile:
            continue
    """

    with open(os.path.join(os.path.join(os.getcwd(),filefolder),filename),"r")as fin:#读取文本
        #valstring=fin.read().decode("utf-8")
        #print(os.path.join(os.getcwd()+'/'+filefolder,filename))
        valstring=fin.read()
        vallist=valstring.split("###")
        #print(vallist)
        if len(vallist) < 2: return 9999
        #vallist2=vallist[1].strip().split('\t',2)
        valstring2=vallist[1].strip()
        #print(valstring2)
        valstringlist=valstring2.strip().split('\t')
            #filter(lambda a:len(a)>1,)
        valstringlist1=list(map(lambda a:a.strip(),valstringlist))
        valstringlist2=list(filter(lambda a:len(a)>1,valstringlist1))

        if len(valstringlist2) == 7:
            valstringlist2.pop(0)
            valstringlist2.pop(0)
            valstringlist2.pop(len(valstringlist2)-1)
            valstringlist2.pop(len(valstringlist2)-1)
            valstringlist2.pop(len(valstringlist2)-1)
            valstringlist2.pop(len(valstringlist2)-1)
        elif len(valstringlist2) == 6:
            valstringlist2.pop(0)
            valstringlist2.pop(0)
            valstringlist2.pop(len(valstringlist2)-1)
            valstringlist2.pop(len(valstringlist2)-1)
            valstringlist2.pop(len(valstringlist2)-1)
        elif len(valstringlist2) == 5:
            valstringlist2.pop(0)
            valstringlist2.pop(0)
            valstringlist2.pop(len(valstringlist2)-1)
            valstringlist2.pop(len(valstringlist2)-1)
        elif len(valstringlist2) == 4:
            valstringlist2.pop(0)
            valstringlist2.pop(0)
            valstringlist2.pop(len(valstringlist2)-1)
        valstring3=''.join(valstringlist2)
        #jieba.enable_parallel()
        words = pseg.cut(valstring3) #进行分词

        NumberofWords=0

        result1=""
        for w in words:
            NumberofWords += 1
            try:
                w.word = Converter('zh-hans').convert(w.word)
            except:
                pass

            # if python 3.x
            #temp = w.word
            #result1 = result1 + '#@' + str(temp)+"/"+str(w.flag) #加词性标注
            # if python 2.x
            temp = unicode(w.word).encode("utf-8")
            result1 = result1 + '#@' + str(temp)+"/"+str(w.flag) #加词性标注


        #print(words)
        #print(NumberofWords)
        resultlist1=result1.split('#@')
        resultlist1=list(filter(lambda a:len(a)>1,resultlist1))

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

        TotalCount=0
        Positive_Value=0
        Negative_Value=0
        PositiveDict=LoadPositiveDict()
        NegativeDict=LoadNegativeDict()
        for each in resultlist1:
            #if 1 > 0:
            try:
                val=each.split('/')
                if val[0].strip() in PositiveDict:
                    Positive_Value=Positive_Value + abs(PositiveDict[val[0].strip()])
                    TotalCount += 1
                    #print("Positive_Value is ......................... "+str(Positive_Value)+" -----"+str(val[0]))
                if val[0].strip() in NegativeDict:
                    Negative_Value=Negative_Value + abs(NegativeDict[val[0].strip()])
                    TotalCount += 1
                    #print("Negative_Value is ......................... "+str(Negative_Value)+" -----"+str(val[0]))

            except:
                continue

        if TotalCount>0:
            #SentimentValue=float(Positive_Value-Negative_Value)#M1.P-N
            SentimentValue=float(Positive_Value-Negative_Value)/TotalCount#M2.P-N/count
            #SentimentValue=float(Positive_Value-Negative_Value)/(Positive_Value+Negative_Value)#M3.P-N/count
            #SentimentValue=float(Positive_Value-Negative_Value)/(Positive_Value+Negative_Value)#M4.P-N/count
        else:
            SentimentValue=0
        #print("Sentiment is ------------------"+str(SentimentValue)+ "----------Total Count is "+str(TotalCount))

        return SentimentValue
#t2=time.time()
#print("分词及词性标注完成，耗时："+str(t2-t1)+"秒。") #反馈结果

def Initlization():
    dict_name={}
    sentiment_value={}
    list_name=[]
    title_weight=float(1.234567891234567)
    with open(os.path.join(os.getcwd(),"InPut_List.txt"),"r")as fin1:
        for eachline1 in fin1:
            #print(eachline1)
            #mytype = (chardet.detect(eachline1))['encoding']
            val1=eachline1.split('%')
            if len(val1) < 2: continue
            item1=val1[0].strip()
            item2=val1[1].strip()
            item=item1+'%'+item2
            #print("----------------------------------------------------------------------"+str(item))
            #Change to Simplfied-Chinese
            #item = Converter('zh-hant').convert(item)
            flag=item in dict_name.keys()
            if flag==True:
                pass
            elif flag==False:
                dict_name[item]='0'
                sentiment_value[item]=0
                list_name.append(item)
        #list_name=list(set(list_name))
    return dict_name,sentiment_value,list_name,title_weight
#Compute how many appearance times for each company in each folder
def Worker2(eachfolder,dict_name,list_name,title_weight):
    eachfolder_size=len(os.listdir(os.path.join(os.getcwd(),eachfolder)))
    for eachfile in os.listdir(os.path.join(os.getcwd(),eachfolder)):
        try:
            eachfolder_size-=1
            print(str(eachfolder_size)+"left...^_^")
            list_temp=[0 for x in range(len(dict_name))]

            with open(os.path.join(os.path.join(os.getcwd(),eachfolder),eachfile),"r")as fin2:#unicode step1: rb
                eachlines=fin2.readlines()
                #eachlines=eachlines.decode("utf-8")

                if len(eachlines)==0:
                    continue
                #---------------
                #if python 2.x
                #mytype=chardet.detect(eachlines[0])["encoding"]#unicode step2:detect type using chardet
                #try:
                    #eachlines=eachlines[0].decode(mytype).encode("utf-8")
                #except:
                    #pass
                #eachlines=eachlines[0].decode(mytype).encode("utf-8").decode("utf-8")#unicode step3:first decode from mytype to unicode/which is str
                #---------------
                #if python 3.x
                eachlines = eachlines[0]
                for x in range(len(dict_name)):#find the company name is shown in content and compute the times
                    try:
                        tempitem1,tempitem2=list_name[x].strip().split('%')

                        if tempitem1==tempitem2:
                            #print(chardet.detect(eachlines)["encoding"])
                            list_temp[x]=list_temp[x]+eachlines.count(tempitem1)
                            list_temp[x]=list_temp[x]+eachfile.count(tempitem1)*title_weight#compute the value that company name shown in title
                        else:
                            list_temp[x]=list_temp[x]+eachlines.count(tempitem1)+eachlines.count(tempitem2)
                            list_temp[x]=list_temp[x]+(eachfile.count(tempitem1)+eachfile.count(tempitem2))*title_weight
                    except:
                        continue
                if max(list_temp)<2:
                    continue
                else:
                    y_indexes=[i for i,v in enumerate(list_temp) if v==max(list_temp)]
                    for y in y_indexes:
                        #if list_name[y]=="萬科":
                            #hh.append(eachfile)
                        dict_name[list_name[y]]=str(int(dict_name[list_name[y]])+1)

                        #sentiment_value[list_name[y]]=sentiment_value[list_name[y]]+ComputeSentiment(eachfolder,eachfile)
                    #temp_i=y_indexes[0]
                    #dict_name[list_name[temp_i]]=str(int(dict_name[list_name[temp_i]])+1)
                    #sentiment_value[list_name[temp_i]]=sentiment_value[list_name[temp_i]]+Sentiment.ComputeSentiment(eachfolder,eachfile)
                    #print(eachfile+"---"+list_name[temp_i]+str(max(list_temp)))
                    #print(y_indexes)
        except:
            continue
    #print(dict_name)
    return dict_name
def Worker3(eachfolder):
    dict_name,sentiment_value,list_name,title_weight=Initlization()
    #child_proc1 = Process(target=Worker1, args=(eachfolder,sentiment_value,list_name,title_weight))
    #child_proc2 = Process(target=Worker2, args=(eachfolder,dict_name,list_name,title_weight))
    #child_proc1.start()
    #child_proc2.start()



    dict_name=Worker2(eachfolder,dict_name,list_name,title_weight)

    sentiment_value=Worker1(eachfolder,sentiment_value,list_name,title_weight,dict_name)

    #sentiment_value=Worker1(eachfolder)
    #child_proc2.join(10000)
    #time.sleep(100000000)
    #print(dict_name)
    #print(sentiment_value)
    return dict_name,sentiment_value






#os.chdir("/home/cityu/wisenewscode")

start=time.clock()
folders=[x for x in os.listdir(os.getcwd()) if os.path.isdir(x)==True and '2011~~2012' in x]

for eachfolder in folders:
    print(eachfolder+" is processing")
    dict_name,sentiment_value=Worker3(eachfolder)
    print("------------------------------------------------------------------>>>")
    with open(os.path.join(os.getcwd(),eachfolder+"_M2.txt"),'w')as fout2:
        for (k,v) in dict_name.items():
            try:
                fout2.write(k+'\t\t'+v+'\t\t'+str(sentiment_value[k])+'\n')
            except:
                continue

end=time.clock()
print("The total time is "+str(end-start)+" secs...")

