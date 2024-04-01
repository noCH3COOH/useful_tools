import os
from pathlib import Path

tree_str = ''

# 遍历子文件夹并复制文件
def analysis_file(path):
    # 后缀名历史
    his_fileExt = [] 
    global tree_str

    tem = os.listdir(".")

    for dir in tem:
        dirname = dir.split('/')[-1]
        if not (dirname.startswith('.') or dirname.startswith('__') or '.' in dirname):
            generate_fileTree(dir, 1)

    for subdir, dirs, files in os.walk(path):
        if not files:
            continue

        for file in files:
            filename = os.path.splitext(file)
            file_ext = filename[1]
            filename = filename[0].split('/')
            filename = filename[-1]

            if not file_ext:
                file_ext = '无后缀'

            if file_ext not in his_fileExt:
                his_fileExt.append(file_ext)
    
    return tree_str, his_fileExt

def generate_fileTree(path, n=0):
    global tree_str
    target = Path(path)
    
    if target.is_dir():
        if (not target.name.startswith('.')) and (not target.name.startswith("__")):
            tree_str += '    |' * n + '-' * 4 + str(target.relative_to(target.parent)) + '\n'
            for cp in target.iterdir():
                generate_fileTree(cp, n + 1)

def calcu_size(size):
    count = 0
    while size >= 1024:
        size /= 1024
        count += 1
    
    size = '%.3f' % size
    
    if 0 == count:
        return str(size) + 'B'
    elif 1 == count:
        return str(size) + 'KB'
    elif 2 == count:
        return str(size) + 'MB'
    elif 3 == count:
        return str(size) + 'GB'
    else:
        return str(size) + 'TB'