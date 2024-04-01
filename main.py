from fileAnalysis import analysis_file
import os

type_exist_dir = []

tool_name = []
tool_dir = []

if __name__ == "__main__":
    tree_str, his_fileExt = analysis_file(".")

    print("Welcome to the tool manager!")
    print("You have the following file structure: ")
    print(tree_str)

    tem = os.listdir(".")

    for dir in tem:
        dirname = dir.split('/')[-1]
        if not (dirname.startswith('.') or dirname.startswith('__') or '.' in dirname):
            type_exist_dir.append(dirname)
    
    print("You have tools in these type:")
    print(type_exist_dir)
    
    for type in type_exist_dir:
        for dir in os.listdir(type):
            tool_name.append(dir)
            tool_dir.append('.\\' + type + '\\' + dir)
    
    print("You have the following tools: ")
    for i in range(len(tool_name)):
        print(str(i) + ": " + tool_name[i] + " in " + tool_dir[i])
    
    print(str(len(tool_name)) + ": exit")

    print("Please enter the number of the tool you want to use: ")
    tool_num = int(input())

    if tool_num == len(tool_name):
        print("Exit!")
        exit()

    print("You have selected the tool: " + tool_name[tool_num])

    if "python" in tool_dir[tool_num]:
        os.system("python " + tool_dir[tool_num] + '\\main' + ".py")
    elif "windows_bat" in tool_dir[tool_num]:
        os.system(tool_dir[tool_num] + '\\main' + ".bat")
    