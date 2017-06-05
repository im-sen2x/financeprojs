"""Visualizes the Barbell Strategy(making a bond portfolios'convexity o higher magnitude)"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import duration_functions as dfunc
import matplotlib.ticker as mticker

bb = pd.read_csv("csv8.csv").set_index("Bonds")
bb.index.name = None

bb.dropna(how="all", inplace=True)

bb.settlement = pd.to_datetime(bb.settlement)
bb.maturity = pd.to_datetime(bb.maturity)

bb.face_value = bb.face_value.str.replace("$", "").str.replace(",", "").astype(float) / 100
bb.coupon_rate = bb.coupon_rate.str.replace("%", "").astype(float) / 100
bb.ir1 = bb.ir1.str.replace("%", "").astype(float) / 100
bb.period =  bb.period.astype(int)

bb["years"] = ((bb.maturity - bb.settlement) / np.timedelta64(1, "Y")).astype(int)

durations, convexities, prices = [],[],[]

for bond_name in bb.index:
	bd_yrs = bb.loc[bond_name, "years"]
	bd_fv = bb.loc[bond_name, "face_value"]
	bd_cr = bb.loc[bond_name, "coupon_rate"]
	bd_ir1 = bb.loc[bond_name, "ir1"]
	bd_period = bb.loc[bond_name, "period"]
	
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


bb["Price1"] = prices
bb["Duration"] = durations
bb["Convexity"] = convexities

bb = bb.reindex_axis(["settlement", "maturity", "face_value", "coupon_rate", "period", "Price1", "years", "ir1", "Duration", "Convexity"], axis=1)
bb1 = bb.set_index([[i for i in range(0, len(bb.index))]])
print(bb)
print(bb1)

c = 0
ind, parts, new_conv = [], [], {}

for row in range(1, len(bb1.index), 3):


	d1 =  (bb1.ix[row, "Duration"] - bb1.ix[row+1, "Duration"]) / (bb1.ix[row-1, "Duration"] - bb1.ix[row+1, "Duration"])
	d2 = 1 - d1


	ind.append(row-1)
	ind.append(row+1)
	parts.append(d1)
	parts.append(d2)
	new_conv[row] = (bb1.ix[row-1, "Convexity"] * d1 + bb1.ix[row+1, "Convexity"] * d2)
	c += 1

pct = pd.Series(parts, index=ind, name="Pct")
bb1 = pd.concat([bb1, pct], axis=1)
bb1["New Convexity"] = bb1.Convexity * bb1.Pct

bb1["New Convexity"].fillna(new_conv, inplace=True)
bb1 = bb1.reindex_axis(["settlement", "maturity", "face_value", "coupon_rate", "period", "Price1", "years", "ir1", "Duration", "Pct", "Convexity", "New Convexity"], axis=1)

c1 = bb1.ix[[s for s in range (1, len(bb1.index),3)], "Convexity"]
c2 = bb1.ix[[s for s in range (1, len(bb1.index),3)], "New Convexity"]

fig = plt.figure()

ax1 = plt.subplot2grid((2,1), (0,0), rowspan=1, colspan=1)
plt.title("BARBELL STRATEGY", color="#4d4848", fontsize=21)
plt.ylabel("CONVEXITY(bar)", color="#4d4848", fontsize=14)

ax2 = plt.subplot2grid((2,1), (1,0), rowspan=1, colspan=1)
plt.xlabel("PORTFOLIO", color="#4d4848", fontsize=18)
plt.ylabel("CONVEXITY(graph)", color="#4d4848", fontsize=14)


xticks = [s for s in range(c)]


ax1.bar(xticks, c2.values, width=0.3, color="#32bd12", label="convexity_2")

ax1.bar(xticks, c1.values, width=0.3, color="#cc2121", label="convexity_1")




ax1.xaxis.set_major_locator(mticker.MaxNLocator(nbins=4))
ax1.yaxis.set_major_locator(mticker.MaxNLocator(nbins=4))
ax1.axes.xaxis.set_ticklabels([])
ax1.set_xlim(-0.5, 3.5)
ax1.set_ylim(0, 200)

ax2.xaxis.set_major_locator(mticker.MaxNLocator(nbins=4))
ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=4))
ax2.set_xlim(-0.5, 3.5)
ax2.set_ylim(60, 200)
plt.xticks(xticks, ["A", "B", "C", "D"])

ax2.plot(xticks, c2.values, color="#32bd12", label="convexity_2")
ax2.plot(xticks, c1.values, color="#cc2121", label="convexity_1")


ax2.fill_between(xticks[:], c2.values[:], c1.values[:], where=(c2.values[:] > c1.values[:]), facecolor="#32bd12", edgecolor="#32bd12", alpha=0.3)

bbox_props = dict(boxstyle='round',fc='w', ec='k',lw=1)
for j in xticks:

	ymin = (c1.values[j] - 60) / 140
	ymax = (c2.values[j] - 60) / 140

	ax2.axvline(xticks[j], ymin=ymin, ymax=ymax, color="red", linewidth=1, ls="--")
	ax2.annotate("+" + str(c2.values[j] - c1.values[j])[0:5], (xticks[j], c2.values[j]),
                 xytext = (xticks[j]-0.1, c2.values[j] + 10), bbox=bbox_props)

ax2.grid(True)

ax1.legend()
ax2.legend()

plt.show()


print(bb1)
