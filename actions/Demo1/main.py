### Begin generated header
import sys
sys.path.append(__file__ + '/../../../../../include')
import lsss
### End generated header

import tkinter as tk
import tkinter.ttk as ttk

from datetime import datetime

import humanfriendly

zoom = lsss.get('/lsss/module/PelagicEchogramModule/zoom')

start = zoom[0]['time'][0:-1] + '000' + zoom[0]['time'][-1]
start = datetime.strptime(zoom[0]['time'], '%Y-%m-%dT%H:%M:%S.%fZ')

stop = zoom[1]['time'][0:-1] + '000' + zoom[1]['time'][-1]
stop = datetime.strptime(zoom[1]['time'], '%Y-%m-%dT%H:%M:%S.%fZ')

duration = humanfriendly.format_timespan(stop-start)
text = 'Echogram duration is {}\nExtends from {} to {}.'.format(duration, 
                             start.strftime('%d %b %Y %H:%M:%S'), 
                             stop.strftime('%d %b %Y %H:%M:%S'))

root = tk.Tk()
root.title('Echogram stats')

status = ttk.Label(root, text=text)
status.pack(side='top', ipadx=5, ipady=5)

ttk.Button(root, text='Close', command=root.destroy).pack(side='top')

root.mainloop()

