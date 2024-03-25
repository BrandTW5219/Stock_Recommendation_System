import numpy as np
import pandas as pd
import talib
import pandas as pd


class MATSClass():
    def __init__(self):
        pass

    # MA_Strategy
    def tradingStrategy(self, stock_name: str, stop_loss: float, days: int):
        file_path = f".\StockData\{stock_name}.csv"
        df = pd.read_csv(file_path)[-days:].reset_index()
        
        # 利用talib計算移動平均線，並畫出5、10、20MA圖
        closePrices = df['Close']  # 收盤價
        close_sma_5 = np.round(talib.SMA(closePrices, timeperiod=5), 2)
        close_sma_10 = np.round(talib.SMA(closePrices, timeperiod=10), 2)
        close_sma_20 = np.round(talib.SMA(closePrices, timeperiod=20), 2)
        
        # 設定交易所需要用的變數
        flage = 0  # 判斷目前是否有持股
        buyPrice = 0
        sellPrice = 0
        culReturn = 0  # 第k次交易之累計報酬
        tax = 0  # 交易成本
        # ====================

        # 買賣策略設定與交易
        for x in range(19, len(closePrices)):  # 每一個交易天
            if flage == 0:  # 狀態: 未持有股票
                # 多頭排列成立
                if close_sma_5[x] > close_sma_10[x] and close_sma_10[x] > close_sma_20[x]:
                    buyPrice = closePrices[x]  # 儲存買進價格
                    tax = tax + buyPrice * 0.001425  # 儲存買進手續費
                    flage = 1  # 更新狀態
            if flage == 1:  # 狀態，持有股票
                sellPrice = closePrices[x]
                if close_sma_5[x] < close_sma_10[x] and close_sma_10[x] < close_sma_20[x]:  # 空頭排列成立
                    # if close_sma_5[x] < close_sma_20[x]:#空頭排列成立
                    tax = tax + sellPrice * 0.001425 + sellPrice * 0.003  # 計算交易成本
                    flage = 0  # 更新成未持有股票
                    culReturn = culReturn + (sellPrice - buyPrice) - tax  # 計算累計獲利
                    tax = 0  # 完成交易, 成本變數歸零
            if stop_loss > 0 and flage == 1:
                if (sellPrice - buyPrice - tax) / buyPrice < -stop_loss:  # 停損條件成立
                    flage = 0
                    culReturn = culReturn + (sellPrice - buyPrice) - tax
                    tax = 0  # 完成交易, 成本變數歸零
        return culReturn / df['Close'].iloc[-1]  # 回傳最後的累計報酬，單位是幾”元”
