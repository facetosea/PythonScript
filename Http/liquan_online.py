#!/usr/bin/env python
import re
import os
import json

def getChangeReq( gid, giftCounts ):
	changeAssetReq='''curl -X PATCH   http://10.111.65.60:80/ams/v1/user/asset   -H 'content-type: application/json'   -d '{"appId":13001,"assetId":"1004","changeCount":"'''
	changeAssetReq += str(giftCounts)
	changeAssetReq += '''","changeType":"3","gid":"'''
        changeAssetReq += str(gid)
        changeAssetReq += '''","pluginId":"","serialNum":"'''
	changeAssetReq += "lqbufa" + str(gid)
	changeAssetReq += '''","serverId":13001,"sign":"","sourceId":1}' '''
        return changeAssetReq

def getGiftCount( index ):
        print "*********"
        print type(index)
        print index
        print "************"
	val = 0
	if index==1:
		val = 288888
	elif index== 2:
		val = 88888
	elif index == 3:
		val = 58888
	elif index == 4:
		val = 38888
	elif index <= 8:
		val = 8888
	elif index <= 16:
		val = 5888
	elif index <= 32:
		val = 3888
	elif index <= 64:
		val = 1888
	elif index <= 128:
		val = 888
	else:
		val= 88
        return val

fr =open('mingci.txt','r')
alllines=fr.readlines()
fr.close()
flog=open('log.txt','a+')
flog.writelines("\n new test*************************\n")
num = 0
for eachline in alllines:
        num += 1
        flog.writelines("\n\n ****  user " + str(num)+ "  start \n" )
        user = re.findall(r"\d+\.?\d*",eachline)
        index = user[0]
        userid = user[1]
	reuest = "curl -X GET http://10.111.67.9:9001/uc/v1/users?appId=13001\&userId=" + userid
        flog.writelines(reuest + '\n')
		
	getUsergid = os.popen(reuest).read()
	flog.writelines(getUsergid)
        userinfo = json.loads(getUsergid)
	if ('errCode' in userinfo) :
            pass
        else:
            flog.writelines("has not errCode Key")
	    continue
        if userinfo['errCode'] != str(0):
	   continue
	changeReq = getChangeReq(userinfo['data']["gid"], getGiftCount(int(index)) )
        flog.writelines(str(userinfo['data']["gid"]) +  "  mingci:" + str(index)+'\n' )
	flog.writelines(changeReq + '\n')
        changeAsset = os.popen(changeReq).read()
	flog.writelines(changeAsset)
flog.close()
