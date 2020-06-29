import sys, threading, time

def test():
    while True:
        time.sleep(2)
        sys.stdout.write("testasd\n")
        sys.stdout.flush()

t = threading.Thread(target=test)
t.start()
while True:
    a = sys.stdin.readline()
