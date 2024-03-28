import tkinter as tk
import tkinter.filedialog as fd
import os

# Conversion table from decimal to hex
HEX = "0123456789ABCDEF"

def transform(num):
    hex_number = ''
    while num != 0:
        hex_number = HEX[num % 16] + hex_number
        num = num // 16
    return hex_number.zfill(8)

def get_file_name(filename):
    return filename[filename.rfind(os.sep) + 1:]

def generate_aLine(out_file, num, str_num, str_ascii, file_size):
    out_file.write(transform(num - 16) + ":   ")
    out_file.write(str_num)
    out_file.write("   " + str_ascii)
    out_file.write("\n")

    now = num / file_size * 100
    now_str = f"\r{now:.3f}%"
    print(now_str, end="\n" if now == 100 else "")

if __name__ == "__main__":
    num = 0  # The Byte have been read
    path_r = ""
    path_w = ""

    try:
        path_r = fd.askopenfile(mode='rb', title='选择文件').name
        print('源文件：' + path_r)
    except Exception as e:
        tk.messagebox.showerror('Could not open file', 'Could not open file: {}'.format(str(e)), parent=self.main)
        exit()

    path_w = fd.askdirectory(title='选择输出路径') + '/Hex_' + get_file_name(path_r).split('/')[-1] + '.txt'
    print('输出文件：' + path_w)
    if not path_w:
        print('未选择路径，退出')
        exit()

    with open(path_r, "rb") as in_file, open(path_w, "w+") as out_file:
        # Get the file size
        in_file.seek(0, os.SEEK_END)
        file_size = in_file.tell()
        in_file.seek(0, os.SEEK_SET)
        out_file.write(f"src file: {get_file_name(path_r)}\nFile Size: {file_size / 1024:.3f} KB\n\n")

        # Print the first row's index
        out_file.write("address     ")
        for i in range(16):
            out_file.write(HEX[i] + "  ")
        out_file.write("   ASCII\n")

        # Read and Write File
        str_num = ""
        str_ascii = ""

        while True:
            byte = in_file.read(1)
            if not byte:
                if "" != str_num:
                    generate_aLine(out_file, num, str_num, str_ascii, file_size)
                break
            
            num += 1
            str_num = str_num + HEX[byte[0] // 16] + HEX[byte[0] % 16] + " "
            if 32 <= byte[0] <= 126:
                str_ascii = str_ascii + chr(byte[0])
            else:
                str_ascii = str_ascii + "."

            if num % 16 == 0:
                generate_aLine(out_file, num, str_num, str_ascii, file_size)
                str_num = ""
                str_ascii = ""
                

    print("Success")
    in_file.close()
    out_file.close()
