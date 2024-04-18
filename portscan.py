import socket,threading,sys,time


#tcp扫描
def scan1(ip,port,openports):
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((ip,port))
        outcome=f"{port} open"
        #print(f"{port} open")
        openports.append(outcome)
    except:
        pass
    finally:
        s.close()

#udp扫描
def scan2(ip, port, openports):
    print('Server %s, Port: %s is scanning' % (ip, port))  # 打印IP和端口
    try:
        port = int(port)  # 整数型port
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket 实例化
        s.settimeout(5)  # 设置超时时间
        s.sendto(b'11', (ip, port))  # 发送数据
        try:
            r, i = s.recvfrom(1024)
            print(r)
            if r:
                #print(f"{port} open")
                outcome=f"主机：{ip}\n{port} open"
                openports.append(outcome)
            else:
                #print('close')
                outcome=f"主机：{ip}\n{port} close"
                openports.append(outcome)
        except socket.timeout:
                outcome=f"主机：{ip}\n{port} close"
                openports.append(outcome)
    except Exception as e:
        print(f"Error scanning port {port}: {e}")
    finally:
        s.close()  # 关闭套接字

#线程分配
def thread(ip,ports,flag):

    count=0

    #模式选择
    if flag==1:
        mode=scan1
    elif flag==2:
        mode=scan2

    openports=[]
    threads = []
    for port in ports:
        t=threading.Thread(target=mode,args=(ip,int(port),openports))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
 
    return openports

#主函数
def main():
    banner()
     #ip="bilibili.com"
    ports=[]
    type=""
    type1=""
    flag=0
    ip=input("请输入ip：")
    while type!="1" or type!="2":
        type=input("模式1：固定端口/模式2：全端口\n")
        if type=="1":
            ports=input("请输入端口号，用英文','分割\n").split(",")
            break
        elif type=="2":
            st=int(input("起始端口："))
            ed=int(input("结束端口："))
            for i in range(st,ed+1):
                ports.append(i)
            break
        else:
            print("模式错误")

    while type1!="1" or type1!="2":
        type1=input("模式1：tcp/模式2：udp\n")
        if type1=="1":
            flag=1
            break
        elif type1=="2":
            flag=2
            break
        else:
            print("模式错误")
   
    print("\n开始扫描\n")
    time1=time.time()
    openports=thread(ip,ports,flag)
    time2=time.time()
    time3=time2-time1
    print("------------------------------------------------------\n")
    print("扫描结果\n")
    for port in openports:
        print(port)
    
    print(f"\n扫描用时：{round(time3,2)}s\n")
    print("------------------------------------------------------\n")

#banner
def banner():
    banner_text="""
  _____ _________   ____    _    _   _ 
 | ____|__  / ___| / ___|  / \  | \ | |
 |  _|   / /\___ \| |     / _ \ |  \| |
 | |___ / /_ ___) | |___ / ___ \| |\  |
 |_____/____|____/ \____/_/   \_\_| \_|

 author:yiranloveyou

 """
    
    print(banner_text)


if __name__ == "__main__":
    while(1):
        main()
        restart = input("是否需要重新开始？(y/n): ")
        if restart.lower() == 'n':
            sys.exit()