from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

BOT_TOKEN = '7832637217:AAHzcSY3gxF_QhFfAfHiQWanDmO8aQZLOik'
CHAT_ID = '1288443359'

HTML_FORM = """
<!doctype html>
<title>Upload File ke Telegram</title>
<h1>Upload File</h1>
<form action="/" method="post" enctype="multipart/form-data">
  <input type="file" name="file">
  <input type="submit" value="Upload">
</form>
{result}
"""

def get_download_link(file_id):
    info_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
    file_info = requests.get(info_url).json()
    file_path = file_info['result']['file_path']
    return f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

@app.get("/", response_class=HTMLResponse)
def form():
    return HTML_FORM.format(result="")

@app.post("/", response_class=HTMLResponse)
async def upload(file: UploadFile = File(...)):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendDocument'
    files = {'document': (file.filename, await file.read())}
    data = {'chat_id': CHAT_ID}
    response = requests.post(url, files=files, data=data).json()
    
    if 'result' in response:
        file_id = response['result']['document']['file_id']
        download_url = get_download_link(file_id)
        result = f"<p>File berhasil diupload! <a href='{download_url}' target='_blank'>Download di sini</a></p>"
    else:
        result = "<p>Gagal mengupload file.</p>"
    
    return HTML_FORM.format(result=result)
