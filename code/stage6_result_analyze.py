# # import pandas as pd
# # from config import *
# # # ==============================
# # # File Paths (ENGLISH)
# # # ==============================
# # PATH_PLAIN = "../results/result_plain.csv"
# # PATH_NORMAL = "../results/result_normal.csv"
# # PATH_GRAPH = "../results/result_graph.csv"
# #
# # # ==============================
# # # Safe CSV Reader
# # # ==============================
# # def safe_read_csv(path):
# #     return pd.read_csv(path, encoding="utf-8")
# #
# # # ==============================
# # # Label Mapping (ENGLISH VERSION)
# # # label: malicious / benign
# # # predict: yes / no
# # # ==============================
# # def get_true_label(label_str):
# #     s = str(label_str).strip().lower()
# #     if s == "malicious":
# #         return 1
# #     elif s == "benign":
# #         return 0
# #     else:
# #         return 0
# #
# # def get_pred_label(pred_str):
# #     s = str(pred_str).strip().lower()
# #     if s == "yes":
# #         return 1
# #     elif s == "no":
# #         return 0
# #     else:
# #         return 0
# #
# # # ==============================
# # # Calculate Accuracy Metrics
# # # ==============================
# # def calc_metrics(path, name):
# #     df = safe_read_csv(path)
# #     y_true = []
# #     y_pred = []
# #
# #     for _, row in df.iterrows():
# #         y_true.append(get_true_label(row["label"]))
# #         y_pred.append(get_pred_label(row["predict"]))
# #
# #     correct = sum(t == p for t, p in zip(y_true, y_pred))
# #     total = len(y_true)
# #     acc = correct / total if total != 0 else 0.0
# #
# #     print(f"==============================================")
# #     print(f"📊【{name}】")
# #     print(f"Total Accuracy:    {acc:.2%}")
# #     print(f"Correct/Total:     {correct}/{total}")
# #     print(f"==============================================")
# #
# #     return {
# #         "Method": name,
# #         "Accuracy": round(acc, 3),
# #         "Correct": correct,
# #         "Total": total
# #     }
# #
# #
# #
# #
# #
# #
# # print("\n🔥 Stage 6: Experimental Results Calculation\n")
# # res_plain = calc_metrics(RESULT_PLAIN_ADV, "No Prompt")
# # res_normal = calc_metrics(RESULT_NORMAL_ADV, "Normal Text Prompt")
# # res_graph = calc_metrics(RESULT_GRAPH_ADV, "Graph Structure Prompt")
# #
# # print("\n\n✅ Final Comparison Table (For Thesis)")
# # df_result = pd.DataFrame([res_plain, res_normal, res_graph])
# # print(df_result.to_string(index=False))
# #
# # print("\n📈 Improvement")
# # imp_normal = (res_graph["Accuracy"] - res_normal["Accuracy"]) * 100
# # imp_plain = (res_graph["Accuracy"] - res_plain["Accuracy"]) * 100
# # print(f"Improvement over Normal Prompt: +{imp_normal:.2f}%")
# # print(f"Improvement over No Prompt:      +{imp_plain:.2f}%")
# #
# # print("\n🎉 Stage 6 Completed!")
#
#
#
# import pandas as pd
# import numpy as np
# from config import *
#
# # ==============================
# # File Paths (ENGLISH)
# # ==============================
# PATH_PLAIN = "../results/result_plain.csv"
# PATH_NORMAL = "../results/result_normal.csv"
# PATH_GRAPH = "../results/result_graph.csv"
#
#
# # ==============================
# # Safe CSV Reader
# # ==============================
# def safe_read_csv(path):
#     return pd.read_csv(path, encoding="utf-8")
#
#
# # ==============================
# # Label Mapping (ENGLISH VERSION)
# # label: malicious / benign
# # predict: yes / no
# # ==============================
# def get_true_label(label_str):
#     s = str(label_str).strip().lower()
#     if s == "malicious":
#         return 1
#     elif s == "benign":
#         return 0
#     else:
#         return 0
#
#
# def get_pred_label(pred_str):
#     s = str(pred_str).strip().lower()
#     if s == "yes":
#         return 1
#     elif s == "no":
#         return 0
#     else:
#         return 0
#
#
# # ==============================
# # Calculate Accuracy, Precision, Recall, F1
# # ==============================
# def calc_metrics(path, name):
#     df = safe_read_csv(path)
#     y_true = []
#     y_pred = []
#
#     for _, row in df.iterrows():
#         y_true.append(get_true_label(row["label"]))
#         y_pred.append(get_pred_label(row["predict"]))
#
#     y_true = np.array(y_true)
#     y_pred = np.array(y_pred)
#
#     # 计算混淆矩阵各项
#     TP = np.sum((y_true == 1) & (y_pred == 1))  # 真阳性（恶意预测正确）
#     TN = np.sum((y_true == 0) & (y_pred == 0))  # 真阴性（良性预测正确）
#     FP = np.sum((y_true == 0) & (y_pred == 1))  # 假阳性
#     FN = np.sum((y_true == 1) & (y_pred == 0))  # 假阴性
#
#     # 指标计算（防止除0）
#     total = len(y_true)
#     correct = TP + TN
#     acc = correct / total if total != 0 else 0.0
#
#     # 精确率 Precision：预测为恶意的里面，真的恶意占比
#     precision = TP / (TP + FP) if (TP + FP) != 0 else 0.0
#
#     # 召回率 Recall：实际恶意中，被检测出来的占比（等于你原来的Yes准确率）
#     recall = TP / (TP + FN) if (TP + FN) != 0 else 0.0
#
#     # F1分数
#     f1 = 2 * precision * recall / (precision + recall) if (precision + recall) != 0 else 0.0
#
#     # 良性样本准确率（No准确率）
#     benign_total = TN + FP
#     no_acc = TN / benign_total if benign_total != 0 else 0.0
#
#     print(f"==============================================")
#     print(f"📊【{name}】")
#     print(f"总准确率(Accuracy):    {acc:.2%}")
#     print(f"精确率(Precision):     {precision:.2%}")
#     print(f"召回率(Recall):        {recall:.2%}")
#     print(f"F1分数(F1):            {f1:.4f}")
#     print(f"恶意识别正确:          {TP}/{TP+FN}")
#     print(f"良性识别正确:          {TN}/{TN+FP}")
#     print(f"总正确/总数:           {correct}/{total}")
#     print(f"==============================================")
#
#     return {
#         "Method": name,
#         "Accuracy": round(acc, 3),
#         "Precision": round(precision, 3),
#         "Recall": round(recall, 3),
#         "F1": round(f1, 3),
#         "TP": TP,
#         "TN": TN,
#         "Correct": correct,
#         "Total": total
#     }
#
#
# print("\n🔥 Stage 6: Experimental Results Calculation\n")
# res_plain = calc_metrics(RESULT_PLAIN_ADV, "No Prompt")
# res_normal = calc_metrics(RESULT_NORMAL_ADV, "Normal Text Prompt")
# res_graph = calc_metrics(RESULT_GRAPH_ADV, "Graph Structure Prompt")
#
# print("\n\n✅ Final Comparison Table (For Thesis)")
# df_result = pd.DataFrame([res_plain, res_normal, res_graph])
# # 只打印论文需要的核心列
# print(df_result[["Method", "Accuracy", "Precision", "Recall", "F1"]].to_string(index=False))
#
# print("\n📈 Improvement (Graph vs Others)")
# print("总准确率提升:")
# imp_normal = (res_graph["Accuracy"] - res_normal["Accuracy"]) * 100
# imp_plain = (res_graph["Accuracy"] - res_plain["Accuracy"]) * 100
# print(f"  - 相比Normal Prompt: +{imp_normal:.2f}%")
# print(f"  - 相比No Prompt:      +{imp_plain:.2f}%")
#
# print("\n精确率提升:")
# p_imp_normal = (res_graph["Precision"] - res_normal["Precision"]) * 100
# p_imp_plain = (res_graph["Precision"] - res_plain["Precision"]) * 100
# print(f"  - 相比Normal Prompt: +{p_imp_normal:.2f}%")
# print(f"  - 相比No Prompt:      +{p_imp_plain:.2f}%")
#
# print("\n召回率提升:")
# r_imp_normal = (res_graph["Recall"] - res_normal["Recall"]) * 100
# r_imp_plain = (res_graph["Recall"] - res_plain["Recall"]) * 100
# print(f"  - 相比Normal Prompt: +{r_imp_normal:.2f}%")
# print(f"  - 相比No Prompt:      +{r_imp_plain:.2f}%")
#
# print("\nF1提升:")
# f1_imp_normal = (res_graph["F1"] - res_normal["F1"]) * 100
# f1_imp_plain = (res_graph["F1"] - res_plain["F1"]) * 100
# print(f"  - 相比Normal Prompt: +{f1_imp_normal:.2f}%")
# print(f"  - 相比No Prompt:      +{f1_imp_plain:.2f}%")
#
# print("\n🎉 Stage 6 Completed!")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from config import *

