"""
A module executable from the shell, it read stdin, it writes std out.

```bash
$ echo "db: ${DATABASE_URL-sqlite:///}" > config.yml
$ cat config.yml | python -m envsub
db: sqlite:///
```
"""

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
