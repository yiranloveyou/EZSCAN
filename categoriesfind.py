import requests,queue,threading,sys,time,socket
from rich import print
from rich.progress import Progress
from urllib.parse import urlparse

#用于探测主机存活
def is_alive(url):
    parsed_url = urlparse(url)
    if  parsed_url.scheme:
        url = parsed_url.netloc + parsed_url.path
    try:
        ip=socket.gethostbyname(url)
        print("主机存活\n"+"url:"+url+"\nip:"+ip+"\n")
        flag=1
    except Exception as e:
        print("不可访问 或 发送错误"+str(e))
        flag=0
    return flag

#扫描功能
def ctscan(url_queue,progress, finished_threads,successful_urls):

    headers={
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76"
    }
    #依次检测队列状态码
    while not url_queue.empty():
        try:
            url=url_queue.get()
            response=requests.get(url=url,headers=headers)
            if response.status_code !=404:
                outcome="URL:"+url+"  code:"+str(response.status_code)+"\n"
                successful_urls.append(outcome)
                print("发现目标！ URL:"+url+"  code:"+str(response.status_code)+"\n")
            else:
                pass
                #print("no")
        except Exception as e:
            pass
            #print("error:"+str(e))
        #更新线程进度条
        with progress:
            progress.update(finished_threads, advance=1)

#线程分配
def thread(url,th_num):
    #记录结果
    successful_urls = []
    url_queue=get_url(url)
    #用来显示进度条
    total_tasks = url_queue.qsize()
    with Progress() as progress:
        task_id = progress.add_task("运行进度", total=total_tasks)
        #记录完成线程数
        finished_threads = 0

        threads = []
        for i in range(th_num):
            t=threading.Thread(target=ctscan,args=(url_queue, progress, task_id,successful_urls))
            threads.append(t)
            t.start()
        
        #阻塞线程，等待所有子线程运行完毕后再执行后面的代码
        for t in threads:
            t.join()
            finished_threads += 1
    return successful_urls

#子目录拼接
def get_url(url):
    url_queue=queue.Queue()
    parsed_url = urlparse(url)
    # 如果没有指定协议，默认使用 https
    if not parsed_url.scheme:
        url = "https://" + url

    for dic in open("./dirList.txt"):#./python/sec tool/tool/minilist.txt
        #url="bilibili.com"
        #url1="https://"+url+"/"+dic
        url1=url+"/"+dic
        url_queue.put(url1)

    return url_queue

#banner
def banner():
    banner_text="""
  _____ _________   ____    _    _   _ 
 | ____|__  / ___| / ___|  / \  | \ | |
 |  _|   / /\___ \| |     / _ \ |  \| |
 | |___ / /_ ___) | |___ / ___ \| |\  |
 |_____/____|____/ \____/_/   \_\_| \_|

 author:yiranloveyou
 ps:输入exit可以退出QWQ                                                        
 """
    
    print(banner_text)

#主程序
def main():

    banner()

    url=""
    flag=0
    num=0

    #小校验
    while(flag!=1):
        url=input("\n请输入目标url:")   
        if url=="exit":
            print("退出成功")
            sys.exit()
        flag=is_alive(url)
        if flag==1:
            is_alive(url)
        elif flag==0:
            is_alive(url)

    while(num!=1):
        th_num=input("请设置线程数量:")
        if th_num=="exit":
            print("退出成功")
            sys.exit()
        num=th_num.isdigit()
        if num!=1:
            print("请输入数字！")

    print("-----------------------------------------------------------------\n")
    print("开始运行\n")
    st=time.time()
    #url="bilibili.com"
    #th_num=10
    successful_urls=thread(url,int(th_num))

    et=time.time()
    ut=et-st
    print("-----------------------------------------------------------------\n")
    print("运行结束\n")
    print("运行时间："+str(round(ut,2))+"s"+"\n")
    print("-----------------------------------------------------------------\n")
    print("运行结果:\n")
    for outcome in successful_urls:
        print(outcome)
    print("-----------------------------------------------------------------\n")

       
if __name__ == "__main__":
    while(1):
        main()
        restart = input("是否需要重新开始？(y/n): ")
        if restart.lower() == 'n':
            sys.exit()