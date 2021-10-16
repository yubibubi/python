# 应用requests的方法，首先需要在开头导入requests包
import requests
# 代理ip格式：{"协议类型":"ip:端口"}
# 在开头导入parsel数据解析模块
import parsel
# 网页响应需要时间，因此代码中需要设置延时
import time

import json
# ---------------------------------------
def check_ip(proxies_list):
    """检测代理ip质量"""
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.47'}

    can_use = []
    for proxy in proxies_list:
        
        try:
            # 下一条代码揭示了如何使用代理ip
            response = requests.get('https://weibo.com/u/6585424401/home?wvr=5',headers=headers,proxies=proxy,timeout=0.1)# 响应时间超过0.1s，则不合格
            if response.status_code == 200: # 证明访问成功
                can_use.append(proxy)
        except Exception as e:
            print(e)
        finally:
            print('当前ip：',proxy,' 检测通过')
    
    return can_use
# ---------------------------------------


# 空列表，存放字典值
proxies_list = []

# 翻页爬取，用for循环遍历每一页
for page in range(1,2):
    print('=======================正在获取第{}页数据======================='.format(page))
    # 获取url路径
    base_url = 'https://www.kuaidaili.com/free/inha/{}/'.format(page)

    # headers参数的数据类型为字典
    # headers参数具体获取方法：
    #   1.在网页中右键进入“检查”（即开发者模式）
    #   2.选择“Network”(网络)，刷新
    #   3.任意选择一项网页内容，选中“headers”
    #   4.提取其中所需元素
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.47'}

    # 在网页headers的General处可查看网页请求方法，如果是GET方式，我们就需要用requests的get方法
    # 返回响应数据
    response = requests.get(base_url,headers=headers)
    # print(response.request.headers) #不加headers等于裸奔 # 测试函数

    # data存储响应数据中的文本信息（即网页源代码）
    data = response.text
    # print(data) # print输出在控制台显示的内容不完整
    # 尝试将内容放在txt文件中
    # file_1 = open('1.txt','w',encoding='utf-8') # 测试函数
    # file_1.write(data) # 测试函数


    # 转换数据类型
    html_data = parsel.Selector(data)

    # 数据解析
    # 通过xpath函数进行精确定位
    # //符号表示跨节点获取，用@进行精准定位
    parse_list = html_data.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr')


    # 遍历for循环
    for tr in parse_list:
        # xpath提取规范，tr数据标签下标从1开始（29:41）
        http_type = tr.xpath('./td[4]/text()').extract_first() # 提取协议类型
        ip_num = tr.xpath('./td[1]/text()').extract_first() # 提取地址
        ip_port = tr.xpath('./td[2]/text()').extract_first() # 提取端口
        # print(http_type,ip_num,ip_port) # 测试函数

        # 构建ip字典
        dict_proxies = {}
        dict_proxies[http_type] = ip_num + ':' + ip_port
        # print(dict_proxies) # 测试函数

        # 将各条信息以字典键值对形式存放于列表
        proxies_list.append(dict_proxies)

        # 降低获取速度，给浏览器反应时间 
        time.sleep(0.2)

# print("获取到的ip数量：",len(proxies_list)) # 测试函数
# print(proxies_list) # 测试函数

# can_use中存储符合条件的代理ip，可直接使用，或存入数据库
can_use = check_ip(proxies_list)
# print("能用的代理ip：",can_use)
# print("能用的代理ip数量：",len(can_use))

file_1 = open('1.txt','w+')
for line in can_use:
    file_1.write(json.dumps(line))
file_1.close()

