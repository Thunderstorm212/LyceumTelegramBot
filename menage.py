from assets.build import build
from assets.status import Statuses
import os
import sys
import threading
import status_remove

if __name__ == '__main__':

    if sys.argv[0]:
        try:
            status_remove_thread = threading.Thread(target=status_remove.update_date)
            build_thread = threading.Thread(target=build)
            status_remove_thread.setDaemon(True)

            if status_remove_thread.start():
                Statuses(2)
            if build():
                Statuses(1)
        except Exception as e:
            print(e)
