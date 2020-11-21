from circular_buffer import circular_buffer
from threading import Thread,Semaphore
from time import sleep,time
from event_module import event
from divide_req import divide_req

number_producer = 5
number_consumer = 8
buffer_size = 20
request_number = 100

global successes
successes = 0
global count,size
count = 0
size = buffer_size

global event_producer,event_consumer
event_producer = event()
event_consumer = event()

global buffer
buffer = circular_buffer(buffer_size)
semaphore = Semaphore()

global count_request_producer
count_request_producer = 0
global count_request_consumer
count_request_consumer = 0

global check_stop_consumer
check_stop_consumer = 0

def append(name,req):                   #พิสูตร append sleep append 15    delay remove start 10
    global count,size
    global count_request_producer
    #sleep(10)
    while req > 0:
        req -=1

        if count > size-1:
            print(f'thread : {name} = sleep append')
            time_out = event_producer.sleep(seconds=5)
            
            
            if time_out == False:
                print(f'thread : {name} = append request false')
                continue
            print(f'thread : {name} = wake up append')

        semaphore.acquire()
        if count > size-1:
            req +=1
            semaphore.release()
            continue
        count_request_producer +=1  

        buffer.add_item('x')
        print("request",count_request_producer,f'producer-{name}',buffer.display())
        #print("request",count_request_producer)
        count +=1
        semaphore.release()
        sleep(0.05)
        if count > 0:
            event_consumer.wake_up()

def remove(name,req):
    global count,size,successes
    global count_request_consumer
    global check_stop_consumer
    sleep(0.5)
    while req > 0:
        req -=1

        if count < 1:
            print(f'thread : {name} = sleep remove')
            time_out = event_consumer.sleep(seconds=15)
            if time_out == False:
                print(f'thread : {name} = remove false')
                continue
            print(f'thread : {name} = wake up remove')
        
        semaphore.acquire()
        if count < 1:
            req +=1
            semaphore.release()
            continue
        count_request_consumer +=1

        item = buffer.remove_item()
        if item == 'x':
            successes = successes + 1
        print("request",count_request_consumer,f'consumer-{name}',buffer.display())
        count -=1
        semaphore.release()
        sleep(0.05)
        if count > 0:
            event_producer.wake_up()

    semaphore.acquire()
    check_stop_consumer += 1
    semaphore.release()

list_req_pro = divide_req(request_number,number_producer).value()
list_req_con = divide_req(request_number,number_consumer).value()

#print("pro",list_req_pro,"con",list_req_con)

start = time()
#create thread producer
for i,req in zip(range(number_producer),list_req_pro):
    producer_thread = Thread(target=append,args=(i,req))
    producer_thread.start()

   # Thread(target=)
#create thread consumer
for i,req in zip(range(number_consumer),list_req_con):
    consumer_thread = Thread(target=remove,args=(i,req))
    consumer_thread.start()
    if i == number_consumer-1:
        consumer_thread.join()

while check_stop_consumer < number_consumer:
    print('ddddddd')

end = time()
timer = end-start
print(f'time {timer}')
print(f'successes {successes}')