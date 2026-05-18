import pandas as pd
import random
import re
import os
import config


def parse_url_parts(url):
    """解析URL的不同部分，避免修改协议和端口等关键部分"""
    try:
        # 匹配协议、域名、端口、路径、查询参数
        pattern = r'^(https?://)([^:/?#]+)(?::(\d+))?([^?#]*)(?:\?([^#]*))?'
        match = re.match(pattern, url)

        if not match:
            return None

        return {
            'protocol': match.group(1),  # http:// 或 https://
            'domain': match.group(2),  # 域名
            'port': match.group(3),  # 端口
            'path': match.group(4) or '/',  # 路径
            'query': match.group(5) or ''  # 查询参数
        }
    except:
        return None


def parse_ip_url(url):
    """解析IP URL的各个部分"""
    pattern = r'^(https?://)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?::(\d+))?([^?#]*)?(?:\?([^#]*))?'
    match = re.match(pattern, url)

    if not match:
        return None

    return {
        'protocol': match.group(1),  # http:// 或 https://
        'ip': match.group(2),  # IP地址
        'port': match.group(3),  # 端口
        'path': match.group(4) or '/',  # 路径
        'query': match.group(5) or ''  # 查询参数
    }


def is_ip_url(url):
    """判断是否为IP地址URL"""
    # 匹配IPv4地址
    ip_pattern = r'https?://(\d{1,3}\.){3}\d{1,3}(?::\d+)?(/[^?#]*)?'
    return bool(re.match(ip_pattern, url))


def is_valid_ip_url(url):
    """验证IP URL是否格式正确"""
    try:
        parsed = parse_ip_url(url)
        if not parsed:
            return False

        # 检查IP地址有效性
        ip_parts = parsed['ip'].split('.')
        if len(ip_parts) != 4:
            return False

        for part in ip_parts:
            num = int(part)
            if num < 0 or num > 255:
                return False

        # 检查端口
        if parsed['port']:
            port = int(parsed['port'])
            if port < 1 or port > 65535:
                return False

        return True
    except:
        return False


def replace_chars(text, char_map, prob):
    """按概率替换字符"""
    if not text:
        return text

    result = []
    for char in text:
        if char in char_map and random.random() < prob:
            result.append(char_map[char])
        else:
            result.append(char)
    return ''.join(result)


def replace_with_homoglyphs(text, homoglyph_map, prob):
    """用同形异义字替换字符"""
    if not text:
        return text

    result = []
    for char in text.lower():  # 只处理小写
        if char in homoglyph_map and random.random() < prob:
            result.append(random.choice(homoglyph_map[char]))
        else:
            result.append(char)
    return ''.join(result)


def randomize_case(text, prob):
    """随机化大小写"""
    if not text:
        return text

    result = []
    for char in text:
        if char.isalpha() and random.random() < prob:
            result.append(char.upper() if char.islower() else char.lower())
        else:
            result.append(char)
    return ''.join(result)


