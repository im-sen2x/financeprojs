"""Python 3.0 file that visualizes the Relationship between the Bond Price and Interest Rates(YTM)""""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import bond_price as bp


df1 = pd.read_csv("csv1.csv", dtype={"Face Value":float})

df1.columns = df1.columns.str.replace(" ", "_")

df1.Acquisition_Date = pd.to_datetime(df1.Acquisition_Date)
df1.Maturity_Date = pd.to_datetime(df1.Maturity_Date)

df1.Interest_Rate = df1.Interest_Rate.str.replace("%", "").astype(float) / 100
df1.Coupon_Rate = df1.Coupon_Rate.str.replace("%", "").astype(float) / 100


df1["Years till Maturity"] = ((df1.Maturity_Date - df1.Acquisition_Date) / np.timedelta64(1, 'Y')).astype(int)
df1["Coupon Pay"] = bp.coupon_pay(df1.Face_Value, df1.Coupon_Rate, df1["Years till Maturity"])
df1["Annuity Value"] = bp.annuity_operation(df1["Coupon Pay"], df1.Interest_Rate, df1.Period, df1["Years till Maturity"])
df1["Maturity Value"] = bp.maturity_operation(df1.Face_Value, df1.Interest_Rate, df1.Period, df1["Years till Maturity"])
df1["Bond Price"] = df1["Annuity Value"] + df1["Maturity Value"]

pd.set_option("precision", 2)


fig = plt.figure()
ax1 = plt.subplot2grid((1, 1), (0, 0), rowspan=1, colspan=1)
ax1.grid(True)
plt.title("Price-Interest Rate Relationship", fontsize=15)
plt.xlabel("Interest Rates", fontsize=12, color="#510800")
plt.ylabel("Bond Price", fontsize=12, color="#510800")

ax1.axes.xaxis.set_ticklabels([a for a in range(0, 21, 1)]) #optional

ax1.xaxis.set_major_locator(mticker.MaxNLocator(nbins=21))

ax1.plot(df1.loc[:,"Interest_Rate"] * 100, df1.loc[:,"Bond Price"], color="#002a83", ls="--")

plt.subplots_adjust(left=0.15, bottom=0.1, right=0.9, top=0.90, wspace=0.2, hspace=0.3)
plt.show()


