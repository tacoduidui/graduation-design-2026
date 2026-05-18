# clean_email.py：钓鱼邮件数据集清洗与标准化（适配 Kaggle Enron 原始数据集）
import pandas as pd
import re
import os
import email
from email import policy
from config import *

# 定义邮件文本清洗函数：去除多余符号、换行
def clean_email_text(text):
    text = str(text).strip()
    # 去除多余换行、制表符
    text = re.sub(r'[\n\t\r]', ' ', text)
    # 去除连续多个空格，保留单个
    text = re.sub(r'\s+', ' ', text)
    # 去除特殊符号（可根据需求调整，保留基本标点）
    text = re.sub(r'[^\w\s,.!?@-]', '', text)
    return text

# 解析 Enron 原始 message 字段，提取正文
def parse_enron_message(raw_msg):
    try:
        msg = email.message_from_string(raw_msg, policy=policy.default)
        body = ""
        # 解析多部件邮件
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode("utf-8", "ignore")
                    break
        else:
            body = msg.get_payload(decode=True).decode("utf-8", "ignore")
        return body.strip()
    except:
        return ""

# 给 Enron 邮件打钓鱼/正常标签（伪标签）
def label_phishing_email(text):
    # 钓鱼关键词（可自行扩展）
    phishing_keywords = [
        "verify", "account", "login", "password", "bank", "credit",
        "free", "win", "click", "link", "urgent", "update", "confirm",
        "security", "personal", "information", "paypal", "ebay"
    ]
    text = str(text).lower()
    return 1 if any(kw in text for kw in phishing_keywords) else 0

# 定义邮件数据集清洗主函数（专门处理 Enron：file + message 列）
def clean_email_data(raw_email_path):
    # 1. 读取 Enron 原始数据集（只有 file, message 列）
    encodings = ["utf-8", "gbk", "gb2312"]
    email_df = None
    for enc in encodings:
        try:
            email_df = pd.read_csv(raw_email_path, encoding=enc)
            break
        except:
            continue
    if email_df is None:
        raise Exception("钓鱼邮件数据集编码错误，无法读取")

    # 2. 必须包含 message 列（Enron 数据集特征）
    if "message" not in email_df.columns:
        raise Exception("Enron 数据集必须包含 message 列！")

    # 3. 解析 message → 提取邮件正文 email
    print("正在解析 Enron 原始邮件正文...")
    email_df["email"] = email_df["message"].apply(parse_enron_message)

    # 4. 自动打标签（0=正常，1=钓鱼）→ 生成 label 列
    print("正在为邮件自动打钓鱼/正常标签...")
    email_df["label"] = email_df["email"].apply(label_phishing_email)

    # 5. 保留核心字段：email + label
    email_df = email_df[["email", "label"]].copy()

    # 6. 重命名为 text，新增 type=email（完全对齐你的代码）
    email_df = email_df.rename(columns={"email": "text"})
    email_df["type"] = "email"

    # 7. 过滤标签：仅保留0/1
    email_df = email_df[email_df["label"].isin([0, 1])]

    # 8. 清洗邮件正文
    email_df["text"] = email_df["text"].apply(clean_email_text)

    # 9. 去重
    email_df = email_df.drop_duplicates(subset=["text"], keep="first")

    # 10. 删除空值、过滤短文本（长度≥50）
    email_df = email_df.dropna(subset=["text"])
    email_df = email_df[email_df["text"].apply(lambda x: len(x) >= 50)]

    # 11. 数据平衡：下采样，保证0/1样本均衡
    min_count = email_df["label"].value_counts().min()
    email_df_balanced = pd.concat([
        email_df[email_df["label"] == 0].sample(n=min_count, random_state=RANDOM_SEED),
        email_df[email_df["label"] == 1].sample(n=min_count, random_state=RANDOM_SEED)
    ], ignore_index=True)

    # 12. 重置索引
    email_df_balanced = email_df_balanced.reset_index(drop=True)

    print(
        f"邮件数据集清洗完成：总样本数{len(email_df_balanced)}，钓鱼样本{len(email_df_balanced[email_df_balanced['label'] == 1])}，正常样本{len(email_df_balanced[email_df_balanced['label'] == 0])}")
    return email_df_balanced

# 主函数：执行邮件清洗并保存
if __name__ == "__main__":
    # 原始 Enron 数据集路径（修改为你自己的路径）
    RAW_EMAIL_PATH = "E:/毕业项目/dataset/raw/enron_email.csv"

    # 执行清洗
    clean_email_df = clean_email_data(RAW_EMAIL_PATH)

    # 保存清洗后的数据
    save_path = os.path.join(CLEAN_DATA_DIR, "clean_email.csv")
    clean_email_df.to_csv(save_path, index=False, encoding="utf-8")
    print(f"清洗后的邮件数据已保存至：{save_path}")