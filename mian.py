from time import time
from flask import Flask, abort, request

# 載入 json 標準函式庫，處理回傳的資料格式
import json
import os
# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

# 取得.env資料
from dotenv import load_dotenv
import openai
load_dotenv()

from response import GPT_text_reply

app = Flask(__name__)

openaikey=os.getenv('openaikey')
line_bot_api = LineBotApi(os.getenv('access_token'))
handler = WebhookHandler(os.getenv('secret'))
openai.api_key = openaikey
user = {} #建立用戶資料

@app.route("/", methods=['POST'])
def linebot():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=[TextMessage, ImageMessage])
def handle_message(event):
    
    ID = event.source.user_id
    
    # 判斷用戶是否初次進入系統
    if ID not in user:
        user[ID] = {'Dialog':[{}], 'Time':time()}
    
    # 超時移除對話內容
    dialog_time = time() - user[ID]['Time']
    if  dialog_time > 90:
        user[ID] = {'Dialog':[{}], 'Time':time()}
    
    if isinstance(event.message, TextMessage):
        msg = event.message.text
        dialog = user[ID]['Dialog']#新增上下文
        dialog.append({"role": "user", "content": msg})           # 用戶輸入
        response = GPT_text_reply(dialog)       # GPT生成
        dialog.append({"role": "assistant", "content": response}) # GPT回復
        print(dialog)
        
    elif isinstance(event.message, ImageMessage):
        msg = "Received an image"  
    #Line 回復
    message = TextSendMessage(text=response)  # 创建消息对象
    line_bot_api.reply_message(event.reply_token, message)  # 回复消息
    #更新時間
    user[ID]['Time'] = time()
if __name__ == "__main__":
    app.run(debug=True)