from ccm.lib.actr import *

class Hanoi(ACTR):
    goal = Buffer()
    retrieve = Buffer()
    # memory = Memory(retrieve)
    memory=Memory(retrieve,threshold=-3)
    DMNoise(memory,noise=0.3)
    
    def init():
        memory.add('move A C')
        memory.add('move A B')
        memory.add('move C B')
        memory.add('move B A')
        memory.add('move B C')
        memory.add('move C A')
    
    def initializeHanoi(goal='hanoi disk1:None?loc1 disk2:None?loc2 disk3:None?loc3 Endpeg:?end'):
        print('All disks start at A and they need to be moved to', end)
        goal.modify(disk1='A', disk2='A', disk3='A')
        memory.request('move A ?end')
    
    def terminateHanoi(goal='hanoi disk1:?end disk2:?end disk3:?end Endpeg:?end'):
        print('All disks have been moved to', end)
        print('Disk 1 is at', end, 'Disk 2 is at', end, 'Disk 3 is at', end)
        goal.set('done')
        print('All moves completed')
        
    def moveDisk1(goal='hanoi disk1:?loc1 disk2:?loc2 disk3:?loc3 Endpeg:?end', # disk 1 can always be moved
                   retrieve='move ?loc1 ?next'):
        print('Move disk 1 from', loc1, 'to', next)
        if next != loc2: # if disk1 is not going to the same peg as disk2
            memory.request('move ?loc2 !?next') # Don't move disk 2 to the same peg as disk 1
        else: # if disk1 and disk2 are on the same peg
            memory.request('move ?loc3 !?loc2')
        goal.modify(disk1=next)

    def moveDisk2(goal='hanoi disk1:?loc1 disk2:?loc2!?loc1 disk3:?loc3 Endpeg:?end', # only move disk 2 if disk 1 is not on the same peg as it, and where it is going
                   retrieve='move ?loc2 ?next!?loc1'):
        print('Move disk 2 from', loc2, 'to', next)
        memory.request('move ?loc1 ?next') # move disk 1 to the same peg as disk 2
        goal.modify(disk2=next)
        
    def moveDisk3(goal='hanoi disk1:?loc1 disk2:?loc2 disk3:?loc3!?loc2!?loc1 Endpeg:?end', # only move disk 3 if disk 1 and 2 are not on the same peg as it, and where it is going
                   retrieve='move ?loc3 ?next!?loc1!?loc2'):
        print('Move disk 3 from', loc3, 'to', next)
        memory.request('move ?loc1 !?next') # move disk 1 away from disk 2 to and not to the same peg as disk 3
        goal.modify(disk3=next)
    

model = Hanoi()
model.goal.set('hanoi disk1:None disk2:None disk3:None Endpeg:C') # 1 is the smallest disk, 3 is the largest disk, end at C
model.run()

# n disks
# first do 1 to n-1
# then from n-2 to 1
# then do n
# then do 1 to n-2
# then from n-3 to 1
# then do n-1
