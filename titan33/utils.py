import akshare as ak



stck_list = []
def get_cmv_less_than_billions(billionsm):
    # 获取所有A股股票列表
    try:
        stock_list = ak.stock_zh_a_spot_em()
        print(stock_list)
    except Exception as e:
        print(f"获取股票列表失败: {e}")
        return
    
    # 获取流通市值数据并过滤
    try:
        filtered_stocks = stock_list[
            (stock_list['流通市值'] < billionsm * 1e8) & 
            (~stock_list['名称'].str.contains('ST')) & 
            (~stock_list['名称'].str.contains('ST*')) 
        ]
    except Exception as e:
        print(f"过滤股票失败: {e}")
        return
    
    # 打印符合条件的股票代码和名称
    for index, row in filtered_stocks.iterrows():
        ts_code = row['代码']
        name = row['名称']
        print(f"符合条件的股票: {ts_code}, 名称: {name}")
        if ts_code.startswith('6'):
            stck_list.append(ts_code + ".SH")
        else:
            stck_list.append(ts_code + ".SZ")

    return stck_list
if __name__ == "__main__":
    tck = get_cmv_less_than_billions(50)
    print(tck)
    print(len(tck))