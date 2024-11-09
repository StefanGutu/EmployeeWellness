import keyboard
from pynput.mouse import Controller
from time import sleep
import threading

block_input_flag = 0  

def blockinput():
    global block_input_flag
    block_input_flag = 1
    t1 = threading.Thread(target=blockinput_start)
    t1.start()
    print("[SUCCESS] Input blocked!")

def unblockinput():
    global block_input_flag
    block_input_flag = 0  
    blockinput_stop()  
    print("[SUCCESS] Input unblocked!")

def blockinput_start():
    mouse = Controller()
    global block_input_flag
    for i in range(150):
        keyboard.block_key(i)  
    while block_input_flag == 1:  
        mouse.position = (0, 0)  

def blockinput_stop():
    global block_input_flag
    for i in range(150):
        keyboard.unblock_key(i) 
    block_input_flag = 0  


#This will be an example how its works
# blockinput()  
# print("Now blocking...")
# sleep(10)  
# unblockinput()  
# print("Now unblocking.")