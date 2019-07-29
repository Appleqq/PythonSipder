from aip import AipFace
import base64
from urllib import parse
import requests
import os
import time

'''
from PIL import Image
import glob
from PIL import ImageFile
'''

""" 你的 APPID AK SK """
APP_ID = "16130432"
API_KEY = "rfO9YGKnCXRknGtNONaseTiT"
SECRET_KEY = "GZ57SwRYG7udPCNZWZZe4zvG6lKdpgND"

''' 服务器信息'''
SESSION_ID = ''
BASE_URL = 'http://cmp.xspinfo.com:90/jsonServer.php'


def compareImages():
    img1 = base64.b64encode(
        open('/Users/xiaohonghong/Desktop/PythonSpider/personImages/IMG_20190427_112858.jpg', 'rb').read())
    pic1 = str(img1, 'utf-8')
    img2 = base64.b64encode(
        open('/Users/xiaohonghong/Desktop/PythonSpider/personImages/IMG_20190427_113002.jpg', 'rb').read())
    pic2 = str(img2, 'utf-8')
    client = AipFace(APP_ID, API_KEY, SECRET_KEY)
    result = client.match([
        {
            'image': "%s" % pic1,
            'image_type': 'BASE64',
            'face_type': 'LIVE',
            "quality_control": "NONE"
        },
        {
            'image': "%s" % pic2,
            'image_type': 'BASE64',
            'face_type': 'LIVE',
            "quality_control": "NONE"
        }
    ])
    print(result)


def searchUserInfo(imageFilePath):
    img1 = base64.b64encode(
        open(imageFilePath, 'rb').read())
    pic1 = str(img1, 'utf-8')

    imageType = 'BASE64'
    groupIdList = 'sp'

    client = AipFace(APP_ID, API_KEY, SECRET_KEY)
    result = client.search(pic1, imageType, groupIdList)
    return result['result']['user_list'][0]['user_id']


'''
用本地的图片，服务器图片做对比
相识度 大于80% 为本人
'''


def compareInfoImage(imageFilePath, imageUrl, personInfo):
    img1 = base64.b64encode(
        open(imageFilePath, 'rb').read())
    pic1 = str(img1, 'utf-8')
    pic2 = imageUrl
    client = AipFace(APP_ID, API_KEY, SECRET_KEY)
    result = client.match([
        {
            'image': "%s" % pic1,
            'image_type': 'BASE64',
            'face_type': 'LIVE',
            "quality_control": "NONE"
        },
        {
            'image': "%s" % pic2,
            'image_type': 'URL',
            'face_type': 'LIVE',
            "quality_control": "NONE"
        }
    ])
    try:
        if 'score' in result['result']:
            print('score')
            if result['result']['score'] > 80.0:
                print('是本人 %s' % result['result']['score'])
                if os.path.isfile(imageFilePath) == True:
                    new_name = personInfo['name'] + '.jpg'
                    os.rename(imageFilePath,
                              os.path.join('/Users/xiaohonghong/Desktop/PythonSpider/personImages mini', new_name))
                    print('文件改名成功')
                else:
                    print('文件不存在')
            else:
                print('不是本人 %s' % result['result']['score'])
        else:
            print(result)
    except:
        print('score 不存在')


"""
登录服务器

"""


def loginserver():
    user = 'pp'
    pwd = 'PPaZJ992560'
    stamp = getTimeStamp()
    print(stamp)
    parmrs = {'action': 'Login',
              'cid': '6',
              'jsonstr': '{"clientVersion":"2.0","souse":"Eomp","pwd":"PPaZJ992560","user":"Pp"}',
              'stamp': stamp,
              }

    response = requests.get(BASE_URL, parmrs)
    session_ID = response.json()['content']['sessionid']

    return session_ID


"""
获取通讯录数据

"""


