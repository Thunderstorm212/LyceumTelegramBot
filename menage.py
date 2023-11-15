from assets.build import build
from assets.status import Statuses
import os
import sys
import threading
import status_remove
import time

if __name__ == '__main__':

    if sys.argv[0]:
        status_remove_thread = threading.Thread(target=status_remove.update_date)
        build_thread = threading.Thread(target=build)
        try:


            # status_remove_thread.join()
            # print(time.time())

            status_remove_thread.setDaemon(True)
            status_remove_thread.start()
            # print(time.time())

            # #
            # build_thread.start()
            # build_thread.join()
            if build():
                Statuses(1)
        except Exception as e:
            print(e)




