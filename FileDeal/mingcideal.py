#!/usr/bin/env python`
import re
f=open('mingci.txt','r')
alllines=f.readlines()
f.close()
f=open('mingci_new.txt','w+')
for eachline in alllines:
	aaa = eachline.split(':',7)
    #a=re.sub('hello','cctv',eachline);
        ss = aaa[4]+aaa[5]
        ss = re.sub('UserID', '', ss)
        ss = re.sub('Stage', '', ss)
	f.writelines(ss +"\n")
f.close()
