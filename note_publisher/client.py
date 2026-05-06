"""note.com API client"""
import requests, json, re

class NoteClient:
    def __init__(self, cookie: str, user_agent: str = "Mozilla/5.0"):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": user_agent,
            "X-Requested-With": "XMLHttpRequest",
            "Cookie": f"_note_session_v5={cookie}" if not cookie.startswith("_note") else cookie
        })
    
    def create_note(self) -> dict:
        r = self.session.post("https://note.com/api/v1/text_notes", json={"template_key": None})
        d = r.json()
        return {"id": d["data"]["id"], "key": d["data"]["key"]}
    
    def upload_eyecatch(self, note_id: str, image_path: str) -> str:
        with open(image_path, "rb") as f:
            r = self.session.post(
                "https://note.com/api/v1/image_upload/note_eyecatch",
                headers={"X-Note-Id": str(note_id)},
                files={"file": ("eyecatch.png", f, "image/png")},
                data={"width": "1280", "height": "672", "note_id": str(note_id)}
            )
        return r.json().get("data", {}).get("url", "")
    
    def publish(self, note_id: str, title: str, body: str, hashtags: list[str] = None) -> str:
        self.session.post(
            f"https://note.com/api/v1/text_notes/draft_save?id={note_id}&is_temp_saved=true",
            json={"body": body, "body_length": len(body), "name": title, "index": True, "is_lead_form": False}
        )
        r = self.session.put(
            f"https://note.com/api/v1/text_notes/{note_id}",
            json={
                "name": title, "free_body": body, "status": "published",
                "price": 0, "index": True,
                "hashtags": hashtags or [],
                "body_length": len(body), "send_notifications_flag": False
            }
        )
        return r.json()["data"]["key"]
    
    def get_article(self, note_key: str) -> dict:
        r = self.session.get(f"https://note.com/api/v3/notes/{note_key}/")
        data = r.json()["data"]
        return {"title": data["name"], "eyecatch": data.get("eyecatch", ""), "body": data.get("body", ""), "url": f"https://note.com/famous_prawn2009/n/{note_key}"}
