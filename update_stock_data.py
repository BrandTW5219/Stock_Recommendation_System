import yfinance as yf
import datetime
import os
import pandas as pd

def get_stock_names_by_category(category: str="[預設]") -> list[str]:
    df = pd.read_csv("category.csv")
    result = []
    
    if category == "[預設]":
        for x, data in enumerate(df['Category']):
            stock_names = df['Stock Codes'].iloc[x]
            stock_names: str
            stock_names = stock_names.split(' ')
            stock_names: list[str]
            result.extend(stock_names)
    else:
        index = 0
        for x, data in enumerate(df['Category']):
            if data == category:
                index = x
                break
        
        stock_names = df['Stock Codes'].iloc[index]
        stock_names: str
        result = stock_names.split(' ')
    
    return result

def get_stock_data(stock_name: str, start_date: datetime.datetime, end_date: datetime.datetime) -> pd.DataFrame:
    # 使用yfinance套件取得股票資料
    df = yf.download(stock_name, start=start_date, end=end_date, progress=False)
    df: pd.DataFrame
    df = df.reset_index()
    return df

def get_df_subset(df: pd.DataFrame) -> pd.DataFrame:
    # 選擇只包含Date、Close、High和Low欄位的子集
    df_subset = round(df[['Date', 'Close', 'High', 'Low']], 2)

    return df_subset

def save_data_to_csv(path: str, data: pd.DataFrame):
    # 如果指定的檔案路徑不存在，則先創建資料夾
    output_folder = os.path.dirname(path)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 將子集保存為CSV檔案
    data.to_csv(path, index=False)

def update_stock_data(stock_name: str):
    output_file_path = f'.\StockData\{stock_name}.csv'

    #從 last_saved_date 開始更新資料
    last_saved_date = datetime.datetime(2023, 1, 1)
    existing_data = None
    if os.path.exists(output_file_path):
        existing_data = pd.read_csv(output_file_path)
        try:
            # 若資料為空會發生錯誤
            last_saved_date = pd.to_datetime(existing_data['Date'].iloc[-1])
        except:
            print(f"{output_file_path} is empty")

    current_time = datetime.datetime.now()
    # 判斷資料是否更新至最新
    if current_time.date() == last_saved_date.date():
        print(f"{stock_name} have been updated")
        return

    if existing_data is not None:
        last_saved_date += datetime.timedelta(days=1)

    new_data = get_stock_data(stock_name, last_saved_date, current_time)
    new_data = get_df_subset(new_data)
    # 合併舊資料
    if existing_data is not None:
        new_data = pd.concat([existing_data, new_data], ignore_index=True)

    try:
        # 用來測試資料是否為空
        # 若是則跳到 except
        pd.to_datetime(new_data['Date'].iloc[-1])

        # 只保留年月日
        # 去掉時分秒
        new_data['Date'] = pd.to_datetime(new_data['Date']).dt.date
        # 刪除日期重複的資料
        new_data.drop_duplicates(subset=['Date'], keep='last', inplace=True)

        save_data_to_csv(output_file_path, new_data)
        print(f"Data for {stock_name} updated successfully.")
    except:
        try:
            os.remove(output_file_path)
        except:
            pass

if __name__ == '__main__':
    stock_names = get_stock_names_by_category()
    for stock_name in stock_names:
        update_stock_data(stock_name)
