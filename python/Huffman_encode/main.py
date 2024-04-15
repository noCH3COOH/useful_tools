import math

# ==================== values ====================

log = open("log.md", "w+", encoding="UTF-8")

D = 2 # n元编码
P_1 = [(1/12), (1/12), (1/12), (1/12), (1/12), (1/12), (1/12), (1/12), (1/12), (1/12), (1/12), (1/12)]

P_1_symbol = []
result = []    # 每个码元的概率
result_runtime = []
result_symbol = []    # 记录各个码元由什么组成
result_symbol_runtime = []
encode_result = []    # 编码结果
encode_result_len = []    # 编码结果长度

min_runtime = []
min_symbol_runtime = []

# ==================== functions ====================

def sort_in_P(P, P_symbol):
    for i in range(len(P)):
        for j in range(i+1, len(P)):
            if P[i] < P[j]:
                P[i], P[j] = P[j], P[i]
                P_symbol[i], P_symbol[j] = P_symbol[j], P_symbol[i]
            elif P[i] == P[j]:
                if len(P_symbol[i]) < len(P_symbol[j]):
                    P_symbol[i], P_symbol[j] = P_symbol[j], P_symbol[i]

    P = [round(i, 3) for i in P]
    return P, P_symbol

def make_log(str):
    log.write(str + '\n')

def min_process(min_symbol_runtime, add_char):
    once_flag = 0

    while ("+" in min_symbol_runtime) or (0 == once_flag):
        right = min_symbol_runtime.split("+")[-1]
        encode_result[result_symbol.index(right)] = add_char + encode_result[result_symbol.index(right)]
        encode_result_len[result_symbol.index(right)] += 1
        min_symbol_runtime = min_symbol_runtime[0:-len(right)-1]

        if ("+" not in min_symbol_runtime) and ("" != min_symbol_runtime):
            right = min_symbol_runtime
            encode_result[result_symbol.index(right)] = add_char + encode_result[result_symbol.index(right)]
            encode_result_len[result_symbol.index(right)] += 1
            min_symbol_runtime = min_symbol_runtime[0:-len(right)-1]

        once_flag = 1

# ==================== main ====================

for p1,i in zip(P_1, range(len(P_1))):
    result.append(p1)
    P_1_symbol.append(str(i+1))
    result_symbol.append(str(i+1))
    encode_result.append("")
    encode_result_len.append(0)

# 霍夫曼编码求最佳二元码
result_runtime = result.copy()
result_symbol_runtime = result_symbol.copy()

## 从大到小排序
while len(result_symbol_runtime) > 1:

    ## 从大到小排序
    result_runtime, result_symbol_runtime = sort_in_P(result_runtime, result_symbol_runtime)
    make_log(str("概率：" + str(result_runtime) + "\n对应码元：" + str([ ("$P_{"+symbol+"}$") for symbol in result_symbol_runtime]).replace("+","")))

    ## 清空处理区域
    min_runtime = []
    min_symbol_runtime = []

    ## 取出最小的D数
    end_flag = 0
    for d in range(D):
        if 0 == len(result_runtime):
            end_flag = 1
            break
        min_runtime.append(result_runtime.pop())
        min_symbol_runtime.append(result_symbol_runtime.pop())

    ## 对对应的编码进行修改
    for d, min_s_r in zip(range(D), min_symbol_runtime):
        min_process(min_s_r, str(d))

    ## 生成新的数
    new = sum(min_runtime)
    new_symbol = ""
    for min_symbol in min_symbol_runtime:
        new_symbol += str(min_symbol + "+")
    new_symbol = new_symbol[0:-1]    # 去掉最后一个+

    ## 添加到列表中
    result_runtime.append(new)
    result_symbol_runtime.append(new_symbol)

    if 1 == end_flag:
        break

make_log("")

# 计算平均码长
average_len = 0
H_U = 0
for p, lenght in zip(result, encode_result_len):
    average_len += p*lenght
    H_U += (- (p*math.log2(p)) )

make_log("平均码长：" + str(average_len))
make_log("编码效率：" + str(H_U / (average_len * math.log2(D)) * 100) + "%")

# 判断是否唯一可译码
flag = 0
for i in range(len(encode_result)):
    for j in range(i+1, len(encode_result)):
        if encode_result[j][0:len(encode_result[i])] == encode_result[i]:
            make_log("非唯一可译码")
            flag = 1
            break

if 0 == flag:
    make_log("唯一可译码")

# 计算编码的方差
sigma_I = 0
for p in result:
    sigma_I += p*(((-math.log2(p)) - H_U) ** 2 )

make_log("方差：" + str(sigma_I))

# 输出
result = [round(r, 3) for r in result]

for p, symbol, encode_r, encode_r_len in zip(result, [("$P_{" + symbol + "}$") for symbol in result_symbol], encode_result, encode_result_len):
    make_log("概率：" + str(p) + " 对应码元：" + str(symbol) + " 对应霍夫曼编码：" + str(encode_r) + " 对应码长：" + str(encode_r_len))

