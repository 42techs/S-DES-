import itertools
from sdes import encrypt, string_to_bits

def generate_keys():
    # 生成所有可能的 10 位二进制密钥
    for i in range(1024):  # 0 到 1023，共 1024 个可能的密钥
        yield [int(bit) for bit in f'{i:010b}']  # 转换为 10 位二进制列表

def closed_test(plaintext):
    ciphertexts = {}  # 用于记录密文及其对应的密钥

    for key in generate_keys():
        # 使用当前密钥加密明文
        bits_plaintext = string_to_bits(plaintext)[0]  # 转换明文为位
        ciphertext = encrypt(bits_plaintext, key)  # 进行加密

        # 将密文转换为字符串格式以便于比较
        cipher_str = ''.join(map(str, ciphertext))
        
        # 如果该密文已经存在列表中，打印原明文和不同密钥
        if cipher_str in ciphertexts:
            print(f"相同密文: {cipher_str}")
            print(f"明文: {plaintext} 使用密钥: {ciphertexts[cipher_str]} 生成相同密文")
            print(f"新的密钥: {key}")
        else:
            ciphertexts[cipher_str] = key  # 将密文和密钥存进字典

if __name__ == "__main__":
    # 测试的明文
    test_plaintext = "BYEBYE"  # 替换为您想要测试的明文
    closed_test(test_plaintext)
