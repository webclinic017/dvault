v2.1.0 released 2022-02-13
- filtered out untradable items from universe
- filtered out penny stocks when generating srategies
- filter out low volume stocks
- condone failed buys if a price move made your limit order invalid
- implement script to purge stale orders and positions
- account for purged positions in charts and expectency calculations

v2.0.0 released 2022-03-19
- Implemented bracket orders, take profit and stop loss sale orders are associtated with each buy
- use limit orders instead of market orders
- provide an easier way to seed new runs
- otimization results are logged to .csv file
- beta released 2022-02-13

v1.0.0 released 2022-01-23
- Get the close times from alpaca
- specify objective and threshold in terms of number of trading days
- inteprest time frame value in terms of trading days
- hard code time frame units to be only days
- design around running after midnight

v0.3.0 released 2022-01-17
- stabalized with test deployments
- Tested mainly unler live paper trading conditions

v0.2.0 released 2022-01-02
- set systemd timer period to be 10 secs, 60 secs, 10 mins, or hourly based on magnitude of strategy time period

v0.1.0 released 2022-01-02
- Initial released version passed adhoc testing
- tested install / uninstall during non market hours
- tested some 30min bars during market hours
- backtested daily bars for ~1500 tickers ~1.5 yrs back

