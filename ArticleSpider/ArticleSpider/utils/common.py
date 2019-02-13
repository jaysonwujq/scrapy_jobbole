import hashlib

def get_md5(url):   #传进来url
    if isinstance(url, str):  #判断是不是str，其实是判断是不是Unicode，python3中默认是Unicode编码
        url = url.encode("utf-8") #转换成utf-8，哈希只认utf-8
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()