# import pandas as pd
# from tqdm import tqdm
# from llm_api import call_glm
# import concurrent.futures
# import time
# import os
#
# # ====================== 并发配置 ======================
# MAX_WORKERS = 1
# RETRY_TIMES = 2
# RETRY_DELAY = 1
#
# # ======================================================
#
# def safe_call_glm(prompt):
#     for i in range(RETRY_TIMES):
#         try:
#             return call_glm(prompt)
#         except Exception as e:
#             if i == RETRY_TIMES - 1:
#                 return "api_failed"
#             time.sleep(RETRY_DELAY)
#     return "api_failed"
#
# def run_inference(prompt_path, output_path):
#     df = pd.read_csv(prompt_path, encoding="utf-8")
#     total = len(df)
#     results = [None] * total
#
#     def process_row(idx_row):
#         idx, row = idx_row
#         prompt = row["prompt"]
#         label = row["label"]
#         text = row["text"]
#         pred = safe_call_glm(prompt)
#
#         return {
#             "idx": idx,
#             "text": text,
#             "label": "malicious" if label == 1 else "benign",
#             "prompt": prompt,
#             "predict": pred
#         }
#
#     print(f"🚀 Starting API inference | workers: {MAX_WORKERS} | total: {total}")
#     with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
#         tasks = [executor.submit(process_row, (idx, row)) for idx, row in df.iterrows()]
#
#         for future in tqdm(concurrent.futures.as_completed(tasks), total=total, desc="Inferring"):
#             res = future.result()
#             results[res["idx"]] = res
#
#             temp_df = pd.DataFrame([r for r in results if r is not None])
#             temp_df.to_csv(output_path + ".temp.csv", index=False, encoding="utf-8")
#
#     result_df = pd.DataFrame([r for r in results if r is not None])
#     result_df.to_csv(output_path, index=False, encoding="utf-8")
#     print(f"✅ Done | Results saved: {output_path}\n")
#     return result_df

from config import *
from zai import ZhipuAiClient  # 使用官方 SDK
import pandas as pd
from tqdm import tqdm
import time
import json
from datetime import datetime

# ====================== 配置 ======================
RETRY_TIMES = 2
RETRY_DELAY = 1
client = ZhipuAiClient(api_key=LLM_API_KEY)

# ==================================================

def call_glm(prompt: str) -> str:
    """
    使用 ZhipuAI 官方 SDK 调用模型
    """
    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt.strip()}
            ],
            # thinking={"type": "enabled"},  # 启用深度思考
            max_tokens=4096,
            temperature=0.6
        )
        # 提取响应内容
        answer = response.choices[0].message.content.strip().lower()
        # # ============== 新增：保存完整回复到文件 ==============
        # log_entry = {
        #     "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        #     "prompt": prompt.strip(),
        #     "full_response": answer,  # 保存完整回复
        #     "model": MODEL,
        #     "temperature": 0.6
        # }
        #
        # # 追加写入日志文件
        # with open("ai_responses.log", "a", encoding="utf-8") as f:
        #     f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        # # ==================================================
        return "yes" if "yes" in answer else "no"

    except Exception as e:
        print(f"API 调用失败: {e}")
        return "no"


def safe_call_glm(prompt):
    """
    带重试机制的包装函数
    """
    for i in range(RETRY_TIMES):
        try:
            return call_glm(prompt)
        except Exception as e:
            if i == RETRY_TIMES - 1:
                return "api_failed"
            time.sleep(RETRY_DELAY)
    return "api_failed"


def run_inference(prompt_path, output_path):
    """
    单线程推理（已移除并发）
    """
    df = pd.read_csv(prompt_path, encoding="utf-8")
    results = []

    print(f"🚀 Starting API inference | workers: 1 (sequential) | total: {len(df)}")

    # 改为单线程顺序处理
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Inferring"):
        prompt = row["prompt"]
        label = row["label"]
        text = row["text"]

        pred = safe_call_glm(prompt)

        result = {
            "idx": idx,
            "text": text,
            "label": "malicious" if label == 1 else "benign",
            "prompt": prompt,
            "predict": pred
        }
        results.append(result)

        # 实时保存进度
        temp_df = pd.DataFrame(results)
        temp_df.to_csv(output_path + ".temp.csv", index=False, encoding="utf-8")

    result_df = pd.DataFrame(results)
    result_df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"✅ Done | Results saved: {output_path}\n")
    return result_df