def generate_ip_perturbation(ip_url):
    """为IP地址URL生成对抗样本"""
    parsed = parse_ip_url(ip_url)
    if not parsed:
        return ip_url

    # 多种IP地址扰动策略
    strategies = [
        'port_manipulation',  # 端口操作
        'path_noise',  # 路径噪声
        'case_obfuscation',  # 大小写混淆
        'encoding_trick',  # 编码技巧
    ]

    # 优先使用端口和路径扰动，避免修改IP本身
    strategy = random.choice(strategies)

    if strategy == 'port_manipulation':
        # 策略1: 端口号操作
        if parsed['port']:
            # 修改现有端口
            port_num = int(parsed['port'])
            if port_num < 10:
                new_port = str(port_num + 1)
            elif port_num > 65530:
                new_port = str(port_num - 1)
            else:
                # 在常见端口附近随机选择
                common_ports = [80, 443, 8080, 8443, 3000, 5000, 8000]
                closest = min(common_ports, key=lambda x: abs(x - port_num))
                new_port = str(closest) if random.random() < 0.7 else str(port_num + random.choice([-1, 1]))
        else:
            # 添加随机端口
            common_ports = ['80', '8080', '3000', '5000', '8000']
            new_port = random.choice(common_ports)

        new_url = parsed['protocol'] + parsed['ip'] + ':' + new_port + parsed['path']
        if parsed['query']:
            new_url += '?' + parsed['query']
        return new_url

    elif strategy == 'path_noise':
        # 策略2: 添加路径噪声
        path = parsed['path']

        # 添加随机路径参数
        noise_params = [
            '?v=1',
            '?t=' + str(random.randint(1000, 9999)),
            '?r=' + str(random.randint(100, 999)),
            '?ref=test',
            '?source=ad'
        ]

        if not parsed['query']:
            # 如果没有查询参数，添加一个
            noise = random.choice(noise_params)
        else:
            # 如果有查询参数，追加一个
            noise = '&' + noise_params[0].lstrip('?')

        new_url = parsed['protocol'] + parsed['ip']
        if parsed['port']:
            new_url += ':' + parsed['port']
        new_url += path + noise
        if parsed['query'] and '?' not in noise:
            new_url += '?' + parsed['query']
        return new_url

    elif strategy == 'case_obfuscation':
        # 策略3: 在路径中使用大小写混淆
        path = parsed['path']

        if len(path) > 1:
            # 将路径中的某些字符随机大小写
            chars = list(path)
            indices = random.sample(range(len(chars)), min(3, len(chars) // 2))
            for i in indices:
                if chars[i].isalpha():
                    chars[i] = chars[i].upper() if chars[i].islower() else chars[i].lower()
            new_path = ''.join(chars)
        else:
            new_path = path

        new_url = parsed['protocol'] + parsed['ip']
        if parsed['port']:
            new_url += ':' + parsed['port']
        new_url += new_path
        if parsed['query']:
            new_url += '?' + parsed['query']
        return new_url

    elif strategy == 'encoding_trick':
        # 策略4: URL编码技巧
        path = parsed['path']

        if len(path) > 1:
            # 对路径中的某些字符进行URL编码
            chars_to_encode = ['/', '.', '-', '_']
            for char in chars_to_encode:
                if char in path and random.random() < 0.3:
                    # 部分编码
                    encoded_char = f"%{ord(char):02X}"
                    path = path.replace(char, encoded_char, 1)

        new_url = parsed['protocol'] + parsed['ip']
        if parsed['port']:
            new_url += ':' + parsed['port']
        new_url += path
        if parsed['query']:
            new_url += '?' + parsed['query']
        return new_url

    return ip_url


def original_url_perturbation(url):
    """对域名型URL进行扰动"""
    # 保存原始URL
    original_url = url

    # 尝试多种扰动策略
    strategies = ['character_replace', 'homoglyph', 'case_switch']
    strategy = random.choice(strategies)

    try:
        if strategy == 'character_replace':
            # 方案1: 视觉相似字符替换
            homoglyphs = {
                '0': 'o',
                '1': 'l',
                'l': '1',
                'i': '1',
                'o': '0',
                'm': 'rn',
                'rn': 'm',
                'w': 'vv',
                'vv': 'w',
                '.': ',',
                ',': '.',
                '-': '_',
                '_': '-'
            }

            # 只替换路径和查询参数部分，不替换协议、域名、端口
            parsed = parse_url_parts(url)
            if parsed:
                # 对路径和查询参数进行扰动
                perturbed_path = replace_chars(parsed['path'], homoglyphs, 0.1)
                perturbed_query = replace_chars(parsed['query'], homoglyphs, 0.1)

                # 重建URL
                new_url = parsed['protocol'] + '://' + parsed['domain']
                if parsed['port']:
                    new_url += ':' + parsed['port']
                new_url += perturbed_path
                if perturbed_query:
                    new_url += '?' + perturbed_query
                return new_url

        elif strategy == 'homoglyph':
            # 方案2: 同形异义字替换（更具欺骗性）
            unicode_homoglyphs = {
                'a': ['а', 'ɑ'],  # Cyrillic 'a'
                'c': ['с'],  # Cyrillic 'c'
                'e': ['е'],  # Cyrillic 'e'
                'o': ['о'],  # Cyrillic 'o'
                'p': ['р'],  # Cyrillic 'p'
                'x': ['х'],  # Cyrillic 'x'
                'y': ['у'],  # Cyrillic 'y'
                's': ['ѕ'],  # Cyrillic Dze
            }

            # 只替换域名中的字母，不替换协议和数字
            parsed = parse_url_parts(url)
            if parsed:
                # 对域名进行同形字替换
                perturbed_domain = replace_with_homoglyphs(parsed['domain'], unicode_homoglyphs, 0.15)

                new_url = parsed['protocol'] + '://' + perturbed_domain
                if parsed['port']:
                    new_url += ':' + parsed['port']
                new_url += parsed['path']
                if parsed['query']:
                    new_url += '?' + parsed['query']
                return new_url

        elif strategy == 'case_switch':
            # 方案3: 大小写混淆（主要用于路径和参数）
            parsed = parse_url_parts(url)
            if parsed:
                # 对路径进行大小写随机化
                perturbed_path = randomize_case(parsed['path'], 0.3)

                new_url = parsed['protocol'] + '://' + parsed['domain'].lower()  # 域名通常小写
                if parsed['port']:
                    new_url += ':' + parsed['port']
                new_url += perturbed_path
                if parsed['query']:
                    new_url += '?' + parsed['query']
                return new_url
    except Exception as e:
        print(f"扰动URL时出错: {e}, URL: {url[:50]}...")

    # 如果所有策略都失败，返回原始URL
    return original_url


def generate_adversarial_test_set(input_path, output_path):
    # 1. 加载测试集
    df = pd.read_csv(input_path)

    # 2. 筛选出恶意 URL (label == 1)
    malicious_df = df[df['label'] == 1].copy()
    benign_df = df[df['label'] == 0].copy()

    print(f"正在为 {len(malicious_df)} 个恶意 URL 生成对抗样本...")

    def smart_perturb_url(url):
        """
        智能URL扰动，根据URL类型使用不同策略
        """
        if is_ip_url(url):
            return generate_ip_perturbation(url)
        else:
            # 使用原有的域名URL扰动策略
            return original_url_perturbation(url)

    # 4. 执行对抗样本生成
    ip_url_count = 0
    perturbed_urls = []

    for idx, url in enumerate(malicious_df['text']):
        if is_ip_url(url):
            ip_url_count += 1
            perturbed = generate_ip_perturbation(url)

            # 验证生成的IP URL是否有效
            if not is_valid_ip_url(perturbed):
                # 如果无效，使用回退策略
                parsed = parse_ip_url(url)
                if parsed and len(parsed['path']) > 1:
                    # 简单地在路径后添加噪声
                    noise = ['?test=1', '?r=' + str(random.randint(100, 999))]
                    perturbed = url + random.choice(noise)
                else:
                    perturbed = url

            perturbed_urls.append(perturbed)
        else:
            # 非IP URL使用域名扰动逻辑
            perturbed_urls.append(original_url_perturbation(url))

    malicious_df['text'] = perturbed_urls

    print(f"发现 {ip_url_count} 个IP地址URL")
    print(f"生成 {len(malicious_df)} 个对抗样本")

    # 5. 标记和保存
    malicious_df['url_type'] = malicious_df['text'].apply(
        lambda x: 'ip' if is_ip_url(x) else 'domain'
    )
    benign_df['url_type'] = benign_df['text'].apply(
        lambda x: 'ip' if is_ip_url(x) else 'domain'
    )

    malicious_df['perturbation_type'] = 'adversarial'
    benign_df['perturbation_type'] = 'original'

    # 6. 合并
    adv_test_df = pd.concat([malicious_df, benign_df], ignore_index=True)

    # 7. 保存
    adv_test_df.to_csv(output_path, index=False)
    print(f"对抗测试集已保存至: {output_path}")

    # 8. 打印IP URL的对抗样本示例
    ip_examples = malicious_df[malicious_df['url_type'] == 'ip'].head(3)
    if not ip_examples.empty:
        print("\nIP地址URL对抗样本示例:")
        for i, row in ip_examples.iterrows():
            # 找到对应的原始URL
            original_idx = df[df['label'] == 1].index[list(malicious_df['text']).index(row['text'])]
            original = df.loc[original_idx, 'text']
            print(f"原URL: {original[:60]}...")
            print(f"新URL: {row['text'][:60]}...")
            print(f"扰动类型: IP地址扰动")
            print()


if __name__ == "__main__":
    test_set_path = os.path.join(config.CLEAN_DATA_DIR, "test_set.csv")
    output_adv_path = os.path.join(config.CLEAN_DATA_DIR, "adv_test_set.csv")

    if os.path.exists(test_set_path):
        generate_adversarial_test_set(test_set_path, output_adv_path)
    else:
        print("未找到 test_set.csv，请先运行切分脚本。")