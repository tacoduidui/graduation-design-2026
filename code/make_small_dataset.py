# import pandas as pd
#
# # 🔥 修复 Windows 路径（必须用 r"" 或者双斜杠）
# INPUT_PATHS = [
#     r"E:\毕业项目\dataset\prompts\prompt_plain.csv",
#     r"E:\毕业项目\dataset\prompts\prompt_normal.csv",
#     r"E:\毕业项目\dataset\prompts\prompt_graph.csv"
# ]
#
# # 随机抽取数量
# SAMPLE_SIZE = 1000
#
# # # 处理正常数据集
# # for path in INPUT_PATHS:
# #     df = pd.read_csv(path, encoding="utf-8")
# #     # ✅ 真·随机抽样，不是取前100条
# #     df_small = df.sample(n=min(SAMPLE_SIZE, len(df)), random_state=42)  # random_state保证可复现
# #     out_path = path.replace(".csv", "_small.csv")
# #     df_small.to_csv(out_path, index=False, encoding="utf-8")
# #     print(f"✅ 已生成随机小数据集：{out_path}，共 {len(df_small)} 条")
#
#
# # 处理对抗样本集
# INPUT_PATHS_ADV = [
#     r"E:\毕业项目\dataset\prompts\prompt_plain_adv.csv",
#     r"E:\毕业项目\dataset\prompts\prompt_normal_adv.csv",
#     r"E:\毕业项目\dataset\prompts\prompt_graph_adv.csv"
# ]
#
# for path in INPUT_PATHS_ADV:
#     df = pd.read_csv(path, encoding="utf-8")
#     df_small = df.sample(n=min(SAMPLE_SIZE, len(df)), random_state=42)
#     out_path = path.replace(".csv", "_small.csv")
#     df_small.to_csv(out_path, index=False, encoding="utf-8")
#     print(f"✅ 已生成随机小数据集：{out_path}，共 {len(df_small)} 条")
#
# print("\n🎉 全部随机采样完成！")
import pandas as pd
from sklearn.model_selection import train_test_split

# 🔥 修复 Windows 路径（必须用 r"" 或者双斜杠）
INPUT_PATHS = [
    r"E:\毕业项目\dataset\prompts\prompt_plain.csv",
    r"E:\毕业项目\dataset\prompts\prompt_normal.csv",
    r"E:\毕业项目\dataset\prompts\prompt_graph.csv"
]

# 随机抽取数量
SAMPLE_SIZE = 1000

# 处理正常数据集
for path in INPUT_PATHS:
    df = pd.read_csv(path, encoding="utf-8")

    # 检查数据量是否足够
    if len(df) < SAMPLE_SIZE:
        print(f"⚠️ 警告：{path} 数据量 ({len(df)}) 小于所需样本数 ({SAMPLE_SIZE})，将使用全部数据")
        df_small = df
    else:
        # ✅ 分层随机抽样，按label比例采样
        # 先按label分组
        labels = df['label']

        # 使用train_test_split进行分层抽样
        df_small, _ = train_test_split(
            df,
            train_size=SAMPLE_SIZE,
            stratify=labels,  # 按label分层
            random_state=42
        )

    out_path = path.replace(".csv", "_small.csv")
    df_small.to_csv(out_path, index=False, encoding="utf-8")

    # 打印label分布
    label_counts = df_small['label'].value_counts()
    print(f"✅ 已生成分层随机小数据集：{out_path}")
    print(f"   样本数：{len(df_small)} 条，label分布：0={label_counts.get(0, 0)} 条，1={label_counts.get(1, 0)} 条")
    print(f"   比例：0={label_counts.get(0, 0) / len(df_small):.1%}，1={label_counts.get(1, 0) / len(df_small):.1%}")
    print()

# 处理对抗样本集
INPUT_PATHS_ADV = [
    r"E:\毕业项目\dataset\prompts\prompt_plain_adv.csv",
    r"E:\毕业项目\dataset\prompts\prompt_normal_adv.csv",
    r"E:\毕业项目\dataset\prompts\prompt_graph_adv.csv"
]

print("=" * 60)
print("开始处理对抗样本集...")

for path in INPUT_PATHS_ADV:
    df = pd.read_csv(path, encoding="utf-8")

    # 检查数据量是否足够
    if len(df) < SAMPLE_SIZE:
        print(f"⚠️ 警告：{path} 数据量 ({len(df)}) 小于所需样本数 ({SAMPLE_SIZE})，将使用全部数据")
        df_small = df
    else:
        # ✅ 分层随机抽样，按label比例采样
        labels = df['label']

        # 使用train_test_split进行分层抽样
        df_small, _ = train_test_split(
            df,
            train_size=SAMPLE_SIZE,
            stratify=labels,  # 按label分层
            random_state=42
        )

    out_path = path.replace(".csv", "_small.csv")
    df_small.to_csv(out_path, index=False, encoding="utf-8")

    # 打印label分布
    label_counts = df_small['label'].value_counts()
    print(f"✅ 已生成分层随机小数据集：{out_path}")
    print(f"   样本数：{len(df_small)} 条，label分布：0={label_counts.get(0, 0)} 条，1={label_counts.get(1, 0)} 条")
    print(f"   比例：0={label_counts.get(0, 0) / len(df_small):.1%}，1={label_counts.get(1, 0) / len(df_small):.1%}")
    print()

print("\n🎉 全部分层随机采样完成！")