# ==============================
# 字体设置（无中文，不报错）
# ==============================
plt.rcParams['axes.unicode_minus'] = False
plt.style.use('seaborn-v0_8-whitegrid')

# ==============================
# 文件路径
# ==============================
PATH_PLAIN = "../results/result_plain.csv"
PATH_NORMAL = "../results/result_normal.csv"
PATH_GRAPH = "../results/result_graph.csv"

# ==============================
# CSV 读取
# ==============================
def safe_read_csv(path):
    return pd.read_csv(path, encoding="utf-8")

# ==============================
# 标签映射
# ==============================
def get_true_label(label_str):
    s = str(label_str).strip().lower()
    return 1 if s == "malicious" else 0

def get_pred_label(pred_str):
    s = str(pred_str).strip().lower()
    return 1 if s == "yes" else 0

# ==============================
# 计算指标
# ==============================
def calc_metrics(path, name):
    df = safe_read_csv(path)
    y_true = [get_true_label(row["label"]) for _, row in df.iterrows()]
    y_pred = [get_pred_label(row["predict"]) for _, row in df.iterrows()]

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    TP = np.sum((y_true == 1) & (y_pred == 1))
    TN = np.sum((y_true == 0) & (y_pred == 0))
    FP = np.sum((y_true == 0) & (y_pred == 1))
    FN = np.sum((y_true == 1) & (y_pred == 0))

    total = len(y_true)
    acc = (TP + TN) / total if total else 0
    precision = TP / (TP + FP) if (TP + FP) else 0
    recall = TP / (TP + FN) if (TP + FN) else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0

    print(f"==============================================")
    print(f"📊【{name}】")
    print(f"Accuracy:    {acc:.2%}")
    print(f"Precision:   {precision:.2%}")
    print(f"Recall:      {recall:.2%}")
    print(f"F1:          {f1:.4f}")
    print(f"Malicious Correct: {TP}/{TP+FN}")
    print(f"Benign Correct:    {TN}/{TN+FP}")
    print(f"Correct/Total:     {TP+TN}/{total}")
    print(f"==============================================")

    return {
        "Method": name,
        "Accuracy": round(acc, 3),
        "Precision": round(precision, 3),
        "Recall": round(recall, 3),
        "F1": round(f1, 3)
    }

