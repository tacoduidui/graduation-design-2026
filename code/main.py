from infer_engine import run_inference
from config import *

print("="*60)
print("🚀 STARTING END-TO-END INFERENCE FRAMEWORK")
print("="*60)

# # ---------------- 正常样本 ----------------
# print("\n[1] Running NO PROMPT (normal)...")
# run_inference(PROMPT_PLAIN_1, RESULT_PLAIN)
#
# print("\n[2] Running NORMAL TEXT PROMPT (normal)...")
# run_inference(PROMPT_NORMAL_1, RESULT_NORMAL)
#
# print("\n[3] Running GRAPH STRUCTURE PROMPT (normal)...")
# run_inference(PROMPT_GRAPH_1, RESULT_GRAPH)

# ---------------- 对抗样本 ----------------
# print("\n[4] Running NO PROMPT (adversarial)...")
# run_inference(PROMPT_PLAIN_1_ADV, RESULT_PLAIN_ADV)
#
# print("\n[5] Running NORMAL TEXT PROMPT (adversarial)...")
# run_inference(PROMPT_NORMAL_1_ADV, RESULT_NORMAL_ADV)

print("\n[6] Running GRAPH STRUCTURE PROMPT (adversarial)...")
run_inference(PROMPT_GRAPH_1_ADV, RESULT_GRAPH_ADV)

print("\n🎉 ALL STAGES COMPLETED SUCCESSFULLY!")