def geAllAddressInfo(session_id):
    stamp = getTimeStamp()
    parmrs = {'action': 'addrbookList',
              'cid': '6',
              'jsonstr': '{"clientVersion":"2.0","keywords":"","type":"1","page":"0"}',
              'stamp': stamp,
              'sessionid': session_id
              }
    response = requests.get(BASE_URL, parmrs)
    datas = response.json()['content']
    return datas


"""
获取个人信息

"""


def getUserInfo(user_id, session_id):
    stamp = getTimeStamp()
    parmrs = {'action': 'contactDetail',
              'cid': '6',
              'jsonstr': '{"clientVersion":"2.0","Enum":"%s"}' % user_id,
              'stamp': stamp,
              'sessionid': session_id
              }
    response = requests.post(BASE_URL, parmrs)
    return response.json()['content']


"""
文件改名

"""


def changeLocalFilename(filePath, userInfo):
    if os.path.isfile(filePath) == True:
        new_name = userInfo['name'] + '.jpg'
        os.rename(filePath,
                  os.path.join('/Users/panping/Desktop/searchImage', new_name))
        print('文件改名成功')


"""
上传用户信息到百度云

"""


def uploadUserInfo(user_avatar_url, userInfo):
    image = user_avatar_url
    imageType = 'URL'
    groupId = 'sp'
    user_id = userInfo['eNum']

    client = AipFace(APP_ID, API_KEY, SECRET_KEY)
    result = client.addUser(image, imageType, groupId, user_id)
    print(result)


"""
时间戳指定格式

"""


def getTimeStamp():
    timestamp = str(time.time())
    timestamp_sc = timestamp + "_SPCMP"
    stamp = base64.b64encode(timestamp_sc.encode('utf-8'))
    return stamp


def matchImages(datas, session_id):
    stamp = getTimeStamp()
    for personInfo in datas:
        stamp = getTimeStamp()
        parmrs = {'action': 'getAvatar',
                  'cid': '6',
                  'jsonstr': '{"clientVersion":"2.0","enum":"%s"}' % personInfo['eNum'],
                  'stamp': stamp,
                  'sessionid': session_id
                  }
        respose = requests.get(BASE_URL, parmrs)
        uploadUserInfo(respose.url, personInfo)
        # macthLocalImage(imageUrl=respose.url, personInfo=personInfo)
        # print(respose.url)


def macthLocalImage(imageUrl, personInfo):
    print(imageUrl)
    rootdir = '/Users/xiaohonghong/Desktop/PythonSpider/personImages mini'
    list = os.listdir(rootdir)
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        if os.path.isfile(path):
            if 'jpg' in path:
                print('++%s' % path)
                compareInfoImage(imageUrl=imageUrl, imageFilePath=path, personInfo=personInfo)


def lookOnLocal():
    rootdir = '/Users/panping/Desktop/searchImage'
    list = os.listdir(rootdir)
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        if os.path.isfile(path):
            if 'jpg' in path:
                user_id = searchUserInfo(imageFilePath=path)
                user_info = getUserInfo(user_id, SESSION_ID)
                changeLocalFilename(path, user_info)


'''
def scaleImage():
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    #in_dir = os.getcwd()  # 当前目录
    in_dir = '/Users/xiaohonghong/Desktop/PythonSpider/personImages'
    out_dir = in_dir + ' mini'  # 转换后图片目录
    ##percent = 0.4#缩放比例
    percent = 0.1
    if not os.path.exists(out_dir): os.mkdir(out_dir)
    for files in glob.glob(in_dir + '/*.jpg'):
        filepath, filename = os.path.split(files)
        im = Image.open(files)
        w, h = im.size
        im = im.resize((int(w * percent), int(h * percent)))
        im.save(os.path.join(out_dir, filename))
'''

if __name__ == '__main__':
    # STEP_1 登录系统，获取系统通讯录数据
     session_ID = loginserver()

    # datas = geAllAddressInfo(session_ID)

    # matchImages(datas, session_ID)

    # scaleImage()
     SESSION_ID = session_ID
     lookOnLocal()

