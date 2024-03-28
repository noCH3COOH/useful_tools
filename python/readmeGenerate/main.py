from fileAnalysis import analysis_file
from emojiLog import emojiLog
import json
import tkinter as tk
import tkinter.filedialog as fd
import os

root = tk.Tk()
root.withdraw()

if __name__ == "__main__":

    path_target = fd.askdirectory(title='选择源工程文件夹')
    if not path_target:
        print('未选择路径，退出')
        exit()
    
    path_info = path_target + '/info.json'    
    path_log = 'log.txt'
    path_config = 'config.json'
    path_md = path_target + '/README.md'
    path_requirement = path_target + '/requirements.txt'

    log = open(path_log, encoding='utf-8', mode='w+')
    md = open(path_md, encoding='utf-8', mode='w+')
    require = open(path_requirement, encoding='utf-8', mode='w+')

    flag_infoExist = False    # 目标路径是否存在编写好的 info.json
    
    if os.path.exists(path_info):   # 检测目标路径是否存在编写好的 info.json
        with open(path_info, encoding='utf-8', mode='r') as infojson:
            info = json.load(infojson)
            infojson.close()
        project_name = info["project.name"]
        
        i = 1
        requirements = info["project.requirements"]
        project_requirements = []
        while i <= len(requirements):
            requirement = requirements["r" + str(i)]
            project_requirements.append(requirement["name"] + requirement["version"])
            i += 1
        
        i = 1
        functions = info["project.functions"]
        project_functions = []
        while i <= len(functions):
            function = functions["f" + str(i)]
            project_functions.append('|' + str(function["brief"]) + '|' + str(function["file"]) + '|' + str(function["how"]) + '|')
            i += 1
        
        i = 1
        modifies = info["project.modify"]
        project_modifies = []
        while i <= len(modifies):
            modify = modifies["m" + str(i)]
            project_modifies.append(modify["time"] + ' ' + emojiLog(modify["type"], modify["content"]))
            i += 1
        
        flag_infoExist = True
    else:
        project_name = os.path.dirname(path_md).split('/')[-1]
        project_requirements = '自己看代码'
        project_functions = '自己看代码'
        project_modifies = '自己记'

    log.write('【源工程】 ' + path_target + '\n')

    tree_str, his_fileExt = analysis_file(path_target)
    log.write('【文件结构】\n' + tree_str + '\n')
    log.write('【包含文件类型】 ' + str(his_fileExt) + '\n')

    # README.md 生成
    md.write('# ' + project_name + '\n')
    md.write('***\n')

    md.write('## 目录\n')
    md.write('- [项目简介](#项目简介)\n')
    md.write('- [依赖列表](#依赖列表)\n')
    md.write('- [安装过程](#安装过程)\n')
    md.write('- [使用方法](#使用方法)\n')
    md.write('\n')
    md.write('***\n')

    md.write('## 项目简介\n')
    md.write('\n')
    md.write('### 项目介绍\n')
    md.write('\n')
    md.write('### 项目结构\n')
    md.write('``` shell\n')
    md.write(tree_str)
    md.write('```\n')
    md.write('包含以下类型的文件：' + str(his_fileExt) + '\n')
    md.write('\n')
    md.write('***\n')

    md.write('## 功能列表\n')
    if flag_infoExist:
        md.write('|brief|file|how|\n')
        md.write('|:-:|:-:|:-:|\n')
        for pf in project_functions:
            md.write(pf + '\n')
    else:
        md.write(project_requirements + '\n')
    md.write('\n')
    md.write('***\n')

    md.write('## 依赖\n')
    if flag_infoExist:
        for pr in project_requirements:
            md.write(pr + '\n\n')
            require.write(pr + '\n')
    else:
        md.write(project_requirements + '\n')
        require.write(project_requirements + '\n')
    md.write('\n')
    md.write('***\n')

    md.write('## 安装过程\n')
    md.write('\n')
    md.write('***\n')

    md.write('## 使用方法\n')
    md.write('\n')
    md.write('***\n')

    md.write('## 更新日志\n')
    if flag_infoExist:
        for pm in project_modifies:
            md.write(pm + '\n\n')
    else:
        md.write('自己看代码\n')
    md.write('\n')
    md.write('***\n')
    
    log.write('【文件生成】 ' + path_md)
    os.system('explorer.exe ' + path_target.replace('/', '\\'))

    log.close()
    md.close()
    require.close()

    exit(0)
