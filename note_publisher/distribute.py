"""Multi-platform distribution"""
import subprocess, os, re
from .client import NoteClient

SKILLS = os.path.expanduser("~/.pi/agent/skills")
SCRIPTS = os.path.expanduser("~/.pi/agent/scripts")

def distribute(note_url: str, substack: bool = True, x: bool = True, threads: bool = True, cookie: str = None) -> dict:
    """note記事を各プラットフォームに拡散"""
    results = {}
    note_key = re.search(r'n/([a-z0-9]+)', note_url).group(1)
    
    # 記事情報取得
    if cookie:
        client = NoteClient(cookie)
        article = client.get_article(note_key)
    else:
        import requests
        r = requests.get(f"https://note.com/api/v3/notes/{note_key}/")
        article = {"title": r.json()["data"]["name"], "eyecatch": r.json()["data"].get("eyecatch", ""), "url": note_url}
    
    # X
    if x:
        r = subprocess.run(["bash", f"{SKILLS}/x-post/x-post.sh", f"{article['title']}\n\n{article['url']}\n\n#AI #LLM #note"], capture_output=True, text=True, timeout=30)
        results["x"] = "ok" if "Done" in r.stdout else "failed"
    
    # Threads
    if threads:
        cmd = ["bash", f"{SKILLS}/threads-post/threads-post.sh"]
        if article.get("eyecatch"):
            cmd += ["--image", article["eyecatch"]]
        cmd.append(f"{article['title']}\n\n{article['url']}")
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        results["threads"] = "ok" if '"status":"ok"' in r.stdout else "failed"
    
    # Substack
    if substack:
        r = subprocess.run(["bash", f"{SCRIPTS}/substack-publish.sh", article["title"], "", "/tmp/substack-dist.md"], capture_output=True, text=True, timeout=60)
        results["substack"] = "ok" if "Published" in r.stdout else "failed"
    
    return results

if __name__ == "__main__":
    import sys
    r = distribute(sys.argv[1])
    for k, v in r.items():
        print(f"{'✅' if v == 'ok' else '❌'} {k}")
