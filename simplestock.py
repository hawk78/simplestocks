import statistics as stats
import math
import bisect

class CommonStockData:
    def __init__(self, sym, parValue, lastDividend):
        self.sym = sym
        self.parValue = parValue
        self.lastDividend = lastDividend

    def dividendYeld(self, tickerPrice):
        return self.lastDividend / tickerPrice

    # I think the PE ratio is usally calulated as tickerPrice / last12MonthsDividend
    # so lets suppose all the shares pay dividends yearly
    def peRatio(self, tickerPrice):
        ld = self.lastDividend
        return tickerPrice / ld if ld != 0 else None

class PreferredStockData(CommonStockData):
    def __init__(self, sym, parValue, lastDividend, fixedDividend):
        super().__init__(sym, parValue, lastDividend)
        self.fixedDividend = fixedDividend

    def dividendYeld(self, tickerPrice):
        return self.fixedDividend * self.parValue / tickerPrice

class Transaction:
    def __init__(self, sym, indicator, quantity, price, timestamp):
        self.sym = sym
        self.indicator = indicator
        self.quantity = quantity
        self.price = price
        self.timestamp = timestamp

    def __lt__(self, other):
        return self.timestamp < other.timestamp

    def  __repr__(self):
        return "([{}] {} {} {}@{})".format(
            self.timestamp,
            self.indicator,
            self.sym,
            self.quantity,
            self.price
        )

class TransactionLog:
    def __init__(self):
        self.oldTransactions = []
        self.transactions = []
        self.indexData = {}

    def recordTrade(self, transaction):
        sym = transaction.sym
        self.transactions.append(transaction)
        data = self.indexData.setdefault(transaction.sym, (0,0))
        prc, qty = (transaction.price, transaction.quantity)
        self.indexData[sym] = (data[0] + prc*qty , data[1] + qty)
        return self

    def prepareIndex(self, timestamp):
        fakeTr = Transaction("Fake", "SELL", 0, 0, timestamp)
        first = bisect.bisect_left(self.transactions, fakeTr)
        removedTransactions = self.transactions[:first]
        self.oldTransactions += removedTransactions
        self.transactions[:first] = []
        for tr in removedTransactions: # can be parallelized
            data = self.indexData[tr.sym]
            prc, qty = (tr.price, tr.quantity)
            self.indexData[tr.sym] = (data[0] - prc*qty, data[1] - qty)

    def stockPrice(self, sym):
        prc, qty = self.indexData[sym]
        return prc / qty

    def computeIndex(self):
        prcs = self.indexData.values()
        return math.exp(stats.mean([math.log(prc/qty) for (prc, qty) in prcs]))
