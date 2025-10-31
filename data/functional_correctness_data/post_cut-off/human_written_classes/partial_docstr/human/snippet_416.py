from StrateQueue.live_system.ib_data_manager import IBDataManager
from typing import Dict, Any

class StreamingStrategy:
    """
    Example streaming strategy that uses real-time data from IB Gateway
    """

    def __init__(self, data_manager: IBDataManager):
        self.data_manager = data_manager
        self.positions = {}
        self.last_signals = {}
        self.price_change_threshold = 0.005
        self.max_position_size = 1000
        logger.info('StreamingStrategy initialized')

    def on_market_data(self, symbol: str, data_type: str, data: Dict[str, Any]):
        """
        Callback function for market data updates

        Args:
            symbol: Symbol that was updated
            data_type: Type of data ('tick', 'bar')
            data: Data dictionary
        """
        try:
            if data_type == 'tick' and 'last_price' in data:
                current_price = data['last_price']
                if current_price is None:
                    return
                from src.StrateQueue.utils.price_formatter import PriceFormatter
                bid_str = PriceFormatter.format_price_for_display(data.get('bid')) if data.get('bid') != 'N/A' else 'N/A'
                ask_str = PriceFormatter.format_price_for_display(data.get('ask')) if data.get('ask') != 'N/A' else 'N/A'
                logger.info(f'📊 {symbol}: {PriceFormatter.format_price_for_display(current_price)} (bid: {bid_str}, ask: {ask_str})')
                self._check_momentum_signal(symbol, current_price)
            elif data_type == 'bar':
                logger.info(f"📈 {symbol} Bar: O:{data['open']:.2f} H:{data['high']:.2f} L:{data['low']:.2f} C:{data['close']:.2f} V:{data['volume']}")
                self._check_bar_signal(symbol, data)
        except Exception as e:
            logger.error(f'Error processing market data for {symbol}: {e}')

    def _check_momentum_signal(self, symbol: str, current_price: float):
        """Check for momentum-based trading signals"""
        try:
            price_series = self.data_manager.get_price_series(symbol, count=50)
            if len(price_series) < 10:
                return
            recent_prices = price_series.tail(10)
            price_change = (current_price - recent_prices.iloc[0]) / recent_prices.iloc[0]
            if price_change > self.price_change_threshold:
                if self.last_signals.get(symbol) != 'BUY':
                    logger.info(f'🟢 BUY signal for {symbol} - momentum: {price_change:.2%}')
                    self.last_signals[symbol] = 'BUY'
            elif price_change < -self.price_change_threshold:
                if self.last_signals.get(symbol) != 'SELL':
                    logger.info(f'🔴 SELL signal for {symbol} - momentum: {price_change:.2%}')
                    self.last_signals[symbol] = 'SELL'
        except Exception as e:
            logger.error(f'Error in momentum signal check for {symbol}: {e}')

    def _check_bar_signal(self, symbol: str, bar_data: Dict):
        """Check for bar-based trading signals"""
        try:
            ohlcv_df = self.data_manager.get_ohlcv_dataframe(symbol, count=20)
            if len(ohlcv_df) < 5:
                return
            ohlcv_df['sma_5'] = ohlcv_df['close'].rolling(5).mean()
            ohlcv_df['sma_10'] = ohlcv_df['close'].rolling(10).mean()
            if len(ohlcv_df) >= 2:
                current_sma5 = ohlcv_df['sma_5'].iloc[-1]
                current_sma10 = ohlcv_df['sma_10'].iloc[-1]
                prev_sma5 = ohlcv_df['sma_5'].iloc[-2]
                prev_sma10 = ohlcv_df['sma_10'].iloc[-2]
                if current_sma5 > current_sma10 and prev_sma5 <= prev_sma10:
                    logger.info(f'🌟 Golden Cross detected for {symbol} - SMA5 crossed above SMA10')
                elif current_sma5 < current_sma10 and prev_sma5 >= prev_sma10:
                    logger.info(f'💀 Death Cross detected for {symbol} - SMA5 crossed below SMA10')
        except Exception as e:
            logger.error(f'Error in bar signal check for {symbol}: {e}')