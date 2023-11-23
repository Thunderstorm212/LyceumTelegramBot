from assets.build import build
import sys
import threading
from db import status_remove

if __name__ == '__main__':

    if sys.argv[0]:
        try:
            status_remove_thread = threading.Thread(target=status_remove.update_date)
            build_thread = threading.Thread(target=build)
            status_remove_thread.setDaemon(True)

            print("Run Thread status remover")
            status_remove_thread.start()

            print("Run build telegram bot")
            build()
        except Exception as e:
            print(e)
