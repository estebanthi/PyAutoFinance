import backtrader as bt
import statistics


class TradesInfo(bt.Analyzer):

    def __init__(self):
        self.returns = []

    def notify_trade(self, trade):
        if trade.isclosed:
            dir = 'short'
            if trade.history[0].event.size > 0: dir = 'long'

            brokervalue = self.strategy.broker.getvalue()

            pnl = trade.history[len(trade.history) - 1].status.pnlcomm
            pnlpcnt = 100 * pnl / brokervalue

            self.returns.append([pnlpcnt, dir])

    def get_analysis(self):
        return {
            "avg_return": statistics.mean([item[0] for item in self.returns]),
            "avg_return_short": statistics.mean([item[0] for item in self.returns if item[1] == "short"]),
            "avg_return_long": statistics.mean([item[0] for item in self.returns if item[1] == "long"])
                }