# ==============================
# 图1：无提示 vs 文本提示
# ==============================
def plot_plain_vs_normal(res_plain, res_normal):
    names = ["No Prompt", "Normal Text Prompt"]
    acc = [res_plain["Accuracy"], res_normal["Accuracy"]]
    pre = [res_plain["Precision"], res_normal["Precision"]]
    rec = [res_plain["Recall"], res_normal["Recall"]]
    f1s = [res_plain["F1"], res_normal["F1"]]

    x = np.arange(len(names))
    w = 0.2

    plt.figure(figsize=(10, 5))
    plt.bar(x - 1.5*w, acc, w, label='Accuracy')
    plt.bar(x - 0.5*w, pre, w, label='Precision')
    plt.bar(x + 0.5*w, rec, w, label='Recall')
    plt.bar(x + 1.5*w, f1s, w, label='F1-Score')

    plt.title('No Prompt vs Normal Text Prompt')
    plt.xticks(x, names)
    plt.ylim(0, 1.1)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("../results/1_plain_vs_normal.png", dpi=300)

# ==============================
# 图2：图结构提示单独指标
# ==============================
def plot_graph_only(res_graph):
    metrics = ["Accuracy", "Precision", "Recall", "F1-Score"]
    values = [res_graph["Accuracy"],
              res_graph["Precision"],
              res_graph["Recall"],
              res_graph["F1"]]

    plt.figure(figsize=(8, 5))
    plt.bar(metrics, values, color='#2ca02c')
    plt.title('Graph Structure Prompt Performance')
    plt.ylim(0, 1.1)
    for i, v in enumerate(values):
        plt.text(i, v+0.01, f'{v:.3f}', ha='center')
    plt.tight_layout()
    plt.savefig("../results/2_graph_only.png", dpi=300)

# ==============================
# 图3：三者最终对比图
# ==============================
def plot_all_three(res_plain, res_normal, res_graph):
    methods = [res_plain["Method"], res_normal["Method"], res_graph["Method"]]
    acc = [res_plain["Accuracy"], res_normal["Accuracy"], res_graph["Accuracy"]]
    pre = [res_plain["Precision"], res_normal["Precision"], res_graph["Precision"]]
    rec = [res_plain["Recall"], res_normal["Recall"], res_graph["Recall"]]
    f1s = [res_plain["F1"], res_normal["F1"], res_graph["F1"]]

    x = np.arange(len(methods))
    w = 0.2

    plt.figure(figsize=(12, 6))
    plt.bar(x - 1.5*w, acc, w, label='Accuracy')
    plt.bar(x - 0.5*w, pre, w, label='Precision')
    plt.bar(x + 0.5*w, rec, w, label='Recall')
    plt.bar(x + 1.5*w, f1s, w, label='F1-Score')

    plt.title('Overall Comparison: No Prompt / Text Prompt / Graph Prompt')
    plt.xticks(x, methods)
    plt.ylim(0, 1.1)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("../results/3_all_comparison.png", dpi=300)
    plt.show()

# ==============================
# 主程序
# ==============================
if __name__ == "__main__":
    print("\n🔥 Stage 6: Experimental Results Calculation\n")

    res_plain = calc_metrics(RESULT_PLAIN_ADV, "No Prompt")
    res_normal = calc_metrics(RESULT_NORMAL_ADV, "Normal Text Prompt")
    res_graph = calc_metrics(RESULT_GRAPH_ADV, "Graph Structure Prompt")

    # 输出表格
    print("\n✅ Final Comparison Table")
    df = pd.DataFrame([res_plain, res_normal, res_graph])
    print(df.to_string(index=False))

    # 依次生成三张图
    print("\n📊 Generating 3 figures in order...")
    plot_plain_vs_normal(res_plain, res_normal)
    plot_graph_only(res_graph)
    plot_all_three(res_plain, res_normal, res_graph)

    print("\n🎉 All 3 figures saved to ../results/")