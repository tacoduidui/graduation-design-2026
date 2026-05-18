# # merge_data.py：合并URL+邮件数据，划分训练/测试集
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from config import *
#
#
# # 主函数：合并数据并划分
# def merge_and_split_data():
#     # 1. 读取清洗后的URL和邮件数据
#     url_df = pd.read_csv(os.path.join(CLEAN_DATA_DIR, "clean_url.csv"), encoding="utf-8")
#     email_df = pd.read_csv(os.path.join(CLEAN_DATA_DIR, "clean_email.csv"), encoding="utf-8")
#     # 2. 合并数据
#     all_data_df = pd.concat([url_df, email_df], ignore_index=True)
#     # 3. 划分训练/测试集：按label分层抽样，保证训练/测试集标签分布一致
#     train_df, test_df = train_test_split(
#         all_data_df,
#         test_size=TEST_SIZE,
#         random_state=RANDOM_SEED,
#         stratify=all_data_df["label"]  # 分层抽样
#     )
#     # 4. 新增set字段，标记训练/测试集
#     train_df["set"] = "train"
#     test_df["set"] = "test"
#     # 5. 合并训练+测试集，重置索引
#     final_df = pd.concat([train_df, test_df], ignore_index=True)
#     final_df = final_df.reset_index(drop=True)
#
#     # 6. 保存标准化原始样本数据集
#     final_df.to_csv(os.path.join(CLEAN_DATA_DIR, CLEAN_CSV_NAME), index=False, encoding="utf-8")
#
#     # 输出统计信息
#     print(f"原始样本数据集合并完成：总样本数{len(final_df)}")
#     print(f"训练集：{len(train_df)}，测试集：{len(test_df)}")
#     print(f"URL样本：{len(final_df[final_df['type'] == 'url'])}，邮件样本：{len(final_df[final_df['type'] == 'email'])}")
#     print(f"恶意样本：{len(final_df[final_df['label'] == 1])}，良性样本：{len(final_df[final_df['label'] == 0])}")
#     # 返回测试集（仅测试集生成对抗样本）
#     return test_df
#
#
# # 主函数执行
# if __name__ == "__main__":
#     # 执行合并并获取测试集
#     test_data_df = merge_and_split_data()
#     # 保存测试集（用于后续对抗样本生成）
#     test_data_df.to_csv(os.path.join(CLEAN_DATA_DIR, "test_set.csv"), index=False, encoding="utf-8")
#     print(f"测试集已保存至：{os.path.join(CLEAN_DATA_DIR, 'test_set.csv')}")

import pandas as pd
from sklearn.model_selection import train_test_split
import config  # 导入配置文件
import os

def split_url_dataset(file_path):
    # 1. 加载数据
    # 假设文件是 CSV 格式，如果是其他格式可调整为 read_table 等
    df = pd.read_csv(file_path)

    # 2. 提取特征和标签
    # 这里假设 'test' 列是 URL 文本，'label' 是 0/1 标签
    X = df['text']
    y = df['label']

    # 3. 数据切分
    # stratify=y 确保训练集和测试集中 0 和 1 的比例与原数据一致
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=config.TEST_SIZE,
        random_state=config.RANDOM_SEED,
        stratify=y
    )

    # 4. 如果你需要保留 'type' 列，可以切分整个 DataFrame
    df_train, df_test = train_test_split(
        df,
        test_size=config.TEST_SIZE,
        random_state=config.RANDOM_SEED,
        stratify=df['label']
    )

    print(f"数据集切分完成！")
    print(f"训练集样本数: {len(df_train)} (恶意样本: {df_train['label'].sum()})")
    print(f"测试集样本数: {len(df_test)} (恶意样本: {df_test['label'].sum()})")

    return df_train, df_test

# 执行切分
# train_df, test_df = split_url_dataset('clean_url.csv')
if __name__ == "__main__":
    train_df, test_df = split_url_dataset(os.path.join(config.CLEAN_DATA_DIR, "clean_url.csv"))
    test_df.to_csv(os.path.join(config.CLEAN_DATA_DIR, "test_set.csv"), index=False, encoding="utf-8")