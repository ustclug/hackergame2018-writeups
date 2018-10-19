
data = open('typed_printf.cpp', 'rb').read().split('\n')[:-1]
result = ''
for line in data:
    tmp_line = line[0] + line[32:39] + line[1:7] + line[20:22] + line[8:20] + line[22:32] + line[39:]
    while(len(tmp_line) and tmp_line[-1] == ' '):
        tmp_line = tmp_line[:-1]
    result += tmp_line+'\n'
open('typed_printf_fixed.cpp', 'wb').write(result)