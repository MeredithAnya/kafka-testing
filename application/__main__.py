import sys
from .bootstrap import bootstrap
from .producer import produce
from .consumer import consume

def main():
    print("setting up kafka...")
    bootstrap()
    print("producing messages...")
    produce()
    print("consuming messages...")
    consume()

if __name__ == '__main__':
    sys.exit(main())