# utils.py 文本→图结构解析工具
from urllib.parse import urlparse

# 解析URL，返回协议、域名、路径、后缀
def parse_url(url):
    try:
        res = urlparse(url)
        protocol = res.scheme
        domain = res.netloc
        path = res.path
        suffix = path.split(".")[-1] if "." in path else ""
        return {
            "protocol": protocol,
            "domain": domain,
            "path": path,
            "suffix": suffix
        }
    except:
        return {"protocol": "", "domain": "", "path": "", "suffix": ""}

# 简单提取邮件关键词（按空格分词，取前5个）
def extract_keywords(text, max_k=5):
    words = text.split()
    words = [w for w in words if len(w) > 1]
    return words[:max_k]