#!/usr/bin/env python  
#coding:UTF-8  
#1.通过参数自动登录ssh远程服务器  
#2.通过配置字符集解决中文乱码问题  
#3.解决改变远程窗口默认较小bug，远程窗口同本地窗口大小动态改变未处理  
#4.实现2级代理  


"""
没有参数是ssh模式，有参数是scp模式
scp模式示例：
connect down /opt/pig_home/persona/DailyActivityPopulationPresentFeature.pig /home/david/code/audiences/persona/persona
然后再选择需要scp的服务器

如果是递归scp
connect down /opt/pig_home/persona /home/david/code/audiences/persona/persona 1

"""
  
import os,sys,pexpect,string  
import struct,fcntl,termios,signal  
  
try:  
    import pexpect  
except:  
    print "你没有pexpect包，试试sudo apt-get install python-pexpect"  
    sys.exit(0)  
  
def sigwinch_passthrough(sig,data):  
    """窗口改动后，自动返回当前窗口值，以便跟远程窗口同步,目前有问题"""  
    s=struct.pack("HHHH",0,0,0,0)  
    a=struct.pack('hhhh',fcntl.ioctl(sys.stdout.fileno(),termios.TIOCGWINSZ,s))  
  
class SimpleSsh:  
    def __init__(self):  
        self.columns=125  
        self.lines=37  
        self.base="~/ssh/"  
        self.filename="/home/david/code/shell/login/host.properties"

        if len(sys.argv) > 1:
            self.type=sys.argv[1]
            self.file1 = sys.argv[2]
            self.file2 = sys.argv[3]
            self.is_r = 0
            if len(sys.argv) == 5:
                # 1 means -r
                self.is_r = sys.argv[4]
        
  
    def createSshUrl(self,paramap):  
        user=paramap["user"]  
        password=paramap["password"]  
        host=paramap["host"]
        port=paramap["port"]  
        #url="luit -encoding GBK ssh -p "+port+" " +user+"@"+host  
        url="luit ssh -p "+port+" " +user+"@"+host  
        
        print url 
          
        return url,password  

    def createScpUrl(self,paramap):
        user=paramap["user"]  
        password=paramap["password"]  
        host=paramap["host"]
        port=paramap["port"]
        url = ""
        if self.type=="down":
            if self.is_r == "1":
                url="luit scp -r -P "+port+" " +user+"@"+host + ":" + self.file1 + " " + self.file2
            else:
                url="luit scp -P "+port+" " +user+"@"+host + ":" + self.file1 + " " + self.file2 
        else:
            if self.is_r == "1":
                url="luit scp -r -P "+port+" " + self.file1 + " " + user+"@"+host + ":" + self.file2
            else:
                url="luit scp -P "+port+" " + self.file1 + " " + user+"@"+host + ":" + self.file2

        print url

        return url,password
  
    def connection(self,url,password):  
        """ """
        lines, columns = os.popen('stty size', 'r').read().split()  
        try:  
            p=pexpect.spawn(url)  
            try:  
                p.setwinsize(int(lines),int(columns))  
                print "resize windows(%s,%s)"%(columns,lines)  
            except:  
                pass  
            p.expect("password:")  
            p.sendline(password)  
            p.interact()  
        except:  
            print "connection close()"  
      
    def argv2map(self,id):  
        paramap={}  
        base=self.base  
        filename=self.filename  
        tmp=""  
        try:  
            file=open(filename,"r")  
        except:  
            file=open(string.join(base,filename))  
        content=file.readlines()  
  
        for x in content:  
            if x.startswith(id):  
                tmp=string.strip(x)  
                break
  
        if tmp=="":  
            print "not found %s"%host  
            sys.exit(0)  
  
        tmparray=string.split(tmp,":")  
        paramap["user"]=tmparray[2]  
        paramap["password"]=tmparray[3]  
        paramap["host"]=tmparray[1]  
        paramap["port"]=tmparray[4]  
  
        return paramap  
  
    def handle(self,para):  
        paramap=self.argv2map(para)  
        # 有参数就是scp模式，否则就是ssh模式
        if len(sys.argv) >1:
            url,password = self.createScpUrl(paramap)
            self.connection(url,password)
        else:
            url,password=self.createSshUrl(paramap)  
            self.connection(url,password) 

    def printConfig(self):
	print('--------------------------------------')
        file=open(self.filename,"r")
        content=file.readlines()
	for x in content:
	    arr = string.split(x,':')
	    print(arr[0]+' -- '+arr[1]+' -- '+arr[2])
	print('--------------------------------------')
	 
  
if __name__=="__main__":     
    print sys.argv[0]
    b=SimpleSsh()
    b.printConfig()
    print("选择服务器id")
    id = raw_input()
   
    b.handle(id)
