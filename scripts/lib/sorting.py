import random
from multiprocessing import Process,Manager,Pipe,Queue
def QuickSortListArray(A):
        if len(A)<=1:
                return A
        else:
                PivotValue=A.pop(0)
                pvVal=int(PivotValue[0])
                lesser=[x for x in A if x[0] < pvVal]
                greater=[x for x in A if x[0] > pvVal]
                pv=[x for x in A if x[0] == pvVal]
                pv.append(PivotValue)
        return QuickSortListArray(lesser)+pv+QuickSortListArray(greater)

def QuickSortMPListArray(A,conn,NumProcs):
        if len(A)<=1 :
                conn.send(A)
                conn.close()
        elif int(NumProcs)<1:
                conn.send(QuickSortListArray(A))
                conn.close()
        else:
                lesser=[]
                greater=[]
                pv=[]
                Pivot=A.pop(0)
                pvVal=int(Pivot[0])
                lesser=[x for x in A if x[0] < pvVal]
                greater=[x for x in A if x[0] > pvVal]
                pv=[x for x in A if x[0] == pvVal]
                pv.append(Pivot)
                Procs=int(NumProcs)-1
                pConnLeft,cConnLeft=Pipe()
                leftProc=Process(target=QuickSortMPListArray,args=(lesser,cConnLeft,Procs))
                pConnRight,cConnRight=Pipe()
                rightProc=Process(target=QuickSortMPListArray,args=(greater,cConnRight,Procs))
                

                leftProc.start()
                rightProc.start()
                conn.send(pConnLeft.recv()+pv+pConnRight.recv())
                conn.close()
        
                leftProc.join()
                rightProc.join()
        return

