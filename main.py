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
    strategy = FactorStrategy(
        model="bband",        # "bband", "rsi", "percentile" etc, refer to model.py for more details

        metric1="derivatives/futures_open_interest_perpetual_sum",
        # transformType1="fft",  # "cumsum", "mean", "sqrt", "log" etc, refer to transformer.py for more details
        # transformPeriod1=50,

        metric2="derivatives/futures_volume_daily_perpetual_sum",
        # transformType2="raw",
        # transformPeriod2=50,

        operator="A / B",     # "A + B", "A - B", "A * B", "A / B", "A / (A + B)", refer to metric.apply_operator()

        asset_input1="HBAR",
        asset_input2="HBAR",
        asset_output1="HBAR",
        currency="NATIVE",

        long_short="long",
        window=250,
        threshold=0.5,
        direction="reversion",   # "momentum", "reversion"
        resolution="1h",        # "1h", "24h"

        delay_time=10          # lag price in minutes (multiple of 10)
        # heatmap_para=heatmap_para
    )

    '''-------------------------Strategy Functions------------------------------------'''
    # strategy.plot_metric(start_timestamp, end_timestamp)

    # strategy.backtest(start_timestamp, end_timestamp)
    # strategy.plot_equity_curve()


    test_dates = [# {"start": "2020-01-01", "end": "2021-12-31"},
    #               {"start": "2022-01-01", "end": "2022-12-31"},
    #               {"start": "2021-01-01", "end": "2022-12-31"},
    #               {"start": "2023-01-01", "end": "2023-12-31"},
    #               {"start": "2022-01-01", "end": "2023-12-31"},
    #               {"start": "2024-01-01", "end": "2024-12-31"},
    #               {"start": "2023-01-01", "end": "2024-12-31"},
    #               {"start": "2025-01-01", "end": "2025-08-14"},
                    {"start": "2020-01-01", "end": "2025-06-30"},
                    {"start": "2025-07-01", "end": "2025-09-19"}
                  ]
    for date in test_dates:
        print(f"Optimizing strategy for date range: {date['start']} to {date['end']}")
        start_timestamp = int(pd.Timestamp(date["start"]).timestamp())
        end_timestamp = int(pd.Timestamp(date["end"]).timestamp())

        strategy.optimize(start_timestamp, end_timestamp)

    # strategy.optimize(start_timestamp, end_timestamp)

    # strategy.batch_optimize(start_timestamp, end_timestamp)

