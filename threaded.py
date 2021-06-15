from _thread import start_new_thread
import pdb

trades = []
count = 0

def add_trade():
    global count
    global trades
    count = count + 1
    trades.append(count)

for i in range(1, 10000000):
    if i % 1000000 == 0:
        start_new_thread(add_trade, ())
        print(trades)
        pdb.set_trace()