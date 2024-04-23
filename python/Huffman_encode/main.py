import math
import huffman as hf

# ==================== values ====================

log = open("log.md", "w+", encoding="UTF-8")

# ==================== functions ====================

def make_log(str):
    log.write(str + '\n')

# ==================== main ====================

if __name__ == "__main__":

    D = 3 # n元编码
    P_1 = [(1/12), (1/12), (1/12), (1/12), (1/12), (1/12), (1/12), (1/12), (1/12), (1/12), (1/12), (1/12)]
    
    output_P, output_P_symbol, encode_output_P, encode_output_P_len = hf.encode(P_1, D)
    
    make_log("【编码报告】")
    
    # 计算平均码长
    average_len = 0
    H_U = 0
    for p, lenght in zip(output_P, encode_output_P_len):
        average_len += p*lenght
        H_U += (- (p*math.log2(p)) )
    
    make_log("平均码长：" + str(average_len))
    make_log("编码效率：" + str(H_U / (average_len * math.log2(D)) * 100) + "%")
    
    # 判断是否唯一可译码
    flag = 0
    for i in range(len(encode_output_P)):
        for j in range(i+1, len(encode_output_P)):
            if encode_output_P[j][0:len(encode_output_P[i])] == encode_output_P[i]:
                make_log("非唯一可译码")
                flag = 1
                break
    
    if 0 == flag:
        make_log("唯一可译码")
    
    # 计算编码的方差
    sigma_I = 0
    for p in output_P:
        sigma_I += p*(((-math.log2(p)) - H_U) ** 2 )
    
    make_log("方差：" + str(sigma_I))
    
    # 输出
    output_P = [round(r, 3) for r in output_P]
    
    for p, symbol, encode_r, encode_r_len in zip(output_P, [("$P_{" + symbol + "}$") for symbol in output_P_symbol], encode_output_P, encode_output_P_len):
        make_log("概率：" + str(p) + " 对应码元：" + str(symbol) + " 对应霍夫曼编码：" + str(encode_r) + " 对应码长：" + str(encode_r_len))
    
    