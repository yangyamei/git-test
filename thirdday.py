from multiprocessing import Process,Queue,Lock
import time,queue,requests
def get_content(url,q,i):
    result={}            #创建多进程访问url返回结果的空字典
    while True:
        try:
            q.get(block=False)   #从队列中取出值，如果为空，则抛出empty异常
        except queue.Empty:
            break
        try:
            r=requests.get(url)  #请求url
        except:
            result['error']=result.setdefault('error',0)+1  #若请求异常，字典中创建error键，键值加1
        else:
            result[r.status_code]=result.setdefault(r.status_code,0)+1 #否则字典中创建返回码的键，键值+1
        for item in result:
            print("进程%d的访问结果：status_code[%s]:%d"%(i+1,item,result.get(item))) #使用for循环遍历字典，打印出请求url的结果
if __name__=="__main__":
    starttime=time.time()
    count=100
    num=2
    url='http://www.baidu.com'
    q=Queue() #存放进程的列表
    processs=[]
    for i in range(count):
        q.put(i)
    for i in range(num):
        p=Process(target=get_content,args=(url,q,i))
        processs.append(p)  #将进程放入进程列表
        p.start()    #开启进程
    for p in processs:
        p.join()     #等待进程结束
    endtime=time.time()
    t=endtime-starttime
    print("spentime:%d"% t)