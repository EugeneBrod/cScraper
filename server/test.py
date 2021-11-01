from threading import Thread, Event
import time

class Counter(Thread):

  def __init__(self, stop_event, interrupt_event):
    self.x = 0
    self.stop_event = stop_event
    self.interrupt_event = interrupt_event
    Thread.__init__(self)
    
  def run(self):
    while not self.stop_event.is_set():
      print(self.x)
      self.x += 1
      time.sleep(1)

STOP_EVENT = Event()
INTERRUPT_EVENT = Event()
thread = Counter(STOP_EVENT, INTERRUPT_EVENT)

def resetThread():
  STOP_EVENT = Event()
  INTERRUPT_EVENT = Event()
  thread = Counter(STOP_EVENT, INTERRUPT_EVENT)
  return thread, STOP_EVENT, INTERRUPT_EVENT

def start(thread, STOP_EVENT, INTERRUPT_EVENT):
  if thread.is_alive():
    print("thread in use")
  else:
    if STOP_EVENT.is_set():
      print("here")
      thread, STOP_EVENT, INTERRUPT_EVENT = resetThread()
    thread.start()
  return thread, STOP_EVENT, INTERRUPT_EVENT

def stop():
  STOP_EVENT.set()
  thread.join()

thread, STOP_EVENT, INTERRUPT_EVENT= start(thread, STOP_EVENT, INTERRUPT_EVENT)
print(thread.is_alive())
thread, STOP_EVENT, INTERRUPT_EVENT= start(thread, STOP_EVENT, INTERRUPT_EVENT)
stop()
time.sleep(5)
thread, STOP_EVENT, INTERRUPT_EVENT= start(thread, STOP_EVENT, INTERRUPT_EVENT)
time.sleep(10)
stop()




