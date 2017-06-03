"""Shows the relationship between a bond's convexity and price.
Shows the magnitude of change in bond prices relative to duration given changes in the interest rates."""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import duration_functions as dfunc
import sys


cvx1 = pd.read_csv("csv7.csv").set_index("Bonds")
cvx1.index.name = None


cvx1.settlement = pd.to_datetime(cvx1.settlement)
cvx1.maturity = pd.to_datetime(cvx1.maturity)

cvx1.face_value = cvx1.face_value.str.replace("$", "").str.replace(",", "").astype(float)
cvx1.coupon_rate = cvx1.coupon_rate.str.replace("%", "").astype(float) / 100
cvx1.ir1 = cvx1.ir1.str.replace("%", "").astype(float) / 100


cvx1["yrs"] = ((cvx1.maturity - cvx1.settlement) / np.timedelta64(1, "Y")).astype(int)

cvx1 = cvx1.reindex_axis(["settlement", "maturity", "yrs", "face_value", "coupon_rate", "ir1", "period"], axis=1)


durations, convexities, prices = [],[],[]

for bond_name in cvx1.index:
	bd_yrs = cvx1.loc[bond_name, "yrs"]
	bd_fv = cvx1.loc[bond_name, "face_value"]
	bd_cr = cvx1.loc[bond_name, "coupon_rate"]
	bd_ir1 = cvx1.loc[bond_name, "ir1"]
	bd_period = cvx1.loc[bond_name, "period"]
	
	num_semesters = bd_yrs * bd_period

	semesters = dfunc.get_semesters(num_semesters, "Semesters")

	cash_flow = dfunc.get_cashflows(num_semesters, bd_fv, bd_cr, bd_period, name="Cash_Flows")

	present_value = dfunc.get_present_value(cash_flow, bd_ir1, bd_period, semesters, name="Present_Value")

	pv_sum = present_value.sum()

	wt = dfunc.get_weight(present_value, pv_sum, name="Weight")

	wtT = dfunc.get_weightT(wt, semesters, name="wt*T")

	convex_ops = dfunc.get_convexity(cash_flow, bd_ir1, semesters, name="convex_ops")

	cvx2 = pd.concat([pd.DataFrame(semesters), cash_flow, present_value, wt, wtT, convex_ops], axis=1).set_index("Semesters")

	dur = wtT.sum() / bd_period

	convexity = convex_ops.sum() /  (present_value.sum() * (1 + bd_ir1)**2)

	durations.append(dur)
	convexities.append(convexity)
	prices.append(present_value.sum())

	print(cvx2)

	print("\n" + bond_name + " price: %.2f" %present_value.sum() + "$")
	print(bond_name + " duration: %.2f" %dur)
	print(bond_name + " convexity: %.2f" %convexity + "\n")

try:
	delta_ir= float(input("Enter change in interest rate(%): "))
except:
	sys.exit("Invalid Interger")

cvx1["Price1"] = prices
cvx1["Duration"] = durations
cvx1["Convexity"] = convexities

cvx1["delta_ir"] = delta_ir / 100

cvx1["ir2"] = cvx1.ir1 + cvx1.delta_ir

cvx1["delta_price(%)"] = (-cvx1.Duration / (1 + cvx1.ir1)) * cvx1.delta_ir

cvx1["convexity_adjustment"] = 0.5 * cvx1.Convexity * (cvx1.delta_ir)**2

cvx1["delta_price"] = cvx1["Price1"] * (cvx1["delta_price(%)"] + cvx1["convexity_adjustment"])

cvx1["Price2"] = cvx1.Price1 + cvx1["delta_price"]

cvx1 = cvx1.reindex_axis(["settlement", "maturity", "yrs", "coupon_rate", "period", "Duration", "Convexity", "ir1", "delta_ir", "ir2", "delta_price(%)", "convexity_adjustment", "Price1", "delta_price", "Price2"], axis=1).copy()




print(cvx1)

fig = plt.figure()

ax1 = plt.subplot2grid((2,1), (0,0), colspan=1, rowspan=1)
plt.title("Bond Convexity", fontsize=22, color="#353856")
plt.ylabel("Bond Price($)", color="#0098d2", fontsize=15)
ax2 = plt.subplot2grid((2,1), (1,0), colspan=1, rowspan=1)
plt.xlabel("Convexity", color="#5c7e9a", fontsize=20)
plt.ylabel("Price(delta-YTM)", color="#5c7e9a", fontsize=15)


ax1.plot(convexities, prices, "--", color="#0098d2", label="Convexity-Bond Price")


for bond_name1 in cvx1.index:

	scatter_prices, scatter_conv = [], []
	scatter_prices.append(cvx1.loc[bond_name1, "Price1"])
	scatter_prices.append(cvx1.loc[bond_name1, "Price2"])
	scatter_conv.append(cvx1.loc[bond_name1, "Convexity"])
	scatter_conv.append(cvx1.loc[bond_name1, "Convexity"])

	ax2.scatter(scatter_conv, scatter_prices, label=bond_name1[-1]+ ", " + str(cvx1.loc[bond_name1, "delta_ir"]) + "%" +" delta")


ax1.grid(True)
ax2.grid(True)

ax1.legend().get_frame().set_alpha(0.8)
ax2.legend(ncol=2, prop=dict(size=9)).get_frame().set_alpha(0.8)

ax1.axes.xaxis.set_ticklabels([])
plt.subplots_adjust(hspace=0.1)
plt.show()

cvx1.to_csv("convexity.csv")
plt.savefig("convexity.png")
