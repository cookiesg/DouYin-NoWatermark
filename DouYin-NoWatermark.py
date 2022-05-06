from dataclasses import dataclass, replace
from distutils.log import info
from logging import exception
from unicodedata import name
from prettytable import PrettyTable
import requests as rq
import re

headers = {"user-agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/100.0.4896.60"}
   
def getVideoInfo(url):
    get_locationAddress = rq.get(url,headers=headers,allow_redirects=False)
    new_url = get_locationAddress.headers["Location"]
    VideoId = re.findall(r"https://www.iesdouyin.com/share/video/(.*?)/",new_url)[0]
    Api = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids="+str(VideoId)
    DataList = rq.get(Api,headers=headers).json()
    PlayAddress = DataList["item_list"][0]["video"]["play_addr"]["url_list"][0]
    replaceAddress = PlayAddress.replace ("playwm","play")                            
    nickName = DataList["item_list"][0]["author"]["nickname"]
    share_title = DataList["item_list"][0]["share_info"]["share_title"]
    try:
      play_url =  DataList["item_list"][0]["music"]["play_url"]["uri"]
    except Exception as e:
         play_url = e
    finally: 
     return replaceAddress,nickName,share_title,play_url

if __name__ == "__main__":
 input_url = input("请输入抖音分享链接:")
 if input_url.find("https://v.douyin.com/") != -1:
      dyurl = re.findall(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",input_url)[0]
      VideoAddress = getVideoInfo(dyurl) 
      x = PrettyTable()
      x.title="抖音视频信息"
      x.field_names=["视频地址","昵称","视频标题","音乐地址"]
      x.add_row([VideoAddress[0],VideoAddress[1],VideoAddress[2],VideoAddress[3]])
      print(x)
      input_info = input("是否下载视频？(Y/N)").upper()
      if input_info == "Y":
           print("正在使出吃奶的力气下载视频，请稍等...")
           res = rq.get(VideoAddress[0],headers=headers).content
           with open(VideoAddress[1]+".mp4","wb") as f:
              f.write(res)
              f.close()
           print("视频下载完成！")
      elif input_info == "N":
          print("您选择了不下载视频，欢迎下次再来！")
 else:
        print("输入的链接有误，再见！")
        exit()
