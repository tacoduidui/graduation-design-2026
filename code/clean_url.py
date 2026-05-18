# clean_url.py：恶意URL数据集清洗与标准化
import pandas as pd
import numpy as np
from config import *


# 定义URL清洗函数
def clean_url_data(raw_url_path, benign_url_path):
    # 1. 读取恶意URL数据集
    # 尝试多种编码，避免乱码
    encodings = ["utf-8", "gbk", "gb2312"]
    url_df = None
    for enc in encodings:
        try:
            url_df = pd.read_csv(raw_url_path, encoding=enc)
            break
        except:
            continue
    if url_df is None:
        raise Exception("恶意URL数据集编码错误，无法读取")

    # 2. 提取核心字段，标注恶意标签
    # 确保url列存在，重命名为text，新增label=1，type=url
    if "url" not in url_df.columns:
        raise Exception("URL数据集缺少url列")
    mal_url_df = url_df[["url"]].rename(columns={"url": "text"})
    mal_url_df["label"] = 1  # 恶意=1
    mal_url_df["type"] = "url"  # 数据类型=url

    # 3. 读取良性URL数据集，标注良性标签
    benign_url_df = pd.read_csv(benign_url_path, encoding="utf-8")
    benign_url_df = benign_url_df[["url"]].rename(columns={"url": "text"})
    benign_url_df["label"] = 0  # 良性=0
    benign_url_df["type"] = "url"

    # 4. 合并恶意+良性URL，开始清洗
    all_url_df = pd.concat([mal_url_df, benign_url_df], ignore_index=True)
    # 4.1 去重
    all_url_df = all_url_df.drop_duplicates(subset=["text"], keep="first")
    # 4.2 删除空值
    all_url_df = all_url_df.dropna(subset=["text"])
    # 4.3 过滤无效URL：长度≥5、http/https开头
    all_url_df = all_url_df[
        all_url_df["text"].apply(lambda x: len(str(x)) >= 5 and str(x).startswith(("http://", "https://")))]
    # 4.4 格式统一：小写、去首尾空格
    all_url_df["text"] = all_url_df["text"].apply(lambda x: str(x).lower().strip())
    # 4.5 重置索引
    all_url_df = all_url_df.reset_index(drop=True)

    print(
        f"URL数据集清洗完成：总样本数{len(all_url_df)}，恶意样本{len(all_url_df[all_url_df['label'] == 1])}，良性样本{len(all_url_df[all_url_df['label'] == 0])}")
    return all_url_df


# 主函数：执行URL清洗并保存
if __name__ == "__main__":
    # 原始恶意URL路径（URLhaus）
    # RAW_URL_PATH = os.path.join(RAW_DATA_DIR, "urlhaus.csv")
    # print(RAW_URL_PATH)
    # 执行清洗
    clean_url_df = clean_url_data(RAW_URL_PATH, BENIGN_URL_CSV)
    # 保存清洗后的URL数据（临时文件，后续与邮件数据合并）
    clean_url_df.to_csv(os.path.join(CLEAN_DATA_DIR, "clean_url.csv"), index=False, encoding="utf-8")
    print(f"清洗后的URL数据已保存至：{os.path.join(CLEAN_DATA_DIR, 'clean_url.csv')}")