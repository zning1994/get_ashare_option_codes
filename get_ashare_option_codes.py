import sys
import json
import time
import requests
import akshare as ak
import pandas as pd

def option_sse_codes_sina(symbol: str = "看涨期权", trade_date: str = "202202", underlying: str = "510050") -> pd.DataFrame:
    """
    获取上海证券交易所所有看涨和看跌期权合约的代码。

    :param symbol: "看涨期权" 或 "看跌期权"
    :param trade_date: 期权到期月份，格式如 "202002"
    :param underlying: 标的产品代码，如 "510050"
    :return: 包含期权代码的 DataFrame
    """
    url = f"https://hq.sinajs.cn/list={'OP_UP_' if symbol == '看涨期权' else 'OP_DOWN_'}{underlying}{trade_date[-4:]}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "Referer": "https://stock.finance.sina.com.cn/",
    }

    response = requests.get(url, headers=headers)
    data_text = response.text
    data_temp = data_text.replace('"', ',').split(',')
    option_codes = [i[7:] for i in data_temp if i.startswith("CON_OP_")]

    return pd.DataFrame(option_codes, columns=["期权代码"])

if __name__ == '__main__':
    etf_data = pd.DataFrame({
        'stock_code': ['510050', '159919', '510300', '159901', '588080', '588000', '159915', '510500', '159922']
    })
    underlying_list = ak.option_sse_list_sina(symbol="50ETF", exchange="null")

    # 初始化空 DataFrame
    all_options_df = pd.DataFrame(columns=["期权代码", "标的物代码"])

    for option_month in underlying_list:
        for _, row in etf_data.iterrows():
            underlying_code = row['stock_code']

            # 获取看涨期权代码
            call_options_df = option_sse_codes_sina(symbol="看涨期权", trade_date=option_month, underlying=underlying_code)
            call_options_df["标的物代码"] = underlying_code
            print(f"标的物代码 {underlying_code} 的看涨期权已下载完毕")
            time.sleep(0.3)
            
            # 获取看跌期权代码
            put_options_df = option_sse_codes_sina(symbol="看跌期权", trade_date=option_month, underlying=underlying_code)
            put_options_df["标的物代码"] = underlying_code
            print(f"标的物代码 {underlying_code} 的看跌期权已下载完毕")
            time.sleep(0.3)

            # 合并到总 DataFrame
            all_options_df = pd.concat([all_options_df, call_options_df, put_options_df], ignore_index=True)

    # 导出为 JSON 文件
    all_options_json = all_options_df.to_json(orient="records", force_ascii=False, indent=4)
    with open("options.json", "w", encoding="utf-8") as f:
        f.write(all_options_json)

    print("已成功导出期权代码至 options.json")
