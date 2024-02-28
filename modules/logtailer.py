#!/usr/bin/env python3
# coding: utf-8

from modules.utils import *
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class LogFileHandler(FileSystemEventHandler, Logger):
    def __init__(self, log_file):
        FileSystemEventHandler.__init__(self)
        Logger.__init__(self)
        self.log_file = log_file
        self.file = open(log_file, 'r')
        self.file.seek(0, 2)  # 将文件指针移到文件末尾

    def on_modified(self, event):
        if event.src_path == os.path.abspath(self.log_file):
            new_content = self.file.read()
            print(new_content, end='', flush=True)


class LogTailThread(threading.Thread):
    def __init__(self, log_file):
        super().__init__()
        self.log_file = log_file
        self.event_handler = LogFileHandler(log_file)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, os.path.dirname(os.path.abspath(log_file)), recursive=False)
        self.observer.start()

    def run(self):
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()

    def stop(self):
        self.observer.stop()
        self.join()
