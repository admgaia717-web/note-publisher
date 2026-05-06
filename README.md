# note-publisher — note.com API非公式クライアント + マルチプラットフォーム拡散

**note.comに記事を投稿し、Substack / X(Twitter) / Threadsに一括拡散するPython CLI。**

非公式APIをリバースエンジニアリングし、1コマンドで記事投稿→全チャネル拡散を実現。

## 特徴

- 📝 note.comに記事を公開（非公式API、Cookie認証）
- 🖼 アイキャッチ画像の自動アップロード（1280x672対応）
- 🐦 X/Twitterに同時投稿
- 🧵 Threadsに画像付きで同時投稿
- ✍️ SubstackにMarkdown変換して同時投稿
- 🔄 全チャネル一括または選択実行
- 🐍 Python 3.13+ / 依存最小限

## インストール

```bash
git clone https://github.com/famous-prawn/note-publisher.git
cd note-publisher
pip install -r requirements.txt
```

## 使い方

### 1. 記事を公開

```python
from note_publisher import NotePublisher

pub = NotePublisher(cookie="_note_session_v5=xxxxx")

# 記事公開
result = pub.publish(
    title="タイトル",
    body="<h2>見出し</h2><p>本文</p>",
    eyecatch_path="~/ComfyUI/output/eyecatch.png",
    hashtags=["#AI", "#note"]
)
print(result["url"])  # → https://note.com/user/n/xxxxx
```

### 2. 全チャネルに一括拡散

```bash
# CLI
python -m note_publisher.distribute "https://note.com/user/n/xxxxx"

# or Python
from note_publisher.distribute import distribute
distribute("https://note.com/user/n/xxxxx", substack=True, x=True, threads=True)
```

### 3. 設定

```bash
# ~/.note-publisher.env
NOTE_COOKIE=_note_session_v5=xxxxx
NOTE_USER=famous_prawn2009
SUBSTACK_SID=s%3Axxxxx
INSTAGRAM_USER=keity717328
```

## 依存サービス

| 機能 | 認証 | 備考 |
|------|------|------|
| note.com API | Cookie (`_note_session_v5`) | ブラウザでログイン→開発者ツールで取得 |
| X/Twitter | Playwright Cookie | ブラウザ自動操作 |
| Threads | Playwright Cookie | 画像添付対応 |
| Substack | substack.sid Cookie | 公式APIラッパー |
| ComfyUI | なし | localhost:8188 アイキャッチ生成 |

## アーキテクチャ

```
note-publisher/
├── note_publisher/
│   ├── __init__.py
│   ├── client.py          # note.com APIクライアント
│   ├── publish.py         # 記事公開パイプライン
│   ├── distribute.py      # マルチプラットフォーム拡散
│   ├── eyecatch.py        # アイキャッチ生成（ComfyUI連携）
│   └── config.py          # 設定管理
├── skills/
│   ├── x-post.sh          # X投稿
│   ├── threads-post.sh    # Threads投稿
│   └── substack-publish.sh # Substack投稿
├── requirements.txt
├── README.md
└── LICENSE
```

## 注意

- note.comの非公式APIを使用しています。利用規約の範囲内でご利用ください。
- Cookieは約90日で期限切れになります。再取得が必要です。
- レート制限に注意（過剰なリクエストはアカウント停止のリスクがあります）

## License

MIT
