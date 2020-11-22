from circular_buffer import circular_buffer
from threading import Thread,Semaphore
from time import sleep,time
from event_module import event
from divide_req import divide_req

x = input("# buff ").split(" ")

producer_thread = int(x[0])
consumer_thread = int(x[1])
buffer_size = int(x[2])
request_number = int(x[3])

print(f"Producers {producer_thread}, Consumers {consumer_thread}")
print(f"Buffer size {buffer_size}")
print(f"Requests {request_number}\n")

number_producer = producer_thread
number_consumer = consumer_thread
buffer_size = buffer_size
request_number = request_number
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

def append(name,req):
    global count,size
    global count_request_producer
    while req > 0:
        req -=1

        if count > size-1:
            time_out = event_producer.sleep(seconds=5) #seconds = 0.05 may processes false
            
            if time_out == False:
                continue

        semaphore.acquire()
        if count > size-1:
            req +=1
            semaphore.release()
            continue
         

        buffer.add_item('x')
        #print("request",count_request_producer,f'producer-{name}',buffer.display())
        count +=1
        semaphore.release()
        #sleep(0.00002)
        if count > 0:
            event_consumer.wake_up()

def remove(name,req):
    global count,size,successes
    global count_request_consumer
    global check_stop_consumer

    sleep(0.0005)
    while req > 0:
        req -=1

        if count < 1:
            time_out = event_consumer.sleep(seconds=5)
            if time_out == False:
                continue
        
        semaphore.acquire()
        if count < 1:
            req +=1
            semaphore.release()
            continue
        count_request_consumer +=1

        item = buffer.remove_item()
        if item == 'x':
            successes = successes + 1
        count -=1
        semaphore.release()
        
        if count > 0:
            event_producer.wake_up()

    semaphore.acquire()
    check_stop_consumer += 1
    #print('count stop =',check_stop_consumer)
    semaphore.release()

list_req_pro = divide_req(request_number,number_producer).value()
list_req_con = divide_req(request_number,number_consumer).value()

#print("pro",list_req_pro,"con",list_req_con)

start = time()
#create thread producer
for i,req in zip(range(number_producer),list_req_pro):
    producer_thread = Thread(target=append,args=(i,req))
    producer_thread.start()

#create thread consumer
for i,req in zip(range(number_consumer),list_req_con):
    consumer_thread = Thread(target=remove,args=(i,req))
    consumer_thread.start()

    if i == number_consumer-1:
        consumer_thread.join()
#stop
while check_stop_consumer < number_consumer:
    pass
    sleep(0.005)
    #print('dddddddd')

end = time()
timer = end-start
print(f'Successfully consumed {successes} requests ({(successes/request_number)*100}%)')
print(f'Elapsed Time: {timer} s ')
print(f'Throughput: {successes/timer} successful requests/s')