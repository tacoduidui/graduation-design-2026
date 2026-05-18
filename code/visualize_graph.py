# visualize_graph.py 图可视化
import matplotlib.pyplot as plt
import networkx as nx
from build_graph import build_single_graph
from config import CLEAN_DATA
import pandas as pd
import os

# 画单张图
def visualize_single_graph(G, save_name):
    plt.figure(figsize=(8, 5))

    # 布局
    pos = nx.spring_layout(G, seed=42)

    # 画节点
    nx.draw_networkx_nodes(G, pos, node_size=1500, node_color="#ffcc00")
    nx.draw_networkx_labels(G, pos, font_size=10, font_family="SimHei" if os.name == "nt" else "DejaVu Sans")

    # 画边
    nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=20, edge_color="black")

    plt.axis("off")
    plt.tight_layout()
    save_path = os.path.join(os.path.dirname(CLEAN_DATA), f"{save_name}.png")
    plt.savefig(save_path, dpi=300)
    plt.close()
    print("✅ 图已保存：", save_path)

# 测试：画第1条URL和第1条邮件
if __name__ == "__main__":
    df = pd.read_csv(CLEAN_DATA)

    # 画第一条URL
    url_row = df[df["type"] == "url"].iloc[0]
    G_url = build_single_graph(url_row["text"], "url")
    visualize_single_graph(G_url, "url_graph")

    # 画第一条邮件
    email_row = df[df["type"] == "email"].iloc[0]
    G_email = build_single_graph(email_row["text"], "email")
    visualize_single_graph(G_email, "email_graph")