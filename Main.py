__author__ = 'chengmin'
from Sentiment import *
import os
#encoding=utf-8
import genius
filelist=os.listdir(os.path.join(os.getcwd(),"inputfolder"))
for eachfile in filelist:
    print(ComputeSentiment(os.path.join(os.path.join(os.getcwd(),"inputfolder"),eachfile)))


#seg_list = genius.seg_text(
#    text,
#    use_combine=True,
#    use_pinyin_segment=True,
#    use_tagging=True,
#    use_break=True
#)
#print('\n'.join(['%s\t%s' % (word.text, word.tagging) for word in seg_list]))