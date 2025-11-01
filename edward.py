async def get_price_data(session, coin, resolution, window_size, minute_filter=10):
    today = datetime.now(timezone.utc)
    start_date = today - timedelta(days=window_size + 1)
    if resolution == "1h":
        start_date = today - timedelta(days=window_size/24 + 1)
    since = int(start_date.timestamp())
    until = int(time.time())
    
    # Always fetch 10-minute data to get specific minute of each hour
    fetch_resolution = "10m"
    params = {"a": coin, "s": since, "u": until, "api_key": API_KEY, "i": fetch_resolution}
    price_text = await fetch_data(session, price_url, params)
    if not price_text:
        return None
    
    df = pd.read_json(StringIO(price_text), convert_dates=['t']).rename(columns={'v': 'price'})
    
    # Filter to get only the specified minute of each hour (default 10th minute)
    if minute_filter is not None:
        df = df[df['t'].dt.minute == minute_filter]
        print(f"Filtered price data to minute {minute_filter} of each hour for {coin}")
    
    return df