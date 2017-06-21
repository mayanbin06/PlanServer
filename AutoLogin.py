import urllib2
import urllib
import zlib
import base64
import gzip
import json
import uuid

import cookielib
import urllib2, httplib
import StringIO, gzip
import io

Host = '666.xbgg8.com'
BaseUrl = 'http://666.xbgg8.com/'
IndexUrl = '?s=/Index/'
VerifyUrl = "?s=/ApiPublic/getNewCaptcha/"

class LoginController:
    def __init__(self):
        self.headers = { 'Host': Host,
                    'Connection':'keep-alive',
                    'Accept': '*/*; q=0.01',
                    'X-Requested-With': 'XMLHttpRequest',
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
                    'Referer': BaseUrl + IndexUrl,
                    'Origin': BaseUrl,
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.8,ja;q=0.6'
                    }
        cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    
        post_data = urllib.urlencode({})
        response = self.opener.open(BaseUrl + IndexUrl)
    
        data = zlib.compress("\"\"")
        post_data = 'zipinfo=' + base64.b64encode(data[2:-4])
        print post_data
    
        req = urllib2.Request(BaseUrl + VerifyUrl, post_data, self.headers)
        response = self.opener.open(req);
        rdata = json.loads(gzdecode(response.read()))
    
        # get image
        req = urllib2.Request(BaseUrl + rdata['info'], headers=self.headers)
        response = self.opener.open(req);
        data = response.read()
        image_data= gzdecode(data)
    
        output = open('verify.png', 'wb')
        output.write(image_data)
    def RefreshVerifyCode(self):
        data = zlib.compress("\"\"")
        post_data = 'zipinfo=' + base64.b64encode(data[2:-4])
        print post_data
    
        req = urllib2.Request(BaseUrl + VerifyUrl, post_data, self.headers)
        response = self.opener.open(req);
        rdata = json.loads(gzdecode(response.read()))
    
        # get image
        req = urllib2.Request(BaseUrl + rdata['info'], headers=self.headers)
        response = self.opener.open(req);
        data = response.read()
        image_data= gzdecode(data)
    
        filename = "/static/image/verify.png"
        output = open(filename, 'wb')
        output.write(image_data)
        return filename
    def Login(self, user, password, verifycode):
        return True
    def __del__(self):
        return

def gzdecode(data):
    compressedstream = StringIO.StringIO(data)
    gziper = gzip.GzipFile(fileobj=compressedstream)
    data2 = gziper.read()
    return data2

if __name__ == '__main__':
    Login()

