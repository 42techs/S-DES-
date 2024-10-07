# S-DES算法实现

## 项目介绍
本项目是根据"信息安全导论"课程第5次课讲述的S-DES算法，使用Python语言来编程实现加、解密程序、提供GUI界面进行交互、实现暴力破解、封闭测试等功能。

## S-DEC算法介绍
S-DES（Simplified DES）是一种对称加密算法，由IBM于1999年提出，是DES的简化版本。S-DES算法的基本思路是将DES算法的分组操作和密钥调度操作合并为一步操作，从而减少了密钥调度操作的次数，提高了加密速度。S-DES算法的密钥长度为64位，分组长度为64位，密钥分为两个部分，即数据密钥和轮密钥。

## 编程和测试要求

### 第1关：基本测试
根据S-DES算法编写和调试程序，提供GUI解密支持用户交互。输入可以是8位的数据和10位的密钥，输出是8位的密文。

### 第2关：交叉测试
考虑到算法标准，所有人在编写程序时需使用相同算法流程和转换单元（P-Box、S-Box等），以保证算法和程序在异构系统或平台上均可正常运行。设有A和B两组同学（选择相同的密钥K），则A、B组同学编写的程序对明文P进行加密应得到相同的密文C；或者B组同学接收到A组程序加密的密文C，使用B组程序解密后可得到与A相同的P。

### 第3关：扩展功能
为了实用性扩展，加密算法的数据输入可为ASCII编码字符串（分组为1 Byte），对应地输出也可以为ASCII字符串（可能出现乱码）。

### 第4关：暴力破解
假设找到了使用相同密钥的明、密文对（一个或多个），请尝试使用暴力破解的方法找到正确的密钥Key。在编写程序时，可考虑使用多线程方式提升破解效率。请设定时间戳，并用视频或动图展示在多长时间内完成了暴力破解。

### 第5关：封闭测试
根据第4关的结果，进一步分析对于随机选择的一个明密文对，是否存在不止一个密钥Key。进一步扩展，对任意给定的明文分组Pₙ，是否会出现选择不同的密钥Kᵢ≠Kⱼ加密得到相同密文Cₙ的情况？

## 实验结果

### 第1关 基础测试
测试明文 `10110010`，密钥 `1110001010` 进行加密解密，使用解密结果查看加密解密流程是否有误。

#### 加密结果
![加密结果](https://github.com/user-attachments/assets/d3599568-667a-417c-a845-560814fbcf01)

#### 解密结果
![解密结果](https://github.com/user-attachments/assets/1d2d209c-b94c-47bc-80fc-f54422b43cd6)

### 第2关 交叉测试
#### 其他小组加密结果
![8c5bc179587a2c7b7ffdf743bae810f5](https://github.com/user-attachments/assets/cb9274b8-1f50-4a71-a910-97f7df4451cc)

#### 本小组加密结果
![200473927ed51a6ad51251094eaeca1a](https://github.com/user-attachments/assets/16d4b33e-b1ac-4276-a874-84512032f6c6)


### 第3关 对ASCII字符串进行加密解密
#### 加密结果
![ASCII字符串加密结果](https://github.com/user-attachments/assets/0bab547d-e63c-4961-ba6f-96cc87671f75)

#### 解密结果
![ASCII字符串解密结果](https://github.com/user-attachments/assets/a36b11a3-6dc3-4843-9fae-663297771436)



### 第4关：暴力破解
假设你找到了使用相同密钥的明、密文对(一个或多个)，请尝试使用暴力破解的方法找到正确的密钥Key。
（1）代码实现

    import itertools
    import time
    from threading import Thread
    from sdes import decrypt, string_to_bits, bits_to_string

    known_plaintext = "HELLO"  # 替换为实际的明文
    known_ciphertext = "Ï"  # 替换为实际的密文

    plaintext_bits = string_to_bits(known_plaintext)[0]  # 获取明文的位
    ciphertext_bits = string_to_bits(known_ciphertext)[0]  # 替换为相应的密文位

    def try_key(key):
        # 使用给定的密钥解密密文
        decrypted_bits = decrypt(ciphertext_bits, key)
    
        # 验证解密出的明文是否与已知明文相同
        if decrypted_bits == plaintext_bits:
            print(f"找到密钥：{''.join(map(str, key))}")
            return True
        return False

    def brute_force_decrypt(start, end):
        for i in range(start, end):
            key = [int(bit) for bit in f'{i:010b}']  # 生成 10 位二进制密钥
            if try_key(key):
                break

    if __name__ == "__main__":
        start_time = time.time()  # 记录开始时间
    
        # 设置线程数
        num_threads = 4
        threads = []
        keys_per_thread = 1024 // num_threads  # 每个线程处理的密钥范围

        for t in range(num_threads):
            start = t * keys_per_thread
            end = (t + 1) * keys_per_thread
            thread = Thread(target=brute_force_decrypt, args=(start, end))
            threads.append(thread)
            thread.start()

        # 等待所有线程完成
        for thread in threads:
            thread.join()

        end_time = time.time()  # 记录结束时间
        print(f"暴力破解完成，耗时: {end_time - start_time:.2f} 秒")
    
    
（2）运行结果
![e01f81b5e980a0324228587284986488](https://github.com/user-attachments/assets/554cc85e-7746-4b03-8011-41f3e121e2b4)


### 第5关：封闭测试
（1）代码实现

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
        test_plaintext = "HELLO"  # 替换为您想要测试的明文
        closed_test(test_plaintext)
    
（2）运行结果
![e634d1fdbcc3f97ecdf9e33784ef07a4](https://github.com/user-attachments/assets/d5795c7f-0065-40bb-8eb6-9e6cc6b7c3e9)


## 总结
本次实验主要是对S-DES算法的实现和测试，包括基本测试、交叉测试、ASCII字符串加密解密、暴力破解、封闭测试等。完成了实验的基本要求

## 开发团队
- 小组：智慧组
- 成员：杨大浩、齐浩男
- 单位：重庆大学大数据与软件学院
