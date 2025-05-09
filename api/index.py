import os
from google import genai
from http.server import BaseHTTPRequestHandler
from google.genai import types
import json
import urllib.parse
import httpx

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        api_key = os.environ.get("GOOGLE_API_KEY")
        path = self.path
        query = path.split('?')[-1]
        params = urllib.parse.parse_qs(query)
        html_url = params.get("url", [""])[0]
        client = genai.Client(api_key=api_key)
        html_content = httpx.get(html_url).content
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                types.Part.from_bytes(
                    data=html_content,
                    mime_type="text/html",
                ),
                "根据网页内容生成一个摘要"
            ]
        )
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            "id": 0,
            "summary": response.text
        }).encode('utf-8'))
        return