#!/usr/bin/env python3
# 百度主动推送（实时通知百度收录）。需要站长平台的推送 token。
#
# token 获取步骤：
#   1) 登录 https://ziyuan.baidu.com （百度搜索资源平台）
#   2) 站点管理 -> 添加并验证站点 shunar.cn
#   3) 左侧「链接提交」->「主动推送」-> 复制页面上的 token
#
# 用法：
#   python3 tools/baidu_push.py <你的百度推送token>
#
# 说明：脚本读取 sitemap.xml 里所有 <loc>（仅含可索引 URL，已排除 noindex 页面），
#       一次性推送给百度。建议每次发布/改动后跑一次。
import sys, urllib.request, urllib.error

ROOT = '/Users/bdeng/Documents/dbweb/shunarcn'
SITE = 'shunar.cn'
API = f'http://data.zz.baidu.com/urls?site={SITE}&token='


def main():
    if len(sys.argv) < 2:
        print('用法: python3 tools/baidu_push.py <百度推送token>')
        return
    token = sys.argv[1]
    urls = []
    for line in open(f'{ROOT}/sitemap.xml', encoding='utf-8'):
        line = line.strip()
        if line.startswith('<loc>'):
            urls.append(line[5:-6])
    if not urls:
        print('未在 sitemap.xml 中找到任何 <loc>，请先确认 sitemap。')
        return
    data = ('\n'.join(urls)).encode('utf-8')
    req = urllib.request.Request(API + token, data=data,
                                 headers={'Content-Type': 'text/plain'})
    try:
        resp = urllib.request.urlopen(req, timeout=20).read().decode('utf-8')
        print('百度返回:', resp)
        print(f'已推送 {len(urls)} 条 URL。')
    except urllib.error.URLError as e:
        print('推送失败:', e)


if __name__ == '__main__':
    main()
