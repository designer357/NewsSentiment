# #-*- encoding: Big5-HKSCS -*-
import requests
from bs4 import BeautifulSoup
import os
import re
import shutil
#import sys
##type = sys.getdefaultencoding()
##reload(sys)
##sys.setdefaultencoding('gbk')



#global base,Start, Interval, articleisinUrlList, Page, path, newfilepath,PageErrorList,TitleErrorList,IndexErrorList

#def Run(url_block1):
def Init(thecookie):
    global articleisinUrlList,mycookie,base,Start, Interval, Page, path, newfilepath,PageErrorList,TitleErrorList,IndexErrorList

    para=[]
    articleisinUrlList=False
    base = "http://libwisenews.wisers.net"
    Start = -50
    Interval = 50
    articleisinUrlList = False
    Page = 0
    path = os.getcwd()

    #mycookie = "__p_scid_CITYULIB_ipaccess=\"CITYULIB@ipaccess|84502399|0|t1ms1|014c46fd1d6f\"; cMACHINECOOKIE=14c27a62e00; JSESSIONID=A17D0828B09A4238F94586DBA3AC07B9.wise19; gallery-simplegallery1=1; __reLoginUrl=\"\"; __lsid=^t1ms1.wisers.com^84502399; cUSERNAME=\"CITYULIB@ipaccess\"; __lst_libwisenews.wisers.net=1427110827442"
    mycookie=thecookie
    #PageErrorList = []
    TitleErrorList = []
    IndexErrorList = []

    #if not os.path.isdir(newfilepath):
        #os.makedirs(newfilepath)
    #else:
        #shutil.rmtree(newfilepath)
        #os.makedirs(newfilepath)
    #with open(path + "/PageList", "w")as f1:
        #f1.write("PageList\n")
    #with open(path + "/ArticleList", "w")as f1:
        #f1.write("ArticleList\n")

    url_block1 = "TRACK-01605"
    para.append(url_block1)
    para.append(Page)
    para.append(Start)
    return para

def GeneratePageListUrl(url_block1,Page,Start):
    Pages=2193

    while (Page<Pages):
        isPageinList = 0
        Page = Page + 1

        Start = Start + Interval
        url_block2 = str(Start)
        url_block3 = str(Start + Interval)
        url="http://libwisenews.wisers.net/NewsSentiment/content.do?wp_dispatch=menu-content&menu-id=/commons/CFT-HK/DA000-DA003-DA010-/DA000-DA003-DA010-65029-&srp_save&cp&cp_s="+url_block2+"&cp_e="+url_block3
        #url = "http://libwisenews.wisers.net/wisenews/content.do?wp_dispatch" \
              #"=menu-content&menu-id=/userfolder/" + url_block1 + "-&srp_save&cp&cp_s=" + url_block2 + "&cp_e=" + url_block3
        with open(path + "/PageList", "a+")as foutpage:
            val_page = foutpage.readlines()
            if len(val_page) > 0:
                for tab in range(len(val_page)):
                    if url == val_page[tab]:
                        isPageinList = 1
                        break
                if isPageinList == 0:
                    foutpage.write(url + '\n')
            else:
                foutpage.write(url + '\n')


