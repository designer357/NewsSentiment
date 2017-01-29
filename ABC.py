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
def All_Jidu():
    all_jidu_list_dict_1 = {'2011-1': ['2011-01', '2011-02', '2011-03'],
                          '2011-2': ['2011-04', '2011-05', '2011-06'],
                          '2011-3': ['2011-07', '2011-08',' 2011-09'],
                          '2011-4': ['2011-10', '2011-11', '2011-12'],
                          '2012-1': ['2012-01', '2012-02', '2012-03'],
                          '2012-2': ['2012-04', '2012-05', '2012-06'],
                          '2012-3': ['2012-07', '2012-08', '2012-09'],
                          '2012-4': ['2012-10', '2012-11', '2012-12'],
                          '2013-1': ['2013-01', '2013-02', '2013-03'],
                          '2013-2': ['2013-04', '2013-05', '2013-06'],
                          '2013-3': ['2013-07', '2013-08', '2013-09'],
                          '2013-4': ['2013-10', '2013-11', '2013-12'],
                          '2014-1': ['2014-01', '2014-02', '2014-03'],
                          '2014-2': ['2014-04', '2014-05', '2014-06'],
                          '2014-3': ['2014-07', '2014-08', '2014-09'],
                          '2014-4': ['2014-10', '2014-11', '2014-12'],
                          '2015-1': ['2015-01', '2015-02', '2015-03'],
                          '2015-2': ['2015-04', '2015-05', '2015-06'],
                          '2015-3': ['2015-07', '2015-08', '2015-09'],
                          '2015-4': ['2015-10', '2015-11', '2015-12'],

    }
    #list_temp = [0 for x in range(len(dict_name))]
    all_jidu_list_dict_2 = {}
    for k,v in all_jidu_list_dict_1.items():
        all_jidu_list_dict_2[k] = 0
    return all_jidu_list_dict_1,all_jidu_list_dict_2
def Worker1(eachfolder,sentiment_value,list_name,title_weight,dict_name):
    print("Process ID# %s" % (os.getpid()))
    eachfolder_size=len(os.listdir(os.path.join(os.getcwd(),eachfolder)))

    for eachfile in os.listdir(os.path.join(os.getcwd(),eachfolder)):
        eachfolder_size-=1
        print(str(eachfolder_size)+"left.....................^_^")
        if 1>0:
            with open(os.path.join(os.path.join(os.getcwd(),eachfolder),eachfile),"rb")as fin2:#unicode step1: rb
                eachlines=fin2.readlines()
                if len(eachlines)==0:
                    continue
                if 1>0:
                    list_temp = map(lambda a:int(a),[v for i,v in dict_name.items()])
                    if max(list_temp)<1:
                        continue
                    else:

                        y_indexes=[i for i,v in enumerate(list_name) if int(dict_name[v])<=max(list_temp) and int(dict_name[v])>=1]
                        for y in y_indexes:
                            sentiment_value[list_name[y]]=sentiment_value[list_name[y]]+float(ComputeSentiment(eachfolder,eachfile))
                else:
                    pass
        else:
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
        #words2 = jieba.cut(valstring3,cut_all=False)
        NumberofWords=0

        result1=""
        for w in words:
            NumberofWords += 1
            try:
                w.word = Converter('zh-hans').convert(w.word)
            except:
                pass
            temp = unicode(w.word).encode("utf-8")
            result1 = result1 + '#@' + str(temp)+"/"+str(w.flag) #加词性标注

        #print(words)
        #print(NumberofWords)
        resultlist1=result1.split('#@')
        resultlist1=list(filter(lambda a:len(a)>1,resultlist1))
        #print("----------------------------")
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

        TotalCount=0
        Positive_Value=0
        Negative_Value=0
        PositiveDict=LoadPositiveDict()
        NegativeDict=LoadNegativeDict()
        for each in resultlist1:
            if 1>0:
                val=each.split('/')
                if val[0].strip() in PositiveDict:
                    Positive_Value=Positive_Value + abs(PositiveDict[val[0].strip()])
                    TotalCount += 1
                    #print("Positive_Value is ......................... "+str(Positive_Value)+" -----"+str(val[0]))
                if val[0].strip() in NegativeDict:
                    Negative_Value=Negative_Value + abs(NegativeDict[val[0].strip()])
                    TotalCount += 1
                    #print("Negative_Value is ......................... "+str(Negative_Value)+" -----"+str(val[0]))

            else:
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
    jieba.load_userdict(os.path.join(os.getcwd(),"InPut_List.txt"))
    dict_name={}
    sentiment_value={}
    list_name=[]
    title_weight=float(1.234567891234567)
    with open(os.path.join(os.getcwd(),"InPut_List.txt"),"rb")as fin1:
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
    all_jidu_list_dict_1,all_jidu_list_dict_2 = All_Jidu()
    dict_name222 = {}
    for k,v in dict_name.items():
        dict_name222[k] = all_jidu_list_dict_2.copy()
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
                mytype=chardet.detect(eachlines[0])["encoding"]#unicode step2:detect type using chardet
                try:
                    eachlines=eachlines[0].decode(mytype).encode("utf-8")
                except:
                    pass
                #eachlines=eachlines[0].decode(mytype).encode("utf-8").decode("utf-8")#unicode step3:first decode from mytype to unicode/which is str
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
                if max(list_temp)<1:
                    continue
                else:
                    y_indexes=[i for i,v in enumerate(list_temp) if v==max(list_temp)]
                    for y in y_indexes:
                        #if list_name[y]=="萬科":
                            #hh.append(eachfile)
                        dict_name[list_name[y]]=str(int(dict_name[list_name[y]])+1)
                    for eachk2,eachv2 in all_jidu_list_dict_1.items():
                        for eachvv2 in eachv2:
                            if eachvv2 in eachlines:
                                dict_name222[list_name[y]][eachk2] = str(int(dict_name222[list_name[y]][eachk2])+1)
                        #sentiment_value[list_name[y]]=sentiment_value[list_name[y]]+ComputeSentiment(eachfolder,eachfile)
                    #temp_i=y_indexes[0]
                    #dict_name[list_name[temp_i]]=str(int(dict_name[list_name[temp_i]])+1)
                    #sentiment_value[list_name[temp_i]]=sentiment_value[list_name[temp_i]]+Sentiment.ComputeSentiment(eachfolder,eachfile)
                    #print(eachfile+"---"+list_name[temp_i]+str(max(list_temp)))
                    #print(y_indexes)
        except:
            continue
    print(dict_name222)
    return dict_name,dict_name222
