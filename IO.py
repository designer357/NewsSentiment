__author__ = 'chengmin'
from threading import Thread

from threading import Event as TEvent

from multiprocessing import Process

from multiprocessing import Event as PEvent

from timeit import Timer

def countdown(n,event):

	while n > 0:

		n -= 1

	event.set()

def io_op(n,event):

	f = open('test.txt','w')

	while not event.is_set():

		f.write('hello,world')

	f.close()

def t1():

	COUNT=100000000

	event = TEvent()

	thread1 = Thread(target=countdown,args=(COUNT,event))

	thread1.start()

	thread1.join()

def t2():

	COUNT=100000000

	event = TEvent()

	thread1 = Thread(target=countdown,args=(COUNT//2,event))

	thread2 = Thread(target=countdown,args=(COUNT//2,event))

	thread1.start(); thread2.start()

	thread1.join(); thread2.join()

def t3():

	COUNT=100000000

	event = PEvent()

	p1 = Process(target=countdown,args=(COUNT//2,event))

	p2 = Process(target=countdown,args=(COUNT//2,event))


	"""

	p3 = Process(target=countdown,args=(COUNT//8,event))

	p4 = Process(target=countdown,args=(COUNT//8,event))
	p5 = Process(target=countdown,args=(COUNT//8,event))

	p6 = Process(target=countdown,args=(COUNT//8,event))




	p7 = Process(target=countdown,args=(COUNT//8,event))

	p8 = Process(target=countdown,args=(COUNT//8,event))
 	"""

	p1.start(); p2.start()
	p1.join(); p2.join()


#931561691663
#6222 5302 5375 8283



	"""
	p3.start(); p4.start()

	p5.start(); p6.start()
	p7.start(); p8.start()
	p1.join(); p2.join()
	p3.join(); p4.join()
	p5.join(); p6.join()
	p7.join(); p8.join()
	"""

def t4():

	COUNT=100000000

	event = TEvent()

	thread1 = Thread(target=countdown,args=(COUNT,event))

	thread2 = Thread(target=io_op,args=(COUNT,event))

	thread1.start(); thread2.start()

	thread1.join(); thread2.join()

def t5():

	COUNT=100000000

	event = PEvent()

	p1 = Process(target=countdown,args=(COUNT,event))

	p2 = Process(target=io_op,args=(COUNT,event))

	p1.start(); p2.start()

	p1.join(); p2.join()

if __name__ == '__main__':

	t = Timer(t1)

	print('countdown in one thread:%f'%(t.timeit(1),))

	t = Timer(t2)

	print('countdown use two thread:%f'%(t.timeit(1),))

	t = Timer(t3)

	print('countdown use two Process:%f'%(t.timeit(1),))

	t = Timer(t4)

	print('countdown in one thread with io op in another thread:%f'%(t.timeit(1),))

	t = Timer(t5)

	print('countdown in one process with io op in another process:%f'%(t.timeit(1),))