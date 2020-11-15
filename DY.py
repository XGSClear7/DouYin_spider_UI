#!/usr/bin/env python
# encoding: utf-8
'''
#-------------------------------------------------------------------
#                   CONFIDENTIAL --- CUSTOM STUDIOS                      
#-------------------------------------------------------------------
#                                                                   
#                   @Project Name : 抖音下载小助手
#                                                                   
#                   @File Name    : main.py                      
#                                                                           
#                                                                   
#-------------------------------------------------------------------
'''
import os, sys, requests
import json, re, time
from retrying import retry
from contextlib import closing

def sec_name(mstr):
    import re
    rstr = r"[\/\\\:\*\?\"\<\>\|]" # '/ \ : * ? " < > |'
    string = re.sub(rstr, "", mstr)
    return string
def chin_name(mstr):
    reg = "[^\u4e00-\u9fa5]"
    return re.sub(reg, '', mstr)
def clear():
    if os.name=='nt':
        y=os.system('cls')
    else:
        y=os.system('clear')
def timechange(timeStamp):
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d_%H-%M-%S", timeArray)
    #print(otherStyleTime)   # 2013--10--10 23:40:00
    return otherStyleTime
def get_sec_uid(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    # 请求网页
    response = requests.get(url, headers=headers)
    #print(response.status_code)  # 打印响应的状态码
    real_url=response.url
    sec_uid=real_url.split("sec_uid=")[1].split("&")[0]
    return sec_uid
def getjsonfilelist(name=None):
    filePath = './json/'
    if not os.path.exists(filePath):
        os.makedirs(filePath)
        return None
    filelist=os.listdir(filePath)
    #print(filelist)
    jsonlist=[]
    for file in filelist:
        if name!=None:
            if ('.json' in file) and (name in file):
                jsonlist.append(file)
        else:
            if ('.json' in file):
                jsonlist.append(file)
    return jsonlist
def getauthor(jsonlist):
    author_list=[]
    for jsonfile in jsonlist:
        with open(f'./json/{jsonfile}','r', encoding='UTF-8') as file:
            jsontemp=json.load(file,strict=False)
            author_list.append({
                'sec_uid': re.sub(r'[\/:*?"<>|]', '', jsontemp['sec_uid']) if jsontemp['sec_uid'] else None,
                'nickname': jsontemp['作者']
            })
    return author_list
class DouYin:
    '''
     This is a main Class, the file contains all documents.
     One document contains paragraphs that have several sentences
     It loads the original file and converts the original file to new content
     Then the new content will be saved by this class
    '''
    def __init__(self):
        '''
        Initial the custom file by some url
        '''
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'Accept-Encoding': 'gzip',
            'X-SS-REQ-TICKET': '1605327720127',
            'sdk-version': '1',
            'User-Agent': 'ttnet okhttp/3.10.0.2',
            'Cookie': 'odin_tt=7458fec70d09eef39b6340587c8d357d0b82df5ea96e70cf55f1fa4cb65072697aa292cadc63e8c1e4a184f98fa5b804; sid_guard=0de12f14cd59d51310bf8dc7e776a3ce%7C1605327216%7C5183893%7CWed%2C+13-Jan-2021+04%3A11%3A49+GMT',
}

    def hello(self):
        '''
        This is welcome speech
        :return: self
        '''
        print("*" * 50)
        print(' ' * 15 + '抖音下载小助手')
        print(' ' * 15 + '无水印 | 有水印')
        print(' ' * 12 + '输入用户的分享链接')
        print(' ' * 2 + '用抖音打开用户页分享，复制链接即可')
        print("*" * 50)
        return self

    def get_video_urls(self, sec_uid, type_flag='p'):
        '''
        Get the video link of user
        :param type_flag: the type of video
        :return: nickname, video_list
        '''
        user_url_prefix = 'https://www.amemv.com/web/api/v2/aweme/post' if type_flag == 'p' else 'https://www.amemv.com/web/api/v2/aweme/like'
        item_url='https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids='
        userinfo_url='https://www.amemv.com/web/api/v2/user/info/?uid='
        print('---解析视频链接中...\r')
        i = 0
        result = []
        max_cursor=0
        has_more=True
        while has_more :
            i = i + 1
            print('---正在第 {} 次尝试...\r'.format(str(i)))
            user_url = user_url_prefix + f'/?sec_uid={sec_uid}&count=2000&max_cursor={max_cursor}' 
            response = self.get_request(user_url)
            html = json.loads(response.content.decode())
            has_more,max_cursor=html['has_more'],html['max_cursor']
            if html['aweme_list'] != []:
                result += html['aweme_list']
      
        nickname = None
        video_list = []
        author={}
        i=0
        uid=result[0]['author']['uid']
        u_url =userinfo_url+str(uid)
        response = self.get_request(u_url)
        resp_json= json.loads(response.content.decode())
        author['user_id'] = resp_json['user_info']['uid']
        author['粉丝'] = resp_json['user_info']['follower_count']
        author['简介'] = resp_json['user_info']['signature'].replace('\n', ',').replace(' ', '')
        author['喜欢作品'] = resp_json['user_info']['favoriting_count']
        author['作者'] = resp_json['user_info']['nickname'].replace('\n', ',').replace(' ', '')
        author['作品'] = resp_json['user_info']['aweme_count']
        author['获赞'] = resp_json['user_info']['total_favorited']
        author['抖音号'] = resp_json['user_info']['unique_id']
        author['关注'] = resp_json['user_info']['following_count']
        author['sec_uid'] = result[0]['author']['sec_uid']
        for item in result:  
            if nickname is None:
                nickname = item['author']['nickname'] if re.sub(r'[\/:*?"<>|]', '', item['author']['nickname']) else None
            datetime=timechange(int(item['video']['origin_cover']['uri'].split("_")[-1])) if len(item['video']['origin_cover']['uri'].split("_"))>1 else None
            if datetime==None:
                aweme_id=item['statistics']['aweme_id']
                v_url =item_url+str(aweme_id)
                response = self.get_request(v_url)
                html = json.loads(response.content.decode())
                datetime=timechange(int(html['item_list'][0]['create_time']))
            
            url=item['video']['play_addr']['url_list']
            video_list.append({
                'desc': re.sub(r'[\/:*?"<>|]', '', item['desc']) if item['desc'] else nickname,
                'url': url,
                'time':datetime
            })
        author['video']=video_list
        with open(f"./json/{nickname}.json","w",encoding='utf-8') as f:
            json.dump(author,f,ensure_ascii=False,indent=4)
        return nickname, video_list
        
    def get_download_url(self, video_url, watermark_flag):
        '''
        Whether to download watermarked videos
        :param video_url: the url of video
        :param watermark_flag: the type of video
        :return: the url of o
        '''
        if watermark_flag == True:
            download_url = video_url.replace('api.amemv.com', 'aweme.snssdk.com')
        else:
            download_url = video_url.replace('aweme.snssdk.com', 'api.amemv.com')

        return download_url

    def video_downloader(self, video_url, video_name, watermark_flag=False):
        '''
        Download the video
        :param video_url: the url of video
        :param video_name: the name of video
        :param watermark_flag: the flag of video
        :return: None
        '''
        size = 0
        video_url = self.get_download_url(video_url, watermark_flag=watermark_flag)
        with closing(requests.get(video_url, headers=self.headers, stream=True)) as response:
            chunk_size = 1024
            content_size = int(response.headers['content-length'])
            if response.status_code == 200:
                filesize=content_size / chunk_size / 1024
                if filesize==0:
                    return 0
                sys.stdout.write('----[文件大小]:%0.2f MB\n' % filesize)
                with open(video_name + '.mp4', 'wb') as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        size += len(data)
                        file.flush()

                        sys.stdout.write('----[下载进度]:%.2f%%' % float(size / content_size * 100) + '\r')
                        sys.stdout.flush()
                return 1     
            else:
                return 0
    @retry(stop_max_attempt_number=3)
    def get_request(self, url, params=None):
        '''
        Send a get request
        :param url: the url of request
        :param params: the params of request
        :return: the result of request
        '''
        if params is None:
            params = {}
        response = requests.get(url, params=params, headers=self.headers, timeout=10)
        assert response.status_code == 200
        return response

    @retry(stop_max_attempt_number=3)
    def post_request(self, url, data=None):
        '''
        Send a post request
        :param url: the url of request
        :param data: the params of request
        :return: the result of request
        '''
        if data is None:
            data = {}
        response = requests.post(url, data=data, headers=self.headers, timeout=10)
        assert response.status_code == 200
        return response

    def run(self):
        '''
        Program entry
        '''
        file_list=getjsonfilelist()
        author_list=[]
        name_list=[]
        if file_list:
            author_list=getauthor(file_list)
            print('己有本地信息的主播如下:\n')
            author_num=1
            for author in author_list:
                name=author['nickname']
                name_list.append(name)
                print(f'{author_num}-{name}')
                author_num+=1
        if author_list!=None and len(author_list)>0:
            no = input('获取指定用户的视频，(默认)添加新用户 输入[1-{}]更新现有用户视频:'.format(len(name_list)))
            if not no:
                sec_uid = get_sec_uid(input('请输入新用户的分享链接:'))
            elif  int(no) in range(1,len(name_list)+1):
                sec_uid=author_list[int(no)-1]['sec_uid']
            else:
                sec_uid = get_sec_uid(input('请输入新用户的分享链接:'))
        else:
            sec_uid = get_sec_uid(input('请输入新用户的分享链接:'))
        sec_uid = sec_uid if sec_uid else 'MS4wLjABAAAAle_oORaZCgYlB84cLTKSqRFvDgGmgrJsS6n3TfwxonM'
        watermark_flag = input('是否下载带水印的视频 (0-否(默认), 1-是):')
        watermark_flag = bool(int(watermark_flag)) if watermark_flag else 0

        type_flag = input('p-上传的(默认), l-收藏的:')
        type_flag = type_flag if type_flag else 'p'

        save_dir = input('保存路径 (默认"./Download/"):')
        save_dir = save_dir if save_dir else "./Download/"

        nickname, video_list = self.get_video_urls(sec_uid, type_flag)
        nickname_dir = os.path.join(save_dir, nickname)

        if not os.path.exists(nickname_dir):
            os.makedirs(nickname_dir)

        if type_flag == 'f':
            if 'favorite' not in os.listdir(nickname_dir):
                os.mkdir(os.path.join(nickname_dir, 'favorite'))

        print('---视频下载中: 共有%d个作品...\r' % len(video_list))

        for num in range(len(video_list)):
            print('---正在解析第%d个视频链接 [%s] 中，请稍后...\n' % (num + 1, video_list[num]['desc']))
            
            title=video_list[num]['time']+video_list[num]['desc'] if video_list[num]['time']!=None else video_list[num]['desc']
            video_path = os.path.join(nickname_dir,title ) if type_flag != 'f' else os.path.join(nickname_dir, 'favorite', video_list[num]['desc'])
            if  os.path.exists(video_path+'.mp4'):
                print('---视频已存在...\r\n')
                continue
            else:
                for url in video_list[num]['url']:
                    succeed=self.video_downloader(url, video_path, watermark_flag)
                    if succeed:
                        break
            print('\n')
        print('---下载完成...\r\n')

if __name__ == "__main__":
    DouYin().hello().run()
    print("程序结束")
    time.sleep(5)
