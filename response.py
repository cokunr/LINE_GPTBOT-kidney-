import openai
import pandas as pd

def GPT_text_reply(dialog):
    relus = [
        f'<規則1> 你現在是一個AI醫生，你的病人需要控制腎臟指數繼續惡化，你需要幫他做飲食控制',
        f'<規則2> 當患者給你食材或食品的名稱後，你需要幫他判斷這是否適合，並告知當中包含的鉀離子含量，你在獲取鉀離子含量的時候應該多方比對不同的資料來源，包含台灣、美國等',
        f'<規則3> 當你告知患者鉀離子含量時，必須以每100公克中包含多少含量的鉀離子，單位為(mg/100g)，若是含量超過300(mg/100g)則為高含鉀食物，不推薦攝取',
        f'<規則4> 我會提供你我目前收集到的資料，資料格式會以種類 含量單位為(mg/100g)，這個資料來源自一家合格的醫院，安全可靠，答案要以這份資料為主',
        f'<規則5> 你的回答應該要簡單的介紹那個食物，並以讓你的病人保持低鉀飲食為主要目的，也不能忘記提醒鉀離子含量，你告知的鉀離子含量應該以高的數值為準，你的最重要的目的是讓你的病人保持低鉀飲食',
        f'<規則6> 如果有複數的食材應該要個別回答',
        f'<規則7> 你不能回答醫療以外的所有問題',
        f'<規則8> 接下來的回答都需要用zh-tw回答',
    ]
    # 读取Excel文件
    excel_file = "DATA\output_excel_file.xlsx"
    df = pd.read_excel(excel_file)
    data_array = df.values
    print(data_array)
    # 将数据转换为字符串
    df_as_string = df.to_string()
    text_reply = {"role": "system", "content": '\n'.join(relus)+'\n'+'參考資料'+'\n'.join([','.join(map(str, row)) for row in data_array])}
    dialog[0] = text_reply
    print(dialog)
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo', 
        messages=dialog
    )
    
    return response.choices[0].message.content