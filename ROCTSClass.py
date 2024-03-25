import talib
from pandas_datareader import data
import pandas as pd


class ROCTSClass():
    def __init__(self):
        pass

    # ROC_Strategy
    def tradingStrategy(self, stock_name: str, stop_loss: float, days: int):
        # 取得股價
        file_path = f".\StockData\{stock_name}.csv"
        df = pd.read_csv(file_path)[-days:].reset_index()

        # 利用talib計算ROC
        closePrices = df['Close']  # 收盤價
        ROC_10 = talib.ROC(closePrices, timeperiod=12)

        # 設定交易所需要用的變數
        flage = 0  # 判斷目前是否有持股
        buyPrice = 0
        sellPrice = 0
        culReturn = 0  # 第k次交易之累計報酬
        tax = 0  # 交易成本
        # ====================

        # 買賣策略設定與交易
        for x in range(10, len(closePrices)):  # 每一個交易天
            if flage == 0:  # 狀態: 未持有股票
                if ROC_10[x - 1] < 0 and ROC_10[x] > 0:
                    buyPrice = closePrices[x]
                    tax = tax + buyPrice * 0.001425
                    flage = 1
            if flage == 1:  # 狀態，持有股票
                sellPrice = closePrices[x]
                if ROC_10[x - 1] > 0 and ROC_10[x] < 0:
                    tax = tax + sellPrice * 0.001425 + sellPrice * 0.003
                    flage = 0
                    culReturn = culReturn + (sellPrice - buyPrice) - tax
                    tax = 0
                    if stop_loss > 0 and flage == 1:
                        if (sellPrice - buyPrice - tax) / buyPrice < -stop_loss:
                            flage = 0
                            culReturn = culReturn + (sellPrice - buyPrice) - tax
                            tax = 0
        return culReturn / df['Close'].iloc[-1]  # 回傳最後的累計報酬，單位是幾”元”
