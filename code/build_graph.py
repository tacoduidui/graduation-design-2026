# build_graph.py 文本 → 图结构（NetworkX）
import pandas as pd
import networkx as nx
from utils import parse_url, extract_keywords
from config import *

# ======================
# 函数1：单个文本生成图
# ======================
def build_single_graph(text, data_type):
    # 初始化空图
    G = nx.DiGraph()  # 有向图
    G.add_node("main", content=text)  # 主节点

    # 如果是URL
    if data_type == "url":
        parts = parse_url(text)
        protocol = parts["protocol"]
        domain = parts["domain"]
        suffix = parts["suffix"]

        # 添加子节点
        G.add_node("protocol", content=protocol)
        G.add_node("domain", content=domain)
        G.add_node("suffix", content=suffix)

        # 添加边
        G.add_edge("main", "protocol")
        G.add_edge("main", "domain")
        G.add_edge("main", "suffix")

    # 如果是邮件
    elif data_type == "email":
        keywords = extract_keywords(text)
        for i, kw in enumerate(keywords):
            node_name = f"kw_{i}"
            G.add_node(node_name, content=kw)
            G.add_edge("main", node_name)

    return G

# ======================
# 函数2：批量生成图并保存
# ======================
def build_all_graphs(CLEAN_DATA_1,GRAPH_DATA_1):
    # 1. 读取清洗好的数据
    df = pd.read_csv(CLEAN_DATA_1)

    graph_records = []  # 保存所有图结构信息
    graph_objects = []  # 保存图对象（用于可视化）

    # 2. 遍历每一条文本
    for idx, row in df.iterrows():
        text = str(row["text"])
        label = row["label"]
        data_type = row["type"]

        # 生成图
        G = build_single_graph(text, data_type)

        # 保存图结构信息（给大模型用）
        nodes = {k: v["content"] for k, v in G.nodes(data=True)}
        edges = list(G.edges())

        graph_records.append({
            "idx": idx,
            "text": text,
            "label": label,
            "type": data_type,
            "nodes": str(nodes),
            "edges": str(edges)
        })
        graph_objects.append(G)

    # 3. 保存图结构数据
    graph_df = pd.DataFrame(graph_records)
    save_path = GRAPH_DATA_1
    graph_df.to_csv(save_path, index=False, encoding="utf-8")

    print("✅ 图结构构建完成！已保存到：", save_path)
    return graph_df, graph_objects

if __name__ == "__main__":
    # build_all_graphs(CLEAN_DATA,GRAPH_DATA)
    build_all_graphs(ADV_DATA,GRAPH_DATA_ADV)