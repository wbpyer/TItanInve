import warnings
import sys
warnings.filterwarnings("ignore")
sys.path.append('./Ru2h-Meta')
import pandas as pd 


from meta import config 
from meta.data_processor import DataProcessor 
# from main import check_and_make_directories 
from meta.data_processors.tushare import Tushare, ReturnPlotter 
from meta.env_stock_trading.env_stocktrading_China_A_shares import StockTradingEnv 
from agents.stablebaselines3_models import DRLAgent 
import os 
from typing import List 
from argparse import ArgumentParser 
from meta import config 
from meta.config_tickers import DOW_30_TICKER 
from meta.config import ( DATA_SAVE_DIR, TRAINED_MODEL_DIR, TENSORBOARD_LOG_DIR, RESULTS_DIR, INDICATORS, TRAIN_START_DATE, TRAIN_END_DATE, TEST_START_DATE, TEST_END_DATE, TRADE_START_DATE, TRADE_END_DATE, ERL_PARAMS, RLlib_PARAMS, SAC_PARAMS, ALPACA_API_KEY, ALPACA_API_SECRET, ALPACA_API_BASE_URL, )

import pyfolio
from pyfolio import timeseries

pd.options.display.max_columns = None

print("ALL Modules have been imported!")


import os

''' 
use check_and_make_directories() to replace the following

if not os.path.exists("./datasets"): 
  os.makedirs("./datasets") 
if not os.path.exists("./trained_models"): 
  os.makedirs("./trained_models") 
if not os.path.exists("./tensorboard_log"): 
  os.makedirs("./tensorboard_log") 
if not os.path.exists("./results"): 
  os.makedirs("./results") 
'''


def check_and_make_directories(directories: List[str]):
    for directory in directories:
        if not os.path.exists("./" + directory):
            os.makedirs("./" + directory)


check_and_make_directories([DATA_SAVE_DIR, TRAINED_MODEL_DIR, TENSORBOARD_LOG_DIR, RESULTS_DIR])


ticker_list = ['600243.SH', '688365.SH', '831906.SZ', '301622.SZ', '920098.SZ', '838670.SZ', '002193.SZ', '002633.SZ', '603825.SH', '870726.SZ', '834407.SZ'] 
#ticker_list = ['600243.SH', '688365.SH', '831906.SZ', '301622.SZ', '920098.SZ', '838670.SZ', '002193.SZ', '002633.SZ', '603825.SH', '870726.SZ', '834407.SZ']

TRAIN_START_DATE = '2022-01-01' 
TRAIN_END_DATE= '2022-08-01' 
TRADE_START_DATE = '2022-08-02' 
TRADE_END_DATE = '2022-12-03'

TIME_INTERVAL = "1d" 
kwargs = {} 
kwargs['token'] = '27080ec403c0218f96f388bca1b1d85329d563c91a43672239619ef5' 
p = DataProcessor(data_source='tushare', start_date=TRAIN_START_DATE, end_date=TRADE_END_DATE, time_interval=TIME_INTERVAL, **kwargs)


# download data
p.download_data(ticker_list=ticker_list)
p.clean_data()
p.fillna()


# download indicator
p.add_technical_indicator(config.INDICATORS) 
p.fillna()


#print(f"p.dataframe: {p.dataframe}")
train = p.data_split(p.dataframe, TRAIN_START_DATE, TRAIN_END_DATE) 
print(f"len(train.tic.unique()): {len(train.tic.unique())}")
print(f"train.tic.unique(): {train.tic.unique()}")
print(f"train.head(): {train.head()}")
print(f"train.shape: {train.shape}")


#  Data Preprocessing
stock_dimension = len(train.tic.unique()) 
state_space = stock_dimension * (len(config.INDICATORS) + 2) + 1 
print(f"Stock Dimension: {stock_dimension}, State Space: {state_space}")
train = train.rename(columns={'time':'date'})
print(train.head())


# build env
env_kwargs = { "stock_dim": stock_dimension, "hmax": 1000, "initial_amount": 1000000, "buy_cost_pct": 6.87e-5, "sell_cost_pct": 1.0687e-3, "reward_scaling": 1e-4, "state_space": state_space, "action_space": stock_dimension, "tech_indicator_list": config.INDICATORS, "print_verbosity": 1, "initial_buy": True, "hundred_each_trade": True }

e_train_gym = StockTradingEnv(df=train, **env_kwargs)   
env_train, _ = e_train_gym.get_sb_env() 
print(f"print(type(env_train)): {print(type(env_train))}")



