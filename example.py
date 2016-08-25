#!/usr/bin/env python3
from simplestock import CommonStockData, PreferredStockData

allStockData = [
    CommonStockData   ("TEA", 100,  0       ),
    CommonStockData   ("POP", 100,  8       ),
    CommonStockData   ("ALE",  60, 23       ),
    PreferredStockData("GIN", 100,  8, 0.02 ),
    CommonStockData   ("JOE", 250, 13       )
    ]

allStockDataMap = dict([(s.sym, s) for s in allStockData])

tickerPrices = [s.parValue for s in allStockData]

def printBaseStockData(stock, tickerPrice):
    peRatio = stock.peRatio(tickerPrice)
    peRatio = "NA" if peRatio is None else "{:.2f}".format(peRatio)
    print("""
            Stock "{}" has:
                par value of "{:.2f}"
                ticker price of "{:.2f}"
                dividend of "{:.2f}"
                P/E ratio of "{}"
                last dividend of "{:.2f}"
          """.format(stock.sym,
                 stock.parValue,
                 tickerPrice,
                 stock.dividendYeld(tickerPrice),
                 peRatio,
                 stock.lastDividend
                )
        )

for p in zip(allStockData, tickerPrices):
    printBaseStockData(*p)

from simplestock import Transaction, TransactionLog

tLog = TransactionLog()

TIME_DELTA = 15 #minutes
now = 0 # interpreted in minutes
#some new transactions happen
tLog.recordTrade(Transaction("TEA", "BUY" , quantity=100, price=50,  timestamp=now))
tLog.recordTrade(Transaction("TEA", "SELL", quantity=100, price=50,  timestamp=now))
tLog.recordTrade(Transaction("TEA", "BUY" , quantity=200, price=100, timestamp=now))
tLog.recordTrade(Transaction("GIN", "BUY" , quantity=100, price=75, timestamp=now))

tLog.prepareIndex(max(0, now-TIME_DELTA)) # no-op here
print("TEA Stock price at t={} is {:.2f}".format(now, tLog.stockPrice("TEA")))
print("GBCE index at t={} is {:.2f}".format(now, tLog.computeIndex()))


now = 10 # interpreted in minutes
#some new transactions happen
tLog.recordTrade(Transaction("TEA", "BUY" , quantity=100, price=100, timestamp=now))
tLog.recordTrade(Transaction("TEA", "SELL", quantity=100, price=100, timestamp=now))
tLog.recordTrade(Transaction("TEA", "BUY" , quantity=200, price=200, timestamp=now))
tLog.recordTrade(Transaction("GIN", "BUY" , quantity=100, price=150, timestamp=now))


now = 16
tLog.prepareIndex(max(0, now-TIME_DELTA)) # discards old transactions from the index
print("TEA Stock price at t={} is {:.2f}".format(now, tLog.stockPrice("TEA")))
print("GBCE index at t={} is {:.2f}".format(now, tLog.computeIndex()))
