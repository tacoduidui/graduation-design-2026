# config.py：数据集处理与对抗样本生成核心参数配置
import os

# 1. 路径配置
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_DATA_DIR = os.path.join(BASE_DIR, "dataset", "raw")

# CLEAN_DATA_DIR = os.path.join(BASE_DIR, "/dataset", "clean")
ADV_DATA_DIR = os.path.join(BASE_DIR, "dataset", "adversarial")


# # 创建目录（若不存在）
# for dir_path in [CLEAN_DATA_DIR, ADV_DATA_DIR]:
#     if not os.path.exists(dir_path):
#         os.makedirs(dir_path)

# 2. 数据处理参数
# 测试集比例（原始样本划分训练/测试，对抗样本仅在测试集生成，避免数据泄露）
TEST_SIZE = 0.2
# 随机种子（保证实验可复现）
RANDOM_SEED = 42
# 良性样本补充：URL/邮件数据集恶意样本居多，补充少量良性样本（后续可从公开良性数据集下载，此处先占位）
# BENIGN_URL_CSV = os.path.join(RAW_DATA_DIR, "benign_url.csv")
BENIGN_EMAIL_CSV = os.path.join(RAW_DATA_DIR, "benign_email.csv")

# 3. 对抗样本生成参数
# 每个原始样本生成的对抗样本数（避免算力消耗过大）1 个原始样本 → 生成 1 个对抗样本
ADV_NUM_PER_SAMPLE = 1
# 攻击方法：TextAttack内置轻量方法，适配URL/短文本
# 字符级：RandomCharacterSwap（随机字符替换）、InsertRandomCharacter（随机字符插入）
# 词汇级：WordSwapRandomSynonym（随机同义词替换）
ATTACK_METHOD = "WordSwapRandomSynonym"
# 生成对抗样本的最大尝试次数（避免单样本生成耗时过久）
MAX_ATTEMPTS = 10
# 对抗样本保存格式
ADV_CSV_NAME = "adversarial_samples.csv"
# 原始清洗样本保存格式
CLEAN_CSV_NAME = "clean_original_samples.csv"





#个人修改
RAW_URL_PATH="E:/毕业项目/dataset/raw/urlhaus.csv"
CLEAN_DATA_DIR="E:/毕业项目/dataset/clean"
BENIGN_URL_CSV="E:/毕业项目/dataset/raw/benign_url.csv"


CLEAN_DATA ="E:\毕业项目\dataset\clean/test_set.csv"
ADV_DATA="E:\毕业项目\dataset/adversarial/adv_test_set.csv"
# 输出：图结构保存路径
GRAPH_OUTPUT = os.path.join(BASE_DIR, "dataset/graph")
os.makedirs(GRAPH_OUTPUT, exist_ok=True)


GRAPH_DATA ="E:\毕业项目\dataset\graph\graph_structure.csv"
GRAPH_DATA_ADV ="E:\毕业项目\dataset\graph\graph_structure_adv.csv"
# 输出：阶段四生成的三种提示词
PROMPT_OUTPUT = os.path.join(BASE_DIR, "dataset/prompts")
os.makedirs(PROMPT_OUTPUT, exist_ok=True)

# 三种提示词保存路径（原始）
PROMPT_PLAIN = os.path.join(PROMPT_OUTPUT, "prompt_plain.csv")    # 无提示
PROMPT_NORMAL = os.path.join(PROMPT_OUTPUT, "prompt_normal.csv") # 普通文本提示
PROMPT_GRAPH = os.path.join(PROMPT_OUTPUT, "prompt_graph.csv")    # 图结构提示（创新）
# 三种提示词保存路径（原始小）
PROMPT_PLAIN_1 = os.path.join(PROMPT_OUTPUT, "prompt_plain_small.csv")    # 无提示
PROMPT_NORMAL_1 = os.path.join(PROMPT_OUTPUT, "prompt_normal_small.csv") # 普通文本提示
PROMPT_GRAPH_1 = os.path.join(PROMPT_OUTPUT, "prompt_graph_small.csv")    # 图结构提示（创新）

# 三种提示词保存路径（对抗）
PROMPT_PLAIN_ADV = os.path.join(PROMPT_OUTPUT, "prompt_plain_adv.csv")    # 无提示
PROMPT_NORMAL_ADV = os.path.join(PROMPT_OUTPUT, "prompt_normal_adv.csv") # 普通文本提示
PROMPT_GRAPH_ADV = os.path.join(PROMPT_OUTPUT, "prompt_graph_adv.csv")    # 图结构提示（创新）
# 三种提示词保存路径（对抗小）
PROMPT_PLAIN_1_ADV = os.path.join(PROMPT_OUTPUT, "prompt_plain_adv_small.csv")    # 无提示
PROMPT_NORMAL_1_ADV = os.path.join(PROMPT_OUTPUT, "prompt_normal_adv_small.csv") # 普通文本提示
PROMPT_GRAPH_1_ADV = os.path.join(PROMPT_OUTPUT, "prompt_graph_adv_small.csv")    # 图结构提示（创新）

# # 三种提示词保存路径
# PROMPT_PLAIN = os.path.join(PROMPT_OUTPUT, "prompt_plain.csv")    # 无提示
# PROMPT_NORMAL = os.path.join(PROMPT_OUTPUT, "prompt_normal.csv") # 普通文本提示
# PROMPT_GRAPH = os.path.join(PROMPT_OUTPUT, "prompt_graph.csv")    # 图结构提示（创新）

# 输出结果路径
RESULT_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(RESULT_DIR, exist_ok=True)

# 推理结果保存路径
RESULT_PLAIN = os.path.join(RESULT_DIR, "result_plain.csv")
RESULT_NORMAL = os.path.join(RESULT_DIR, "result_normal.csv")
RESULT_GRAPH = os.path.join(RESULT_DIR, "result_graph.csv")

# 推理结果保存路径
RESULT_PLAIN_ADV = os.path.join(RESULT_DIR, "result_plain_adv.csv")
RESULT_NORMAL_ADV = os.path.join(RESULT_DIR, "result_normal_adv.csv")
RESULT_GRAPH_ADV = os.path.join(RESULT_DIR, "result_graph_adv.csv")

# 大模型API配置（你自己的key）
LLM_API_KEY = "79d9f63a0ef44193add7046419a6f705.RIbnVowXjFgvo6zI"
DEEPSEEK_API_KEY="sk-f5bc2f3ef86c4dc58d0e9f5a19258513"
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
MODEL = "glm-4.5-air"
# ===================== SYSTEM PROMPT (PURE ENGLISH) =====================
SYSTEM_PROMPT = """
Only return 'yes' or 'no'.
"""

PLAINJSON=os.path.join(PROMPT_OUTPUT, "plain.jsonl")
NORMALJSON=os.path.join(PROMPT_OUTPUT, "normal.jsonl")
GRAPHJSON=os.path.join(PROMPT_OUTPUT, "graph.jsonl")
PLAINJSON_ADV=os.path.join(PROMPT_OUTPUT, "plain_adv.jsonl")
NORMALJSON_ADV=os.path.join(PROMPT_OUTPUT, "normal_adv.jsonl")
GRAPHJSON_ADV=os.path.join(PROMPT_OUTPUT, "graph_adv.jsonl")