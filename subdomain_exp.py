import socket,requests,queue,threading


def scan(url):
    for dic in open("./sub.txt"):#./python/sec tool/tool/sub.txt
        url1=(dic+url).replace("\n","")
        try:
            ip=socket.gethostbyname(url1)
            print("url:"+url1+"\nip:"+ip+"\n")
        except Exception as e:
            pass


if __name__ == "__main__":
    url=input("url:")
    scan(url)
