import os
from google import genai
from http.server import BaseHTTPRequestHandler
import json
import urllib.parse
from urllib.parse import quote

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        api_key = os.environ.get("GOOGLE_API_KEY")
        print(api_key)
        path = self.path
        query = path.split('?')[-1]
        params = urllib.parse.parse_qs(query)
        content = params.get("content", [""])[0]
        print(f"未解谜--content: {content}")
        if content is not None:
            content = quote(content, safe='')
        print(f"解谜--content: {content}")
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            "id": 0,
            "summary": content
        }).encode('utf-8'))
        return