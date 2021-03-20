#!/bin/python3
import sys
import os

if len(sys.argv) < 3:
    print(f'usage: {os.path.basename(sys.argv[0])} src dest')
    sys.exit(1)

src = sys.argv[1]
dest = sys.argv[2]

with open(src, 'rb') as sf:
    data = sf.read()

size = len(data)
idx = 168
eol = '\n' if os.name == 'posix' else '\r\n'
with open(dest, 'w') as df:
    while idx < size:
        total_len = data[idx] | data[idx + 1] << 8
        idx += 4
        code_len = (data[idx] | data[idx + 1] << 8) * 2
        idx += 2
        code = data[idx:idx + code_len].decode('utf-16')
        idx += 8
        value_len = total_len - 16
        value = data[idx:idx + value_len].decode('utf-16')
        idx += value_len + 2
        df.write(f'{code} {value}{eol}')
