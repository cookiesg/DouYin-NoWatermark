from dataclasses import replace
import requests as rq
import re

headers = {"user-agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/100.0.4896.60"}

def get_location(url):
    get_locationAddress = rq.get(url,headers=headers,allow_redirects=False)
    new_url = get_locationAddress.headers["Location"]
    VideoId = re.findall(r"https://www.iesdouyin.com/share/video/(.*?)/",new_url)[0]
    return VideoId
   
def getNoWatermarkAddress(id):
    
    Api = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids="+str(id)
    PlayAddress = rq.get(Api,headers=headers).json()["item_list"][0]["video"]["play_addr"]["url_list"][0]
    replaceAddress = PlayAddress.replace ("playwm","play")
    return replaceAddress      

if __name__ == "__main__":
    
    dycopy =r"抖音分享链接复制到此处"
    
    url = re.findall(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",dycopy)[0]
    VideoID = get_location(url)
    VideoAddress = getNoWatermarkAddress(VideoID)
    print(VideoAddress)