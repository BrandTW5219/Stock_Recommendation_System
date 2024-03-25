import tkinter as tk
from tkinter import ttk
import threading
import pandas as pd
import os
import twstock

from update_stock_data import get_stock_names_by_category
from update_stock_data import update_stock_data

from MATSClass import MATSClass
from MACDTSClass import MACDTSClass
from KDTSClass import KDTSClass
from ROCTSClass import ROCTSClass

class SRS:
    # 使用 run() 叫出視窗

    def __init__(self):
        self.root = None
        self.init_root()

        self.titleLabel = None
        self.categoryLabel = None
        self.categoryBox = None
        self.budgetLabel = None
        self.budgetEntry = None
        self.budgetVal = None
        self.stoplossLabel = None
        self.stoplossEntry = None
        self.stoplossVal = None
        self.daysLabel = None
        self.daysEntry = None
        self.daysVal = None
        self.budgetButton = None
        self.categoryValueLabel = None
        self.budgetStateLabel = None
        self.stoplossStateLabel = None
        self.daysStateLabel = None
        self.stateLabel = None
        self.resultLabel = None
        self.init_ui()
    
    def init_root(self):
        self.root = tk.Tk()
        self.root.title('股票推薦系統 SRS')
        self.root.geometry("360x640")
    
    def run(self):
        self.root.mainloop()

    def init_ui(self):
        self.init_titleLabel()
        self.init_categoryLabel()
        self.init_categoryBox()
        self.init_budgetLabel()
        self.init_budgetEntry()
        self.init_stoplossLabel()
        self.init_stoplossEntry()
        self.init_daysLabel()
        self.init_daysEntry()
        self.init_budgetButton()
        self.init_categoryValueLabel()
        self.init_budgetStateLabel()
        self.init_stoplossStateLabel()
        self.init_daysStateLabel()
        self.init_stateLabel()
        self.init_resultLabel()
    
    def init_titleLabel(self):
        self.titleLabel = ttk.Label(self.root, text="歡迎使用股票推薦系統", font=("Arial", 12, "bold"))
        self.titleLabel.pack(pady=5)

    def init_categoryLabel(self):
        self.categoryLabel = ttk.Label(self.root, text="請選擇股票類別 (產業)", font=("Arial", 10))
        self.categoryLabel.pack(pady=3)

    def init_categoryBox(self):
        category_list = ["[預設]"]
        df = pd.read_csv("category.csv")
        categorys = df['Category'].to_list()
        category_list.extend(categorys)

        self.categoryBox = ttk.Combobox(self.root, state="readonly", values=category_list)
        self.categoryBox.pack(pady=3)
        self.categoryBox.set("[預設]")
    
    def init_budgetLabel(self):
        self.budgetLabel = ttk.Label(self.root, text="請輸入預算金額 (元/股)", font=("Arial", 10))
        self.budgetLabel.pack(pady=3)

    def init_budgetEntry(self):
        self.budgetVal = tk.StringVar()

        self.budgetEntry = tk.Entry(self.root, textvariable=self.budgetVal)
        self.budgetEntry.pack(pady=3)

    def init_stoplossLabel(self):
        self.stoplossLabel = ttk.Label(self.root, text="請輸入交易停損點 (%)", font=("Arial",10))
        self.stoplossLabel.pack(pady=3)

    def init_stoplossEntry(self):
        self.stoplossVal = tk.StringVar()

        self.stoplossEntry = tk.Entry(self.root, textvariable=self.stoplossVal)
        self.stoplossEntry.pack(pady=3)

    def init_daysLabel(self):
        self.daysLabel = ttk.Label(self.root, text="請輸入分析歷史資料量 (天數)", font=("Arial", 10))
        self.daysLabel.pack(pady=3)

    def init_daysEntry(self):
        self.daysVal = tk.StringVar()

        self.daysEntry = tk.Entry(self.root, textvariable=self.daysVal)
        self.daysEntry.pack(pady=3)
    
    def init_budgetButton(self):
        self.budgetButton = tk.Button(self.root, text="分析", bg="lightgreen", command=self.checkBudget)
        self.budgetButton.pack(pady=3)

    def init_categoryValueLabel(self):
        self.categoryValueLabel = tk.Label(self.root, text="", fg="red", font=("Arial", 10))
        self.categoryValueLabel.pack(pady=3)

    def init_budgetStateLabel(self):
        self.budgetStateLabel = tk.Label(self.root, text="", fg="red", font=("Arial", 10))
        self.budgetStateLabel.pack(pady=3)

    def init_stoplossStateLabel(self):
        self.stoplossStateLabel = tk.Label(self.root, text="", fg="red", font=("Arial",10))
        self.stoplossStateLabel.pack(pady=3)

    def init_daysStateLabel(self):
        self.daysStateLabel = tk.Label(self.root, text="", fg="red", font=("Arial",10))
        self.daysStateLabel.pack(pady=3)
    
    def init_stateLabel(self):
        self.stateLabel = tk.Label(self.root, text="", fg="blue", font=("Arial", 12))
        self.stateLabel.pack(pady=3)

    def init_resultLabel(self):
        self.resultLabel = tk.Label(self.root, text="", fg="red", font=("Arial,10"))
        self.resultLabel.pack(pady=3)

    def run_sub_thread(self):
        class StockNamesObj:
            def __init__(self):
                self.stock_names = None

        def update_stock_datas():
            self.stateLabel.config(text = "正在更新資料...")
            category = self.categoryBox.get()
            stock_names = get_stock_names_by_category(category)
            for index, stock_name in enumerate(stock_names):
                update_stock_data(stock_name)
                self.stateLabel.config(text=f"正在更新資料...{int(100.0 * index / len(stock_names))}%")
            self.stateLabel.config(text="")
        
        def get_stock_names_by_preference(stock_names_obj: StockNamesObj):
            self.stateLabel.config(text = "正在篩選資料...")
            category = self.categoryBox.get()
            stock_names_obj.stock_names = get_stock_names_by_category(category)
            target_price = float(self.budgetVal.get())
            target_stock_names = []
            for stock_name in stock_names_obj.stock_names:
                file_path = f".\StockData\{stock_name}.csv"
                if os.path.exists(file_path):
                    last_close_price = float(pd.read_csv(file_path)['Close'].iloc[-1])
                    if last_close_price <= target_price:
                        target_stock_names.append(stock_name)
            stock_names_obj.stock_names = target_stock_names
            self.stateLabel.config(text="")

        self.budgetButton.config(state="disabled")

        sub_thread = threading.Thread(target=update_stock_datas, daemon=True)
        sub_thread.start()
        sub_thread.join()

        stock_names_obj = StockNamesObj()
        sub_thread = threading.Thread(target=get_stock_names_by_preference, daemon=True, args=(stock_names_obj,))
        sub_thread.start()
        sub_thread.join()

        # 計算指標
        self.stateLabel.config(text="正在計算指標...")
        stock_names = stock_names_obj.stock_names
        results = {}
        the_best_stock_name = None
        max_val = -9999
        use_strategy = None

        strategys = {}
        strategys['MA'] = MATSClass()
        strategys['MACD'] = MACDTSClass()
        strategys['KD'] = KDTSClass()
        strategys['ROC'] = ROCTSClass()
        strategys_keys = strategys.keys()

        days = int(self.daysVal.get())
        stop_loss = int(self.stoplossVal.get()) / 100.0
        for index, stock_name in enumerate(stock_names):
            results[stock_name] = {}

            for key in strategys_keys:
                results[stock_name][key] = strategys[key].tradingStrategy(
                    stock_name,
                    stop_loss,
                    days
                )
                if results[stock_name][key] > max_val:
                    max_val = results[stock_name][key]
                    the_best_stock_name = stock_name
                    use_strategy = key

            self.stateLabel.config(text=f"正在計算指標...{int(100.0 * index / len(stock_names))}%")
        
        if the_best_stock_name:
            chinese_name = twstock.realtime.get(the_best_stock_name.split('.')[0])['info']['name']
            self.stateLabel.config(text="您的推薦結果")
            self.resultLabel.config(text=f"推薦項目 = {chinese_name}({the_best_stock_name}) \n\n使用指標 = {use_strategy} \n\n指標數值 = {round(max_val, 2)}", font=("Bold",12))
        else:
            self.stateLabel.config(text=f"無任何推薦")
            self.resultLabel.config(text="")
        self.budgetButton.config(state="active")

    def checkBudget(self):
        # Category State
        self.categoryValueLabel.config(text = "您選擇的類別 = " + self.categoryBox.get())
        # Budget State
        if self.budgetVal.get().isdigit() and int(self.budgetVal.get()) > 0:
            self.budgetStateLabel.config(text = "您輸入的預算 = " + self.budgetVal.get() + " 元/股")
        else:
            self.budgetStateLabel.config(text = "請重新輸入有效預算 (僅限正整數)")
            self.budgetVal.set("")
            self.resultLabel.config(text = "")
            return
        # Stoploss State
        if self.stoplossVal.get().isdigit() and int(self.stoplossVal.get()) >=0 and int(self.stoplossVal.get()) <= 100:
            self.stoplossStateLabel.config(text = "您輸入的停損點 = " + self.stoplossVal.get() + "%")
        else:
            self.stoplossStateLabel.config(text = "請重新輸入有效停損 (僅限正整數)")
            self.stoplossVal.set("")
            self.resultLabel.config(text = "")
            return
        # Days State
        if self.daysVal.get().isdigit() and int(self.daysVal.get()) >= 50 and int(self.daysVal.get()) <= 200:
            self.daysStateLabel.config(text = "您的分析資料天數 = " + self.daysVal.get() + "天")
        else:
            self.daysStateLabel.config(text = "請重新輸入有效天數 (50至200天)")
            self.daysVal.set("")
            self.resultLabel.config(text = "")
            return
        update_thread = threading.Thread(target=self.run_sub_thread, daemon=True)
        update_thread.start()
        
if __name__ == "__main__":
    SRS().run()
