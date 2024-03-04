import pandas as pd

# 讀取 Excel 檔案
df = pd.read_excel('DATA\未處理資料.xlsx')

# 檢查 DataFrame 的資料結構
print("原始資料:")
print(df)

# 將相同標題的列整合到一起
new_df = pd.DataFrame(columns=["名稱", "含量"])

current_title = None
current_row = {}
for index, row in df.iterrows():
    for column in df.columns:
        if "名稱" in column:  # 找到標題列
            if pd.isna(row[column]):  # 如果名稱為 NaN，則跳過這一行
                break
            if current_title:  # 如果已經有標題列被處理過
                new_df = new_df.append(current_row, ignore_index=True)  # 將該標題列添加到新的 DataFrame 中
            current_title = row[column]  # 更新當前標題
            current_row = {"名稱": current_title}  # 初始化新的列
        else:
            current_row["含量"] = row[column]  # 添加含量

# 將最後一個標題列添加到新的 DataFrame 中
new_df = new_df.append(current_row, ignore_index=True)

print("\n整合後的資料:")
print(new_df)
new_df.to_excel("DATA\output_excel_file.xlsx", index=False)

result_string = new_df.to_string(index=False)

print("\n轉換為字串:")
print(result_string)