# train
agent = DRLAgent(env=env_train) 
DDPG_PARAMS = { "batch_size": 256, "buffer_size": 50000, "learning_rate": 0.0005, "action_noise": "normal", } 
POLICY_KWARGS = dict(net_arch=dict(pi=[64, 64], qf=[400, 300])) 
model_ddpg = agent.get_model("ddpg", model_kwargs=DDPG_PARAMS, policy_kwargs=POLICY_KWARGS)
trained_ddpg = agent.train_model(model=model_ddpg, tb_log_name='ddpg', total_timesteps=10000)



agent = DRLAgent(env=env_train) 
model_a2c = agent.get_model("a2c")
trained_a2c = agent.train_model(model=model_a2c, tb_log_name='a2c', total_timesteps=50000)


# trade
trade = p.data_split(p.dataframe, TRADE_START_DATE, TRADE_END_DATE) 
trade.head()
trade.rename(columns={'time':'date'},inplace=True)
trade.head()



env_kwargs = { "stock_dim": stock_dimension, "hmax": 1000, "initial_amount": 1000000, "buy_cost_pct": 6.87e-5, "sell_cost_pct": 1.0687e-3, "reward_scaling": 1e-4, "state_space": state_space, "action_space": stock_dimension, "tech_indicator_list": config.INDICATORS, "print_verbosity": 1, "initial_buy": False, "hundred_each_trade": True } 
e_trade_gym = StockTradingEnv(df=trade, **env_kwargs)




df_account_value_ddpg, df_actions_ddpg = DRLAgent.DRL_prediction(model=trained_ddpg, environment=e_trade_gym)
df_actions_ddpg.to_csv("action_ddpg.csv", index=False) 
print(f"df_actions_ddpg: {df_actions_ddpg}")
df_account_value_ddpg.head(133)
df_account_value_ddpg.loc[103] = ["2020-01-03 00:00:00",1.226122e+06]
df_account_value_ddpg.tail()
df_account_value_ddpg.rename(columns={'date':'time'},inplace=True)




df_account_value_a2c, df_actions_a2c = DRLAgent.DRL_prediction(model=trained_a2c, environment=e_trade_gym)
df_actions_a2c.to_csv("action_a2c.csv", index=False) 
print(f"df_actions_a2c: {df_actions_a2c}")
df_account_value_a2c.head(133)
df_account_value_a2c.loc[103] = ["2020-01-03 00:00:00",1.226122e+06]
df_account_value_a2c.tail()
df_account_value_a2c.rename(columns={'date':'time'},inplace=True)




trade.rename(columns={'date':'time'},inplace=True)




plotter = ReturnPlotter(df_account_value_ddpg, trade, TRADE_START_DATE, TRADE_END_DATE)
plotter.plot("DDPG", "green")


plotter = ReturnPlotter(df_account_value_a2c, trade, TRADE_START_DATE, TRADE_END_DATE)
plotter.plot("A2C", "red")


plotter.plot("000016", "black")
# baseline_df = plotter.get_baseline("399300")


daily_return = plotter.get_return(df_account_value_ddpg)
# daily_return_base = plotter.get_return(baseline_df, value_col_name="close")

perf_func = timeseries.perf_stats 
# perf_stats_all = perf_func(returns=daily_return, factor_returns=daily_return_base, positions=None, transactions=None, turnover_denom="AGB")
perf_stats_all = perf_func(returns=daily_return)
print("==============DDPG Strategy Stats===========")
print(f"perf_stats_all: {perf_stats_all}")





daily_return = plotter.get_return(df_account_value_a2c)
# daily_return_base = plotter.get_return(baseline_df, value_col_name="close")

perf_func = timeseries.perf_stats 
# perf_stats_all = perf_func(returns=daily_return, factor_returns=daily_return_base, positions=None, transactions=None, turnover_denom="AGB")
perf_stats_all = perf_func(returns=daily_return)
print("==============A2C Strategy Stats===========")
print(f"perf_stats_all: {perf_stats_all}")




# daily_return = plotter.get_return(df_account_value)
# daily_return_base = plotter.get_return(baseline_df, value_col_name="close")

# perf_func = timeseries.perf_stats
# perf_stats_all = perf_func(returns=daily_return_base, factor_returns=daily_return_base, positions=None, transactions=None, turnover_denom="AGB")

# print("==============Baseline Strategy Stats===========")

# print(f"perf_stats_all: {perf_stats_all}")

