# Douyin_Spider

### 声明：项目内容不用于商业用途，仅做学习交流，如果侵犯了您的权益,请邮箱联系我，我将删除该项目


| 作者   | 邮箱           |
| ------ | -------------- |
| Muking | mj2754@126.com |

#### 介绍

批量爬取抖音视频

#### 项目架构

1. 使用 Python 编写后端爬虫部分,Python_QT实现页面UI设计；
2. 下载过用户信息保存为json文件，在./json目录，之后可以选择更新加载新视频，无需重新输入分享链接信息

#### 目录结构

```
DY.py           #控制台版抖音爬虫程序
UI_DY.py        #UI版抖音爬虫程序
```

#### 需要的参数

```
url 分享链接      # 可以从 手机 端用户主页点击分享中获取到链接
```

#### 运行环境

```
Python 3.8
```

#### 环境依赖库

##### Python

- requests==2.21.0

- retrying==1.3.3

- PyQt5==5.15.1

#### 安装依赖
``` python
pip install -r  requirement.txt #即可一键安装依赖
```
#### 程序运行
```    python
python DY.py or python UI_DY.py    #即可开始爬取视频。
```
### 注:

#### 如果有项目问题，可以发邮箱沟通或者在线提交issues，我会在空余时间及时回复的

#### 下载过的用户信息保存在./json目录

#### 可以选择更新新视频，无需重新输入分享链接信息
