# # generate_prompts.py
# # 自动生成 3 种提示词：无提示、普通提示、图结构提示
#
# import pandas as pd
# from config import *
# from prompt_utils import parse_nodes, parse_edges, graph_to_natural
#
# # ==========================
# # 1. 生成【无提示】
# # ==========================
# def generate_plain_prompts(df):
#     prompts = []
#     for idx, row in df.iterrows():
#         prompts.append({
#             "idx": idx,
#             "text": row["text"],
#             "label": row["label"],
#             "prompt": row["text"]  # 直接输入文本
#         })
#     pd.DataFrame(prompts).to_csv(PROMPT_PLAIN, index=False, encoding="utf-8")
#     print("✅ 无提示生成完成")
#
# # ==========================
# # 2. 生成【普通文本提示】
# # ==========================
# def generate_normal_prompts(df):
#     prompts = []
#     template = """请判断以下内容是否为恶意内容。
# 内容：{}
# 仅回答是或否。"""
#
#     for idx, row in df.iterrows():
#         prompt_text = template.format(row["text"])
#         prompts.append({
#             "idx": idx,
#             "text": row["text"],
#             "label": row["label"],
#             "prompt": prompt_text
#         })
#     pd.DataFrame(prompts).to_csv(PROMPT_NORMAL, index=False, encoding="utf-8")
#     print("✅ 普通提示生成完成")
#
# # ==========================
# # 3. 生成【图结构提示 · 创新】
# # ==========================
# def generate_graph_prompts(graph_df):
#     prompts = []
#     template = """请根据以下结构信息判断内容是否为恶意。
# 结构节点：{}
# 结构关系：{}
# 请仅回答是或否。"""
#
#     for idx, row in graph_df.iterrows():
#         nodes = parse_nodes(row["nodes"])
#         edges = parse_edges(row["edges"])
#         node_str, edge_str = graph_to_natural(nodes, edges)
#
#         prompt_text = template.format(node_str, edge_str)
#         prompts.append({
#             "idx": idx,
#             "text": row["text"],
#             "label": row["label"],
#             "nodes": row["nodes"],
#             "edges": row["edges"],
#             "prompt": prompt_text
#         })
#
#     pd.DataFrame(prompts).to_csv(PROMPT_GRAPH, index=False, encoding="utf-8")
#     print("✅ 图结构提示生成完成")
#
# # ==========================
# # 主函数：一次性生成全部
# # ==========================
# if __name__ == "__main__":
#     df_clean = pd.read_csv(CLEAN_DATA)
#     df_graph = pd.read_csv(GRAPH_DATA)
#
#     generate_plain_prompts(df_clean)
#     generate_normal_prompts(df_clean)
#     generate_graph_prompts(df_graph)
#
#     print("\n🎉 阶段四全部完成！已生成 3 组提示词！")

# generate_prompts.py (ENGLISH PROMPTS)
import pandas as pd
from config import *
from prompt_utils import parse_nodes, parse_edges, graph_to_natural_enhanced

# ==========================
# 1. 生成【无提示】（不变）
# ==========================
def generate_plain_prompts(df,PROMPT_PLAIN_11):
    prompts = []
    for idx, row in df.iterrows():
        prompts.append({
            "idx": idx,
            "text": row["text"],
            "label": row["label"],
            "prompt": row["text"]
        })
    pd.DataFrame(prompts).to_csv(PROMPT_PLAIN_11, index=False, encoding="utf-8")
    print("✅ Plain prompts generated")

# ==========================
# 2. 生成【普通文本提示】- 英文
# ==========================
def generate_normal_prompts(df,PROMPT_NORMAL_11):
    prompts = []
    # 英文提示词（模型看得懂！）
    template = """Determine whether the following content is malicious.
Content: {}
Answer only YES or NO."""

    for idx, row in df.iterrows():
        prompt_text = template.format(row["text"])
        prompts.append({
            "idx": idx,
            "text": row["text"],
            "label": row["label"],
            "prompt": prompt_text
        })
    pd.DataFrame(prompts).to_csv(PROMPT_NORMAL_11, index=False, encoding="utf-8")
    print("✅ Normal text prompts generated")

# ==========================
# 3. 生成【图结构提示】- 英文（你的创新点）
# ==========================
def generate_graph_prompts(graph_df, PROMPT_GRAPH_11):
    prompts = []
    # 改进后的模板：增加任务背景，明确结构重要性
    template = """Task: Analyze the structural integrity of a URL to detect malicious patterns.
Structural Layout:
- Components (Nodes): {}
- Topology (Edges): {}

Security Reasoning: Check for abnormal deep hierarchies, suspicious redirections, or unusual component relationships.
Question: Is the underlying structure of this URL characteristic of a malicious attack?
Answer only YES or NO."""

    for idx, row in graph_df.iterrows():
        # 假设 row["nodes"] 和 row["edges"] 是字符串形式的 dict/list，需要解析
        # 这里建议对 parse_nodes 进行增强，提取统计特征
        nodes = parse_nodes(row["nodes"])
        edges = parse_edges(row["edges"])

        # 使用增强后的转换函数
        node_str, edge_str = graph_to_natural_enhanced(nodes, edges)

        prompt_text = template.format(node_str, edge_str)
        prompts.append({
            "idx": idx,
            "text": row["text"],
            "label": row["label"],
            "nodes": row["nodes"],
            "edges": row["edges"],
            "prompt": prompt_text
        })

    pd.DataFrame(prompts).to_csv(PROMPT_GRAPH_11, index=False, encoding="utf-8")
    print(f"✅ Enhanced Graph structure prompts generated: {len(prompts)} rows")

# ==========================
# 主函数
# ==========================
if __name__ == "__main__":
    # df_clean = pd.read_csv(CLEAN_DATA)
    # df_graph = pd.read_csv(GRAPH_DATA)
    #
    # generate_plain_prompts(df_clean,PROMPT_PLAIN)
    # generate_normal_prompts(df_clean,PROMPT_NORMAL)
    # generate_graph_prompts(df_graph,PROMPT_GRAPH)

    df_clean = pd.read_csv(ADV_DATA)
    df_graph = pd.read_csv(GRAPH_DATA_ADV)

    generate_plain_prompts(df_clean, PROMPT_PLAIN_ADV)
    generate_normal_prompts(df_clean, PROMPT_NORMAL_ADV)
    generate_graph_prompts(df_graph, PROMPT_GRAPH_ADV)

    print("\n🎉 All prompts (English version) generated successfully!")