def Worker3(eachfolder):
    dict_name,sentiment_value,list_name,title_weight=Initlization()
    #child_proc1 = Process(target=Worker1, args=(eachfolder,sentiment_value,list_name,title_weight))
    #child_proc2 = Process(target=Worker2, args=(eachfolder,dict_name,list_name,title_weight))
    #child_proc1.start()
    #child_proc2.start()



    dict_name,dict_name222=Worker2(eachfolder,dict_name,list_name,title_weight)

    #sentiment_value=Worker1(eachfolder,sentiment_value,list_name,title_weight,dict_name)

    #sentiment_value=Worker1(eachfolder)
    #child_proc2.join(10000)
    #time.sleep(100000000)
    #print(dict_name)
    #print(sentiment_value)
    return dict_name,dict_name222


#os.chdir("/home/cityu/wisenewscode")

start=time.clock()
folders=[x for x in os.listdir(os.getcwd()) if os.path.isdir(x)==True and '2011~~2012' in x]
list1 = ['2011-1','2011-2','2011-3','2011-4','2012-1','2012-2','2012-3','2012-4',\
         '2013-1','2013-2','2013-3','2013-4','2014-1','2014-2','2014-3','2014-4',
         '2015-1','2015-2','2015-3','2015-4']
for eachfolder in folders:
    print(eachfolder+" is processing")
    dict_name,dict_name222=Worker3(eachfolder)

    print("------------------------------------------------------------------>>>")
    with open(os.path.join(os.getcwd(),eachfolder+"_STATISTICS.txt"),'w')as fout2:
        for (k,v) in dict_name222.items():
            temp = k+':'
            for each in list1:
                temp = temp + str(dict_name222[k][each])+','
            temp = temp + ''+ str(dict_name[k]) + '\N'
            #temp = temp + ','+ str(sentiment_value[k]) + '\n'
            fout2.write(temp)

end=time.clock()
print("The total time is "+str(end-start)+" secs...")

