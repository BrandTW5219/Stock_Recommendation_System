import pandas as pd
import talib

class KDTSClass():
    def __init__(self):
        pass

    def tradingStrategy(self, stock_name: str, stop_loss: float, days: int):
        file_path = f".\StockData\{stock_name}.csv"
        df = pd.read_csv(file_path)[-days:].reset_index()

        closePrices = df['Close']
        slowK, slowD = talib.STOCH(
            df["High"],
            df["Low"],
            df["Close"],
            fastk_period = 9,
            slowk_period = 3,
            slowd_period = 3
        )
        df["SlowK"] = slowK
        df["SlowD"] = slowD
        
        flage = 0
        buyPrice = 0
        sellPrice = 0
        culReturn = 0
        tax = 0
        # BACKTESTING FOR KD STRATEGY
        for x in range(9, len(closePrices)):
            if flage == 0:
                if slowK[x] > slowD[x] and slowK[x-1] < slowD[x-1]:
                    buyPrice = closePrices[x]
                    tax = tax + buyPrice * 0.001425
                    flage = 1
            if flage == 1:
                sellPrice = closePrices[x]
                if slowK[x] < slowD[x] and slowK[x-1] > slowD[x-1]:
                    tax = tax + buyPrice * 0.001425 + sellPrice * 0.003
                    flage = 0
                    culReturn += (sellPrice - buyPrice - tax)
                    tax = 0
            if stop_loss > 0 and flage == 1:
                if(sellPrice - buyPrice - tax) / buyPrice < -stop_loss:
                    flage = 0
                    culReturn += (sellPrice - buyPrice - tax)
                    tax = 0
        return culReturn / df['Close'].iloc[-1]
