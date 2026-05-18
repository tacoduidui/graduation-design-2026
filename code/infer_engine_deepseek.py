from config import *
import os
from openai import OpenAI
import pandas as pd
from tqdm import tqdm
import time
import json
from datetime import datetime
import requests
import logging
import httpx

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====================== 配置 ======================
RETRY_TIMES = 3
RETRY_DELAY = 2

# 检查必要的配置变量
try:
    from config import SYSTEM_PROMPT
except ImportError:
    SYSTEM_PROMPT = "你是一个有帮助的助手"
    logger.warning("⚠️ 使用默认的 SYSTEM_PROMPT")

try:
    from config import DEEPSEEK_API_KEY

    if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY == "your_api_key_here":
        raise ValueError("请配置有效的 DEEPSEEK_API_KEY")
except (ImportError, ValueError) as e:
    logger.error(f"❌ 请检查 config.py 中的 DEEPSEEK_API_KEY 配置: {e}")
    DEEPSEEK_API_KEY = None
    exit(1)


def create_client():
    """
    创建自定义的 OpenAI 客户端
    """
    try:
        # 获取代理设置
        proxy_url = None

        # 尝试从环境变量获取
        proxy_sources = [
            os.environ.get('HTTPS_PROXY'),
            os.environ.get('https_proxy'),
            os.environ.get('HTTP_PROXY'),
            os.environ.get('http_proxy'),
        ]

        for proxy in proxy_sources:
            if proxy:
                proxy_url = proxy
                logger.info(f"✅ 使用代理: {proxy_url}")
                break

        # 如果没有环境变量，尝试从 config.py 导入
        if not proxy_url:
            try:
                from config import HTTPS_PROXY, HTTP_PROXY
                proxy_url = HTTPS_PROXY or HTTP_PROXY
                if proxy_url:
                    logger.info(f"✅ 从 config.py 使用代理: {proxy_url}")
            except ImportError:
                pass

        # 创建 HTTP 客户端
        if proxy_url:
            # 创建带代理的客户端
            proxies = {
                "http://": proxy_url,
                "https://": proxy_url
            }

            http_client = httpx.Client(proxies=proxies, timeout=30.0)

            client = OpenAI(
                api_key=DEEPSEEK_API_KEY,
                base_url="https://api.deepseek.com",
                http_client=http_client
            )
        else:
            # 创建不带代理的客户端
            client = OpenAI(
                api_key=DEEPSEEK_API_KEY,
                base_url="https://api.deepseek.com"
            )
            logger.info("✅ 创建客户端，不使用代理")

        return client

    except Exception as e:
        logger.error(f"❌ 创建客户端失败: {e}")
        raise


# 初始化客户端
try:
    client = create_client()

    # 测试连接
    logger.info("正在测试 API 连接...")
    test_response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": "Hello, reply with 'test passed'"}],
        max_tokens=20
    )
    test_result = test_response.choices[0].message.content.strip()
    logger.info(f"✅ API 连接测试成功: {test_result}")

except Exception as e:
    logger.error(f"❌ 客户端初始化失败: {e}")
    client = None


# ==================================================

def call_glm(prompt: str) -> str:
    """
    调用 DeepSeek 模型
    """
    if client is None:
        logger.error("客户端未初始化，无法调用 API")
        return "api_failed"

    try:
        # 简单的 API 调用
        response = client.chat.completions.create(
            model="deepseek-chat",  # 模型名称
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt.strip()}
            ],
            max_tokens=4096,
            temperature=0.6,
            stream=False
        )
        # 提取响应内容
        answer = response.choices[0].message.content.strip().lower()
        logger.debug(f"API 响应: {answer[:100]}...")

        # 更灵活的响应检查
        if "yes" in answer or "是" in answer or "true" in answer:
            return "yes"
        elif "no" in answer or "否" in answer or "false" in answer:
            return "no"
        else:
            logger.warning(f"⚠️ 响应不明确: {answer[:50]}...")
            return "no"

    except Exception as e:
        logger.error(f"API 调用失败: {e}")
        return "api_failed"


def safe_call_glm(prompt):
    """
    带重试机制的包装函数
    """
    for i in range(RETRY_TIMES):
        try:
            result = call_glm(prompt)
            if result != "api_failed":
                return result
        except Exception as e:
            logger.warning(f"第 {i + 1} 次调用失败: {e}")
            if i < RETRY_TIMES - 1:
                time.sleep(RETRY_DELAY * (i + 1))
    return "api_failed"


def run_inference(prompt_path, output_path):
    """
    单线程推理
    """
    if client is None:
        logger.error("DeepSeek 客户端未初始化，无法进行推理")
        return None

    try:
        df = pd.read_csv(prompt_path, encoding="utf-8")
    except Exception as e:
        logger.error(f"读取 CSV 文件失败: {e}")
        return None

    results = []

    print(f"🚀 Starting API inference | total: {len(df)}")
    logger.info(f"开始推理，总计 {len(df)} 条数据")

    # 检查输出目录是否存在
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 改为单线程顺序处理
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Inferring"):
        prompt = row["prompt"]
        label = row["label"]
        text = row["text"]

        pred = safe_call_glm(prompt)

        if pred == "api_failed":
            logger.warning(f"第 {idx} 条数据 API 调用失败，跳过")
            result = {
                "idx": idx,
                "text": text,
                "label": "malicious" if label == 1 else "benign",
                "prompt": prompt,
                "predict": "api_failed",
                "error": "API调用失败"
            }
        else:
            result = {
                "idx": idx,
                "text": text,
                "label": "malicious" if label == 1 else "benign",
                "prompt": prompt,
                "predict": pred
            }

        results.append(result)

        # 实时保存进度
        if len(results) % 5 == 0:
            temp_df = pd.DataFrame(results)
            temp_df.to_csv(output_path + ".temp.csv", index=False, encoding="utf-8")
            logger.debug(f"已处理 {len(results)} 条数据")

    result_df = pd.DataFrame(results)
    result_df.to_csv(output_path, index=False, encoding="utf-8")

    # 删除临时文件
    temp_file = output_path + ".temp.csv"
    if os.path.exists(temp_file):
        os.remove(temp_file)

    # 统计结果
    success_count = len([r for r in results if r.get("predict") != "api_failed"])
    logger.info(f"✅ 完成 | 成功: {success_count}/{len(df)} | 失败: {len(df) - success_count}")
    print(f"✅ Done | Results saved: {output_path}")
    return result_df


# 测试函数
if __name__ == "__main__":
    # 测试 API 连接
    test_prompt = "请回答 yes 或 no: 这是测试吗？"
    print("测试 API 连接...")
    result = call_glm(test_prompt)
    print(f"测试结果: {result}")

    if result != "api_failed":
        print("✅ API 连接测试通过！")
    else:
        print("❌ API 连接测试失败，请检查网络和配置")