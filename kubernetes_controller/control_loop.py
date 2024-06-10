from threading import Thread, Lock
import time


class globalVars:
    pass


G = globalVars()  # empty object to pass around global state
G.lock = Lock()  # not really necessary in this case, but useful none the less
G.value = 0
G.kill = False


def run_job_controller(n):  # function doing intense computation
    for i in range(n):
        if G.kill:
            G.kill = False
            return
        time.sleep(n)  # super intense computation
        with G.lock:
            G.value += i


t = Thread(target=foo, args=(10,))
t.start()


def askinput():
    # change to raw_input for python 2.7
    choice = input(
        "1: get G.value\n2: get t.isAlive()\n3: kill thread\nelse: exit\ninput: "
    )
    if choice == "1":
        with G.lock:
            print(G.value)
    elif choice == "2":
        print(t.is_alive())
    elif choice == "3":
        G.kill = True
    else:
        return 0
    return 1


while askinput():
    pass
