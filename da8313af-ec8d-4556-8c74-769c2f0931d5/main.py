from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, BB
from surmount.logging import log

class TradingStrategy(Strategy):
    """
    A strategy focusing on economic downturns, particularly with the consideration
    of war impacts on the North American economy. It focuses on Gold and Treasury
    ETFs, as well as inverse ETFs to the broader market. This demonstrates a bet
    against strong market performance in the face of socio-economic uncertainty.
    """
    def __init__(self):
        # Tickers for Gold ETF, Long-term Treasury ETF, and Inverse S&P 500 ETF
        self.tickers = ["GLD", "TLT", "SH"]
        # Initial allocation with an equal distribution
        self.initial_allocation = {ticker: 1/len(self.tickers) for ticker in self.tickers}

    @property
    def interval(self):
        # Daily data is likely sufficient for this strategic outlook
        return "1day"

    @property
    def assets(self):
        # The strategy focuses on these specific assets
        return self.tickers

    @property
    def data(self):
        # No specific additional data needed at initialization
        return []

    def run(self, data):
        """
        The 'run' method is where the trading logic lives. Given this strategy's focus,
        rebalancing might lean towards assets expected to perform better during economic
        downturns, adjusting allocations based on current market conditions.
        """
        # Example simplistic logic for rebalancing based on simple moving average trends
        allocation_dict = self.initial_allocation.copy()

        for ticker in self.tickers:
            d = data["ohlcv"]  # Assuming data structure compatibility
            if len(d) < 20:  # Check if there's enough data for SMA calculation
                continue  # Not enough data, skip this asset
            
            # Calculate a simple moving average for the last 20 days
            sma20 = SMA(ticker, d, 20)
            
            # Example condition - if the current price is below the 20-day SMA,
            # increase allocation for TLT and GLD, decrease for SH (or vice versa)
            # This is a simplistic view and should be adjusted according to thorough analysis
            if ticker in ["GLD", "TLT"] and d[-1][ticker]["close"] < sma20[-1]:
                allocation_dict[ticker] += 0.1  # Increasing stake in Gold and T-Bonds
            elif ticker == "SH" and d[-1][ticker]["close"] > sma20[-1]:
                allocation_dict[ticker] -= 0.1  # Decreasing stake in Inverse ETF
                
        # Normalize allocations to ensure they sum to 1 (or less)
        total = sum(allocation_dict.values())
        for ticker in allocation_dict:
            allocation_dict[ticker] /= total

        return TargetAllocation(allocation_dict)