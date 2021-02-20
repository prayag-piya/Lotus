from Engine.processer import kamal
from Engine.parser import totalHits, parsing
from threading import Thread
from network.scanner import *


def main():
    # obj = kamal()
    # obj.packets()
    th = Thread(target=servicescan)
    th.start()


main()
