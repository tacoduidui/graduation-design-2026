import csv
import json
from config import *


def csv_to_batch_json(csv_file, output_file="batch_requests.jsonl"):
    """
    将CSV评论转换成指定格式的批量请求JSONL文件
    :param csv_file: 输入CSV路径
    :param output_file: 输出JSONL路径
    """
    # 打开输出文件（每行一个JSON）
    with open(output_file, "w", encoding="utf-8") as f_out:
        # 读取CSV
        with open(csv_file, "r", encoding="utf-8") as f_in:
            reader = csv.DictReader(f_in)  # 自动识别表头

            # 遍历每一行评论
            for index, row in enumerate(reader, start=1):
                # 直接读取 prompt 列内容
                prompt_text = row.get("prompt", "").strip()
                if not prompt_text:
                    continue  # 跳过空内容

                # 构造用户提示词（严格按照你给的格式）


                # 构造完整JSON结构
                request_json = {
                    "custom_id": f"request-{index}",
                    "method": "POST",
                    "url": "/v4/chat/completions",
                    "body": {
                        "model": MODEL,
                        "messages": [
                            {
                                "role": "system",
                                "content": SYSTEM_PROMPT
                            },
                            {
                                "role": "user",
                                "content": prompt_text
                            }
                        ]
                    }
                }

                # 写入文件（每行一个JSON）
                f_out.write(json.dumps(request_json, ensure_ascii=False) + "\n")

    print(f"✅ 转换完成！共生成 {index} 条请求")
    print(f"📄 输出文件：{output_file}")


# 运行转换
if __name__ == "__main__":
    csv_to_batch_json(PROMPT_PLAIN_1, PLAINJSON)
    csv_to_batch_json(PROMPT_NORMAL_1, NORMALJSON)
    csv_to_batch_json(PROMPT_GRAPH_1, GRAPHJSON)

    csv_to_batch_json(PROMPT_PLAIN_1_ADV, PLAINJSON_ADV)
    csv_to_batch_json(PROMPT_NORMAL_1_ADV, NORMALJSON_ADV)
    csv_to_batch_json(PROMPT_GRAPH_1_ADV,GRAPHJSON_ADV)