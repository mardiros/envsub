import sys
from .envsub import sub


def main():
    cnt = 0
    while True:
        cnt += 1
        res = sub(sys.stdin).read()
        if not res:
            return
        else:
            print(res, end="")


if __name__ == "__main__":
    main()
