from strategy import FactorStrategy
import pandas as pd

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    '''------------------------Config------------------------------------'''
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 1000)

    heatmap_para = {"window": (5, 375, 10),
                    "threshold": (0, 0.5, 0.025)}

    start_date = "2020-01-01"
    end_date = "2021-12-31"
    start_timestamp = int(pd.Timestamp(start_date).timestamp())
    end_timestamp = int(pd.Timestamp(end_date).timestamp())

    '''-----------------------Strategy Detail------------------------------------'''
    # Initialize the FactorStrategy class
    # metrics_list = ["indicators/mvrv_account_based"]
    # metrics_list = ["derivatives/futures_open_interest_perpetual_sum"] 
    # metrics_list = ["institutions/us_spot_etf_flows_net"]
    # metrics_list = ["derivatives/futures_open_interest_perpetual_sum_all"]
    # metrics_list = ["derivatives/futures_funding_rate_perpetual_all"]
    # metrics_list = ["derivatives/options_25delta_skew_1_week"]
    # metrics_list = ["derivatives/futures_liquidated_volume_long_sum"]
    # metrics_list = ["supply/current"]
    # metrics_list = ["derivatives/futures_estimated_leverage_ratio"]
    # metrics_list = ["addresses/active_count"]
    # metrics_list = ["market/price_usd_close"]
    # metrics_list = ["transactions/count"]
    # metrics_list = ["addresses/min_100_count"]
    # metrics_list = ["derivatives/futures_funding_rate_perpetual"]
    # metrics_list = ["distribution/exchange_net_position_change"]
    # metrics_list = ["transactions/transfers_volume_exchanges_net"]
    # metrics_list = ["market/realized_volatility_2_weeks"]
    # metrics_list = ["derivatives/futures_open_interest_cash_margin_sum"]
    # metrics_list = ["supply/active_more_1y_percent"]
    # metrics_list = ["derivatives/options_25delta_skew_1_week"]
    # metrics_list = ["indicators/ssr"]
    # metrics_list = ["market/spot_volume_sum_intraday"]
    # metrics_list = ["derivatives/options_25delta_skew_1_week"]
    # metrics_list = ["derivatives/options_volume_put_call_ratio"]
    # metrics_list = ["derivatives/options_open_interest_put_call_ratio"]
    # metrics_list = ["derivatives/options_open_interest_distribution"]
    # metrics_list = ["derivatives/options_atm_implied_volatility_6_months"]
    metrics_list = ["market/realized_volatility_1_month"]
    # metrics_list = ["transactions/transfers_volume_exchanges_net_pit"]
    # metrics_list = ["derivatives/options_25delta_skew_1_week"]
    # metrics_list = ["indicators/ssr"]
    # metrics_list = ["transactions/transfers_volume_to_exchanges_sum"]
    
    model_list = ["tanh"] #["bband", "log_bband", "robust", "tanh", "ma_diff", "roc", "rsi", "min_max", "percentile", "raw", "2ma_cross"]

    for metrics in metrics_list:
        for model in model_list:
            print(f"Initializing strategy with model: {model} and metric: {metrics}")
            strategy = FactorStrategy(
                model=model,  # "bband", "log_bband", "robust", "tanh", "ma_diff", "roc", "rsi", "min_max", "percentile", "raw", "2ma_cross"
                metric1=metrics,
                #metric2="derivatives/futures_volume_daily_perpetual_sum",
                # metric2="market/marketcap_usd",
                # operator="A / B",
                asset_input1="HBAR",
                asset_input2="HBAR",
                asset_output1="HBAR",
                currency="NATIVE",
                long_short="long short",
                window=250,
                threshold=0.5,
                direction="momentum",  # "momentum", "reversion"
                resolution="1h",  # "1h", "24h"

                delay_time=10
            )

            test_dates = [ 
                # {"start": "2020-01-01", "end": "2021-12-31"},
                # {"start": "2022-01-01", "end": "2022-12-31"},
                # {"start": "2021-01-01", "end": "2022-12-31"},
                # {"start": "2023-01-01", "end": "2023-12-31"},
                # {"start": "2022-01-01", "end": "2023-12-31"},
                # {"start": "2024-01-01", "end": "2024-12-31"},
                # {"start": "2023-01-01", "end": "2024-12-31"},
                # {"start": "2024-08-14", "end": "2025-08-14"},
                # {"start": "2025-01-01", "end": "2025-08-14"},
                # {"start": "2020-01-01", "end": "2025-06-30"},
                {"start": "2025-01-01", "end": "2025-10-14"}
                # {"start": "2024-01-17", "end": "2025-07-24"},
                # {"start": "2025-07-25", "end": "2025-09-24"},
                # {"start": "2024-01-17", "end": "2024-04-17"},
                # {"start": "2024-04-18", "end": "2024-07-18"},
                # {"start": "2024-07-19", "end": "2024-10-19"},
                # {"start": "2024-10-20", "end": "2025-01-20"},
                # {"start": "2025-01-21", "end": "2025-04-21"},
                # {"start": "2025-04-22", "end": "2025-07-20"},
                # {"start": "2025-07-21", "end": "2025-09-24"},
                # {"start": "2025-10-01", "end": "2025-10-08"}
                ]
            for date in test_dates:
                print(f"Optimizing strategy for date range: {date['start']} to {date['end']}")
                start_timestamp = int(pd.Timestamp(date["start"]).timestamp())
                end_timestamp = int(pd.Timestamp(date["end"]).timestamp())

                strategy.optimize(start_timestamp, end_timestamp)