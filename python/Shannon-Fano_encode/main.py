# 概率和码元
probabilities = [0.2, 0.15, 0.15, 0.1, 0.1, 0.1, 0.1, 0.1]
symbols = ['$P_{1}$', '$P_{2}$', '$P_{3}$', '$P_{4}$', '$P_{5}$', '$P_{6}$', '$P_{7}$', '$P_{8}$']

# 对符号进行排序
sorted_symbols = sorted(zip(probabilities, symbols), key=lambda x: x[0], reverse=True)

# Shannon-Fano编码函数
def shannon_fano_encode(sorted_symbols):
    if len(sorted_symbols) <= 1:
        return {sorted_symbols[0][1]: '0'} if sorted_symbols else {}
    
    # 找到中点，尽可能均匀地分割符号
    mid = sum(p[0] for p in sorted_symbols) / 2
    lower_sum = 0
    for i, (p, s) in enumerate(sorted_symbols):
        lower_sum += p
        if lower_sum >= mid:
            break
    
    # 分割为两个子集，并递归编码
    left_set = shannon_fano_encode(sorted_symbols[:i+1])
    right_set = shannon_fano_encode(sorted_symbols[i+1:])
    
    # 将左边的编码添加'0'，右边的编码添加'1'
    for s in left_set:
        left_set[s] = '0' + left_set[s]
    for s in right_set:
        right_set[s] = '1' + right_set[s]
    
    return dict(list(left_set.items()) + list(right_set.items()))

# 进行编码
encode_table = shannon_fano_encode(sorted_symbols)
print(encode_table)
