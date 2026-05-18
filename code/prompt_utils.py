# # prompt_utils.py
# # 作用：把保存的字符串格式 nodes/edges 转回可用格式
#
# def parse_nodes(nodes_str):
#     try:
#         return eval(nodes_str)  # 转成字典
#     except:
#         return {}
#
# def parse_edges(edges_str):
#     try:
#         return eval(edges_str)  # 转成列表
#     except:
#         return []
#
# # 把图结构转为自然语言
# def graph_to_natural(nodes, edges):
#     node_str = "、".join([f"{k}:{v}" for k, v in nodes.items() if v])
#     edge_str = "、".join([f"{a}→{b}" for a, b in edges])
#     return node_str, edge_str


# prompt_utils.py (ENGLISH VERSION)
# 作用：把保存的字符串格式 nodes/edges 转回可用格式

def parse_nodes(nodes_str):
    try:
        return eval(nodes_str)
    except:
        return {}

def parse_edges(edges_str):
    try:
        return eval(edges_str)
    except:
        return []

# 把图结构转为 英文自然语言
def graph_to_natural(nodes, edges):
    node_str = ", ".join([f"{k}:{v}" for k, v in nodes.items() if v])
    edge_str = ", ".join([f"{a} -> {b}" for a, b in edges])
    return node_str, edge_str


def graph_to_natural_enhanced(nodes, edges):
    """
    改进点：
    1. 增加类型标签，减少原始字符串干扰。
    2. 对长路径进行结构化描述。
    """
    # 1. 节点处理：只保留类型，或者对内容进行脱敏
    # 例如：与其写 http8:raw... 不如写 Content: [Long Path String]
    formatted_nodes = []
    for k, v in nodes.items():
        if k == 'main':
            # 对核心内容进行抽象，降低对抗样本干扰
            formatted_nodes.append(f"Root_Content(length:{len(str(v))})")
        else:
            formatted_nodes.append(f"{k.capitalize()}_Component('{v}')")

    node_str = ", ".join(formatted_nodes)

    # 2. 边处理：使用更具逻辑性的连接词
    formatted_edges = []
    for a, b in edges:
        formatted_edges.append(f"[{a}] is linked to [{b}]")

    edge_str = "; ".join(formatted_edges)

    # 3. 增加图的全局特征（关键！）
    graph_summary = f"The graph consists of {len(nodes)} functional segments."

    return node_str, f"{edge_str}. {graph_summary}"