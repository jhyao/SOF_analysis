import os
import re


def count_line(file_path):
    code = 0
    blank = 0
    note = 0
    for line in open(file_path, 'r', encoding='utf-8'):
        line = line.strip()
        if line:
            if line.startswith('#'):
                note += 1
            else:
                code += 1
        else:
            blank += 1
    print(f'{file_path}: {[code, note, blank]}')
    return code, note, blank

def loc_add(loc1, loc2):
    return [loc1[i] + loc2[i] for i in range(len(loc1))]

def loc(path, pattern):
    if not os.path.exists(path):
        return
    if os.path.isdir(path):
        pass
    if os.path.isfile(path):
        return count_line(path)
    loc_count = [0, 0, 0]
    for root, dirs, files in os.walk(path):
        for file in files:
            if re.match(pattern, file):
                loc_count = loc_add(loc_count, count_line(os.path.join(root, file)))
    print(f'{path} all:{sum(loc_count)}, code:{loc_count[0]}, note:{loc_count[1]}, blank:{loc_count[2]}')
    return loc_count

if __name__ == '__main__':
    loc(r'E:\SOF', '.*\.html$')
