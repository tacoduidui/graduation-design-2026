本项目是基于图结构提示工程的大模型恶意 URL 对抗检测系统，基于 Python 实现了恶意 URL 的检测与对抗性验证。系统支持数据集加载、模型调用、对抗样本生成、检测结果评估与日志记录，可用于网络安全威胁检测、恶意 URL 识别与鲁棒性验证等场景。
## 项目目录结构
"""├── .gitattributes
├── .gitignore.txt
├── ai_responses.log
├── batch_temp_1.jsonl
│   ├── build_graph.py
│   ├── clean_email.py
│   ├── clean_url.py
│   ├── config.py
│   ├── csv_json.py
│   ├── generate_adversarial.py
│   ├── generate_prompts.py
│   ├── infer_engine.py
│   ├── infer_engine_deepseek.py
│   ├── llm_api.py
│   ├── main.py
│   ├── make_small_dataset.py
│   ├── merge_data.py
│   ├── prompt_utils.py
│   ├── stage6_result_analyze.py
│   ├── utils.py
│   ├── visualize_graph.py
│   │   ├── adversarial_samples.csv
│   │   ├── adv_test_set.csv
│   │   ├── adv_test_set.csv
│   │   ├── clean_email.csv
│   │   ├── clean_original_samples.csv
│   │   ├── clean_url.csv
│   │   ├── email_graph.png
│   │   ├── email_graph1.png
│   │   ├── test_set.csv
│   │   ├── url_graph.png
│   │   ├── url_graph1.png
│   │   ├── graph_structure.csv
│   │   ├── graph_structure_adv.csv
│   │   ├── graph.json
│   │   ├── graph.jsonl
│   │   ├── graph_adv.json
│   │   ├── graph_adv.jsonl
│   │   ├── normal.json
│   │   ├── normal.jsonl
│   │   ├── normal_adv.json
│   │   ├── normal_adv.jsonl
│   │   ├── plain.json
│   │   ├── plain.jsonl
│   │   ├── plain_adv.json
│   │   ├── plain_adv.jsonl
│   │   ├── prompt_graph.csv
│   │   ├── prompt_graph_adv.csv
│   │   ├── prompt_graph_adv_small.csv
│   │   ├── prompt_graph_small.csv
│   │   ├── prompt_normal.csv
│   │   ├── prompt_normal_adv.csv
│   │   ├── prompt_normal_adv_small.csv
│   │   ├── prompt_normal_small.csv
│   │   ├── prompt_plain.csv
│   │   ├── prompt_plain_adv.csv
│   │   ├── prompt_plain_adv_small.csv
│   │   ├── prompt_plain_small.csv
│   │   ├── benign_url.csv
│   │   ├── urlhaus.csv
│   │   ├── urlhaus.csv
│   │   ├── urlhauscsv.txt
│   │   │   ├── csv.txt
│   │   ├── 下载.zip
│   ├── 1_plain_vs_normal.png
│   ├── 2_graph_only.png
│   ├── 3_all_comparison.png
│   ├── accuracy_comparison.png
│   ├── metrics_comparison.png
│   ├── result_graph.csv
│   ├── result_graph.csv.temp.csv
│   ├── result_graph_adv.csv
│   ├── result_graph_adv.csv.temp.csv
│   ├── result_normal.csv
│   ├── result_normal.csv.temp.csv
│   ├── result_normal_adv.csv
│   ├── result_normal_adv.csv.temp.csv
│   ├── result_plain.csv
│   ├── result_plain.csv.part1.csv
│   ├── result_plain.csv.temp.csv
│   ├── result_plain_adv.csv
│   ├── result_plain_adv.csv.temp.csv
├── result_plain.txt
├── _batch_task_1.jsonl"""
