import unittest
import datetime as dt

import backtrader as bt

from pyautofinance.common.engine import Engine, ComponentsAssembly
from pyautofinance.common.feeds import BackDatafeed
from pyautofinance.common.feeds.extractors import CCXTCandlesExtractor
from pyautofinance.common.dataflux import DiskDataflux
from pyautofinance.common.brokers import BackBroker
from pyautofinance.common.sizers import Sizer
from pyautofinance.common.metrics import EngineMetricsCollection, TotalGrossProfit
from pyautofinance.common.strategies import BracketStrategyExample, Strategy
from pyautofinance.common.timeframes import h4
from pyautofinance.common.testers import MonteCarloTester
from pyautofinance.common.metrics import RiskOfRuin


class TestTesters(unittest.TestCase):

    start_date = dt.datetime(2020, 1, 1)
    end_date = dt.datetime(2021, 1, 1)
    symbol = 'BTC-EUR'
    timeframe = h4

    cash = 100000
    commission = 0.02

    dataflux = DiskDataflux()

    broker = BackBroker(cash, commission)
    strategy = Strategy(BracketStrategyExample, stop_loss=2, risk_reward=3)
    datafeed = BackDatafeed(symbol, start_date, timeframe, end_date, dataflux, candles_extractor=CCXTCandlesExtractor())
    sizer = Sizer(bt.sizers.PercentSizer, percents=90)
    metrics = EngineMetricsCollection(TotalGrossProfit)

    assembly = ComponentsAssembly(broker, strategy, datafeed, sizer, metrics)

    def test(self):
        engine = Engine(self.assembly)
        result = engine.run()
        tester = MonteCarloTester(1000, 100000, 50000)
        test_result = tester.test(result[0])
        test_result['RiskOfRuin']

    def test_validation(self):
        engine = Engine(self.assembly)
        result = engine.run()
        tester = MonteCarloTester(1000, 100000, 50000)
        test_result = tester.test(result[0])

        metric = RiskOfRuin
        validation_function = lambda risk_of_ruin: risk_of_ruin < 0.3

        validation = tester.validate(test_result, metric, validation_function)
        self.assertIsInstance(validation, bool)



if __name__ == '__main__':
    unittest.main()