#!/usr/bin/env python3
# coding: utf-8


from modules.daemons import *

bd = BunnyDaemon()
if len(sys.argv) != 2:
    print("Usage: python3 bunny.py start|stop|restart|status")
    exit(1)
else:
    if sys.argv[1] == 'start':
        bd.start()
    elif sys.argv[1] == 'stop':
        bd.stop()
    elif sys.argv[1] == 'restart':
        bd.restart()
    elif sys.argv[1] == 'status':
        bd.status()
    else:
        print("Usage: python3 bunny.py start|stop|restart|status")
        exit(1)




