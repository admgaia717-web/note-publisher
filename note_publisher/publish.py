"""note publishing pipeline"""
from .client import NoteClient

class NotePublisher:
    def __init__(self, cookie: str):
        self.client = NoteClient(cookie)
    
    def publish(self, title: str, body: str, eyecatch_path: str = None, hashtags: list[str] = None) -> dict:
        note = self.client.create_note()
        if eyecatch_path:
            self.client.upload_eyecatch(note["id"], eyecatch_path)
        key = self.client.publish(note["id"], title, body, hashtags)
        return {"key": key, "url": f"https://note.com/famous_prawn2009/n/{key}"}