def GenePageUrl(page_urls):
    with open("Count.txt")as fin2:
        count_val=fin2.readlines()
    ArticleCount=int(count_val[0].strip())
    ArticleListCount=int(count_val[1].strip())
        #r = requests.get(url)
        #mycookie = "__p_scid_CITYULIB_ipaccess=\"CITYULIB@ipaccess|84502399|0|t1ms1|014c46fd1d6f\"; cMACHINECOOKIE=14c27a62e00; JSESSIONID=A17D0828B09A4238F94586DBA3AC07B9.wise19; gallery-simplegallery1=1; __reLoginUrl=\"\"; __lsid=^t1ms1.wisers.com^84502399; cUSERNAME=\"CITYULIB@ipaccess\"; __lst_libwisenews.wisers.net=1427110827442"
            #"__p_scid_CITYULIB_ipaccess=\"CITYULIB@ipaccess|84434622|0|t1ms1|014c4168733a\"; cMACHINECOOKIE=14c27a62e00; JSESSIONID=B5381EE186BFB6F87E75C01CD524D2BF.wise18; __reLoginUrl=\"\"; __lsid=^t1ms1.wisers.com^84434622; cUSERNAME=\"CITYULIB@ipaccess\"; __lst_libwisenews.wisers.net=1427024125134"


        #tab_pages=2#The max is 283
        #total_pages=0#The max is 283*50
    TotoalPageList=[]
    for tab_pages in range(len(page_urls)):
    #if tab_pages>=0:
        page_url=page_urls[tab_pages].strip()

        myheaders = {"Host": "libwisenews.wisers.net",
                     "Referer": "http://libwisenews.wisers.net/NewsSentiment/index.do?_",
                     "Content-type": "text/html; charset=utf-8",
                     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                     "Accept Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:36.0) Gecko/20100101 Firefox/36.0",
                     "Cookie": mycookie
                     }
        #print(page_url)
        r = requests.get(page_url, headers=myheaders)
        r.encoding = "Big5-HKSCS"
        listcontent = r.text
        beautiful_content = BeautifulSoup(listcontent)
        Temp = beautiful_content.findAll(name='a', attrs={'href': re.compile(r"/NewsSentiment/content\.do.*list")})

        #print("The length of Temp is "+str(len(Temp)))
        if len(Temp)==0:
            continue
        TitleList = []
        UrlList = []
        TempTitleList = []
        TempUrlList = []

        pattern1 = re.compile(r"/NewsSentiment/content\.do.*text")
        pattern2 = re.compile(r"<span class=\"ClipItemTitle\">.*</span>")

        for tab in range(len(Temp)):
            TempUrlList.append(pattern1.findall((str(Temp[tab]))))
            TempTitleList.append(pattern2.findall(str(Temp[tab])))

        for tab in range(len(Temp)):
            if len(TempUrlList[tab])>0:
                UrlList.append(base + str(TempUrlList[tab][0]).replace('amp;', ''))
            #else:
                #print("111111111111111111")
                #break
            if len(TempTitleList[tab])>0:
                TitleList.append(str(TempTitleList[tab][0]).replace('<span class="ClipItemTitle">', '').replace('</span>', ''))
            ArticleCount=ArticleCount+1




        if (len(UrlList) == 0):
            print("The Length of UrlList is 0 ")
        else:
            for tab_j in range(len(UrlList)):
                try:
                    TotoalPageList.append(str(TitleList[tab_j])+"@#$"+str(UrlList[tab_j]))
                except:
                    print(str(len(TitleList))+"/////////////////////"+str(len(UrlList))+str(tab_j))

            if ArticleCount>=(ArticleListCount+1)*10000:
                ArticleListCount+=1



                with open(path+"/ArticleList  "+str(ArticleListCount)+"~"+str(ArticleListCount+1)+"0000", "w")as fout:
                    #val = fout.readlines()
                    for tab1 in range(len(TotoalPageList)):
                        fout.write(TotoalPageList[tab1]+'\n')
                TotoalPageList=[]
                """
                    if len(val)>0:
                        print(len(val))
                        for tab1 in range(len(val)):
                            val_eachline = val[tab1]
                            for tab2 in range(len(UrlList)):
                                if UrlList[tab2] in val_eachline:
                                    continue
                                else:
                                    #print(TitleList[tab2] + "@#$" + UrlList[tab2]+'1111111111111111111\n')
                                    fout.write(TitleList[tab2] + "@#$" + UrlList[tab2]+'\n')
                    else:
                        for tab3 in range(len(UrlList)):
                            #print(TitleList[tab3] + "@#$" + UrlList[tab3]+'22222222222222222222\n')
                            fout.write(TitleList[tab3] + "@#$" + UrlList[tab3]+'\n')
                """

            with open("Count.txt","w")as fout2:
                fout2.write(str(ArticleCount)+'\n')
                fout2.write(str(ArticleListCount))
                            #fout.write(OutputText)
                            #except:
                            #TitleErrorList.append(TitleList[tab1])
            print("The " + str(ArticleCount) + " ArticleUrl_____is Complete!!!And The Length of Page Url is "+str(len(Temp)))
            #print(tab_pages)
            #time.sleep(10)


