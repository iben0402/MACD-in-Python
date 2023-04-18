import pandas
import matplotlib.pyplot as plt

number_of_probes = 1000

daty = pandas.read_csv('cdr.csv', delimiter=';')
daty = daty.loc[:, 'Data']

zamk = pandas.read_csv('cdr.csv', delimiter=';')
zamk = zamk.loc[:, 'Zamkniecie']

# wykres wartosci spolki
plt.figure(figsize=(12, 8))
plt.plot(daty, zamk)
plt.title('Wartość akcji społki Tesla')
plt.xlabel('Daty')
plt.ylabel('Zamkniece')
plt.xticks(range(1, 1000, 50), rotation=30)
plt.show()


cdr = pandas.read_csv('cdr.csv', delimiter=';', index_col=0, parse_dates=True)
# EMA12
period = 12
N = (number_of_probes / period).__round__()
alpha = 2 / (N + 1)
factor = 1 - alpha
exp1 = []
value = 0
value_denominator = 0

for i in range(0, 26):
    exp1.append(0)

for i in range(26, 1000):
    for j in range(0, period + 1):
        day = zamk[i - j]  # Value of given day
        value += day * (factor ** j)  # Meter of EMAN for given day
        value_denominator += factor ** j  # Denominator of EMAN for given day

    value = value / value_denominator
    exp1.append(value)
    value = 0
    value_denominator = 0

# EMA26
period = 26
N = (number_of_probes / period).__round__()
alpha = 2 / (N + 1)
factor = 1 - alpha
exp2 = []
value = 0
value_denominator = 0

for i in range(0, 26):
    exp2.append(0)

for i in range(26, 1000):
    for j in range(0, period + 1):
        day = zamk[i - j]  # Value of given day
        value += day * (factor ** j)  # Meter of EMAN for given day
        value_denominator += factor ** j  # Denominator of EMAN for given day

    value = value / value_denominator
    exp2.append(value)
    value = 0
    value_denominator = 0

# MACD
macd = list()
for item_exp1, item_exp2 in zip(exp1, exp2):
    macd.append((item_exp1 - item_exp2))
cdr['MACD'] = macd

# Signal
table = cdr['MACD']
period = 9
N = (number_of_probes / period).__round__()
alpha = 2 / (N + 1)
factor = 1 - alpha
sig = []
value = 0
value_denominator = 0

for i in range(0, 35):
    sig.append(0)

for i in range(35, 1000):
    for j in range(0, period + 1):
        day = table[i - j]  # Value of given day
        value += day * (factor ** j)  # Meter of signal for given day
        value_denominator += factor ** j  # Denominator of signal for given day

    value = value / value_denominator
    sig.append(value)
    value = 0
    value_denominator = 0

cdr['Signal line'] = sig

fig, ax = plt.subplots()
cdr[['MACD', 'Signal line']].plot(ax=ax)
cdr['Zamkniecie'].plot(ax=ax, alpha=0.25, secondary_y=True)

plt.show()


# Algorithm to buy stocks

start_money = 1000
money = start_money
bought_stock = 0
macd = cdr['MACD']
sig = cdr['Signal line']

for i in range(35, 1000):
    if macd[i] >= sig[i] and macd[i-1] < sig[i-1]:
        # buy stock
        bought_stock = money / zamk[i]
        money = 0
        print("bought for value {0}".format(zamk[i]))
    elif macd[i] <= sig[i] and macd[i-1] > sig[i-1] and bought_stock > 0:
        #sell stock
        money = bought_stock*zamk[i]
        bought_stock = 0
        print("sold for value {0} \n \n".format(zamk[i]))

    if i == 999 and bought_stock > 0:
        money = bought_stock * zamk[i]
        bought_stock = 0
        print("sold for value {0} \n \n".format(zamk[i]))



print("You started with {0} and ended with {1}.".format(start_money, money))
print("You earned: {0}".format(money-start_money))
