"""Visualizes predicted bond prices regarding changes in interest rates""""

import pandas as pd
import numpy as np
import bond_price as bp
import matplotlib.pyplot as plt
import duration_functions as dfunc

df1 = pd.read_csv("csv5.csv").set_index("Attributes")

df1.index.name = None
df1.columns = df1.columns.str.replace(" ", "_")
df1.index = df1.index.str.replace(" ", "_")



df1.loc["Maturity", :] = df1.loc["Maturity", :].astype(int)
df1.loc["Face_Value", :] = df1.loc["Face_Value", :].str.replace("$", "").str.replace(",", "").astype(float)
df1.loc["Periods", :] = df1.loc["Periods", :].astype(int)
df1.loc["Coupon_Rate", :] = df1.loc["Coupon_Rate", :].str.replace("%", "").astype(float) / 100
df1.loc["YTM", :] = df1.loc["YTM", :].str.replace("%", "").astype(float) / 100
df1.loc["delta_YTM", :] = df1.loc["delta_YTM", :].str.replace("%", "").astype(float) / 100



bond_prices = []
bond_durations = []
deltas = []
delta_prices = []
new_prices = []

for bond in df1.columns:

	bd_mat = df1.loc["Maturity", bond]
	bd_fv = df1.loc["Face_Value", bond]
	bd_cr = df1.loc["Coupon_Rate", bond]
	bd_periods = df1.loc["Periods", bond]
	bd_YTM = df1.loc["YTM", bond]
	bd_delta = df1.loc["delta_YTM", bond]

	price = bp.annuity_operation(bd_fv, bd_YTM, bd_cr, bd_periods, bd_mat) + bp.maturity_operation(bd_fv, bd_YTM, bd_periods, bd_mat)
	bond_prices.append(price)

	num_semesters = bd_mat * bd_periods
	semesters = dfunc.get_semesters(num_semesters, "Semesters")

	cash_flow = dfunc.get_cashflows(num_semesters, bd_fv, bd_cr, bd_periods, "Cash_Flows")

	present_value = dfunc.get_present_value(cash_flow, bd_YTM, bd_periods, semesters, "Present_Value")

	pv_sum = present_value.sum()

	wt = dfunc.get_weight(present_value, pv_sum, "Weight")

	wtT = dfunc.get_weightT(wt, semesters, "wt*T")

	dur = wtT.sum() / bd_periods
	bond_durations.append(dur)

	delta = -(dur / (1+bd_YTM)) * (bd_delta)
	deltas.append(delta)

	delta_price = price * delta
	delta_prices.append(delta_price)

	new_price = price + delta_price
	new_prices.append(new_price)


d1 = pd.DataFrame([bond_prices], index=["Price"], columns=df1.columns.values)
d2 = pd.DataFrame([bond_durations], index=["Duration"], columns=df1.columns.values)
d3 = pd.DataFrame([deltas], index=["delta%"], columns=df1.columns.values)
d4 = pd.DataFrame([delta_prices], index=["delta_Price"], columns=df1.columns.values)
d5 = pd.DataFrame([new_prices], index=["Predicted_Price"], columns=df1.columns.values)

new_df = pd.concat([df1, d1, d2, d3, d4, d5], axis=0)
new_df.loc["delta%",: ] = new_df.loc["delta%",: ] * 100

print(new_df)

fig = plt.figure()
ax1 = plt.subplot2grid((1,1), (0,0), rowspan=1, colspan=1) 
plt.ylabel("Price($)", fontsize=18, color="#525252")
plt.xlabel("Duration(years)", fontsize=18, color="#525252")
plt.title("Price Approximations of Bonds", fontsize=22, color="#525252")

ax1.grid(True)

for bond1 in new_df.columns:
	x = []
	y = []
	x.append(new_df.loc["Duration", bond1])
	x.append(new_df.loc["Duration", bond1])
	y.append(new_df.loc["Price", bond1])
	y.append(new_df.loc["Predicted_Price", bond1])

	print(x, y)

	ax1.scatter(x, y, label="delta " + str(new_df.loc["delta_YTM", bond1] * 100) + "%") 
	#break
	ax1.set_xlim(2, 18)
	ax1.set_ylim(400, 1600)
plt.legend(loc=2, ncol=2, prop=dict(size=10)).get_frame().set_alpha(0.7)

plt.show()