def RunCrawler(mycookie,newfilepath):

    if not os.path.isdir(newfilepath):
        os.makedirs(newfilepath)
    else:
        pass
        #shutil.rmtree(newfilepath)
        #os.makedirs(newfilepath)
    myheaders2 = {"Host":"libwisenews.wisers.net",
            "Referer":"http://libwisenews.wisers.net/NewsSentiment/index.do?new-login=true",
            "Content-type": "text/html; charset=utf-8",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:36.0) Gecko/20100101 Firefox/36.0",
            "Cookie":mycookie
        }

    path=os.getcwd()
    filelist=os.listdir(path)
    #t=0
    for eachfile in filelist:
        if "Article" in eachfile:
            ArticleCount=1
            with open(eachfile) as fin:
                print("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL"+str(eachfile))
                for eacharticle in fin:
                    #print("The "+str(ArticleCount)+" Article_____is Processing!!!")

                    (Title,Url)=eacharticle.split('@#$')
                    if not os.path.isfile(newfilepath+"/"+Title):
                        #t=t+1
                        #print(Title)
                        temprequest=requests.get(Url,headers=myheaders2)

                        soup=BeautifulSoup(temprequest.text)

                        scripttext=[x.extract() for x in soup.find_all('script')]

                        OutputText=soup.text.strip().replace('\n','')

                        pattern3=re.compile(r"\.ftNotice.*}")
                        OutputText2=pattern3.findall(OutputText)
                        #print("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT"+str(OutputText2[0]))
                        try:
                            pattern4=re.compile(OutputText2[0])
                            OutputText=pattern4.sub("###",OutputText)

                            if '/' in Title:
                                Title=Title.replace("/","")
                            elif '\\' in Title:
                                Title=Title.replace("\\","")
                            elif '（' in Title:
                                Title=Title.replace("（","")
                            elif '）' in Title:
                                Title=Title.replace("）","")
                            with open(newfilepath+"/"+Title,"w")as fout:
                                fout.write(OutputText)
                        except:
                            pass
                        #print("The "+str(ArticleCount)+" Article_____is Complete!!!")
                        ArticleCount=ArticleCount+1
                    else:
                        pass
                        #t=t+1
                #print(str(t)+"LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL"+str(eachfile))
                        #pass
                        #print("The "+str(ArticleCount)+" Article_____is Completed!!!")                        #TitleErrorList.append(Title)
        else:
            print("There is Error when crawlering Url!!!!!!!!!!")




from threading import Thread
import multiprocessing
import time
def worker():
    #name = multiprocessing.current_process().name
    #print(name, 'Starting')
    #global articleisinUrlList,ArticleListCountCount,ArticleCount,mycookie,base,Start, Interval, Page, path, newfilepath,PageErrorList,TitleErrorList,IndexErrorList
    para=Init(mycookie)
    GeneratePageListUrl(para[0],para[1],para[2])
    path=os.getcwd()
    with open(path + "/PageList")as fin_pageurl:
        page_urls= fin_pageurl.readlines()
    #for i in range(283):
        #print("hahahha"+str(i))
    GenePageUrl(page_urls)

    #time.sleep(2)
    #print(name, 'Exiting')
def worker2():
    Init(mycookie)
    name = multiprocessing.current_process().name
    print(name, 'I am doing nothing but just print..........................................\\\\\\')
    time.sleep(2)
    GenePageUrl()


def my_service():
    name = multiprocessing.current_process().name
    print(name, 'Starting')
    print(mycookie)
    time.sleep(10)
    RunCrawler(mycookie)
    #time.sleep(3)
    print(name, 'Exiting')
if __name__=="__main__":
    global A_count,B_count
    #para=Init()
    #GenerateUrl(para[0],para[1],para[2])
    #RunCrawler(mycookie)
    #Thread(target=GenerateUrl(para[0],para[1],para[2]),args=()).start()
    #Thread(target=RunCrawler(mycookie),args=()).start()
    #service = multiprocessing.Process(name='my_service',
                                      #target=my_service)
    #worker_1 = multiprocessing.Process(name='worker_1',target=worker)
    #worker_2 = multiprocessing.Process(target=worker2) # default name
#    global articleisinUrlList,ArticleListCountCount,ArticleCount,mycookie,base,Start, Interval, Page, path, newfilepath,PageErrorList,TitleErrorList,IndexErrorList
    OutputFileFolder = input("Please Input the File Folder that You Want to Save your Files...")
    newfilepath = os.getcwd() + '/' + str(OutputFileFolder)
    mycookie ="__p_scid_CITYULIB_ipaccess=\"CITYULIB@ipaccess|87409174|0|t2ms1|014d37fb41f3\"; cMACHINECOOKIE=14cf9f4476f; JSESSIONID=30164574E03195955B4EB83A2875DD7A.wise25; __reLoginUrl=\"\"; __lsid=^t2ms1.wisers.com^87409174; cUSERNAME=\"CITYULIB@ipaccess\"; __lst_libwisenews.wisers.net=1431121643978"
    with open("Count.txt","w")as fout2:
        fout2.write(str(0)+'\n')
        fout2.write(str(0))
    #worker()
    RunCrawler(mycookie,newfilepath)
    #worker_2.start()#notice avoid to write duplicate content
    #service.start()