import json
import requests
import pandas as pd

def option_sse_codes_sina(
    symbol: str = "看涨期权",
    trade_date: str = "202202",
    underlying: str = "510050",
) -> pd.DataFrame:
    """
    上海证券交易所-所有看涨和看跌合约的代码

    :param symbol: choice of {"看涨期权", "看跌期权"}
    :type symbol: str
    :param trade_date: 期权到期月份
    :type trade_date: "202002"
    :param underlying: 标的产品代码 华夏上证 50ETF: 510050 or 华泰柏瑞沪深 300ETF: 510300
    :type underlying: str
    :return: 看涨看跌合约的代码
    :rtype: Tuple[List, List]
    """
    if symbol == "看涨期权":
        url = "".join(
            [
                "https://hq.sinajs.cn/list=OP_UP_",
                underlying,
                str(trade_date)[-4:],
            ]
        )
    else:
        url = "".join(
            [
                "https://hq.sinajs.cn/list=OP_DOWN_",
                underlying,
                str(trade_date)[-4:],
            ]
        )
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "hq.sinajs.cn",
        "Pragma": "no-cache",
        "Referer": "https://stock.finance.sina.com.cn/",
        "sec-ch-ua": '"Not.A/Brand";v="99", "Google Chrome";v="132", "Chromium";v="132"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Sec-Fetch-Dest": "script",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    }
    r = requests.get(url, headers=headers)
    data_text = r.text
    data_temp = data_text.replace('"', ",").split(",")
    temp_list = [i[7:] for i in data_temp if i.startswith("CON_OP_")]
    temp_df = pd.DataFrame(temp_list)
    temp_df.reset_index(inplace=True)
    temp_df["index"] = temp_df.index + 1
    temp_df.columns = [
        "序号",
        "期权代码",
    ]
    return temp_df

if __name__ == '__main__':
    underlying_list = ['202502','202503','202506','202509']
    etf_data = pd.DataFrame({
        'stock_code': ['510050', '159919', '510300', '159901', '588080', '588000', '159915', '510500', '159922']
    })

    for option_month in underlying_list:
        option_code_list = []
        for index, row in etf_data.iterrows():
            # 获取看涨期权代码
            option_sse_codes_sina_df = option_sse_codes_sina(symbol="看涨期权", trade_date=option_month, underlying=row['stock_code'])
            option_code_list.extend(list(option_sse_codes_sina_df['期权代码']))

            # 获取看跌期权代码
            option_sse_codes_sina_df = option_sse_codes_sina(symbol="看跌期权", trade_date=option_month, underlying=row['stock_code'])
            option_code_list.extend(list(option_sse_codes_sina_df['期权代码']))
        print(option_code_list)