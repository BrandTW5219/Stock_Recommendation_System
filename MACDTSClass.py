import talib
import pandas as pd

class MACDTSClass:
    def __init__(self):
        pass

    def tradingStrategy(self, stock_name: str, stop_loss: float, days: int):
        file_path = f".\StockData\{stock_name}.csv"
        df = pd.read_csv(file_path)[-days:].reset_index()

        # 計算 MACD 指標
        df['macd'], df['signal'], _ = talib.MACD(
            df['Close'],
            fastperiod=12,
            slowperiod=26,
            signalperiod=9
        )

        # 設定交易所需要用的變數
        flage = 0  # 判斷目前是否有持股
        buyPrice = 0
        sellPrice = 0
        culReturn = 0  # 第k次交易之累計報酬
        tax = 0  # 交易成本

        # 買賣策略設定與交易
        for x in range(1, len(df)):  
            if flage == 0:  # 狀態: 未持有股票
                # MACD 黃金交叉
                if df['macd'][x] > df['signal'][x] and df['macd'][x-1] <= df['signal'][x-1]:
                    buyPrice = df['Close'][x]  # 儲存買進價格
                    tax = tax + buyPrice * 0.001425  # 儲存買進手續費
                    flage = 1  # 更新狀態
            if flage == 1:  # 狀態，持有股票
                # MACD 死亡交叉或停損
                if df['macd'][x] < df['signal'][x] or ((buyPrice - df['Close'][x]) / buyPrice) > stop_loss:
                    sellPrice = df['Close'][x]
                    tax = tax + sellPrice * 0.001425 + sellPrice * 0.003  # 計算交易成本
                    flage = 0  # 更新成未持有股票
                    culReturn = culReturn + (sellPrice - buyPrice) - tax  # 計算累計獲利
                    tax = 0  # 完成交易, 成本變數歸零

        return culReturn / df['Close'].iloc[-1]
