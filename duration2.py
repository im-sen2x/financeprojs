"""Python 3.0 file that visualizes the factors in the duration on a bond(Coupon Rate, Maturity, and Interest Rates(YTM))""""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import bond_price as bp

def p_value(fv, ir, n, sem):
	return fv / (1 + ir/n) ** sem

dr1 = pd.read_csv("csv2.csv").set_index("Attributes")
dr3 = pd.read_csv("csv3.csv").set_index("Attributes")
dr5 = pd.read_csv("csv4.csv").set_index("Attributes")

dr1.index.name = None
dr3.index.name = None
dr5.index.name = None


dr1.columns = dr1.columns.str.replace(" ", "_")
dr1.index = dr1.index.str.replace(" ", "_")

dr3.columns = dr3.columns.str.replace(" ", "_")
dr3.index = dr3.index.str.replace(" ", "_")

dr5.columns = dr5.columns.str.replace(" ", "_")
dr5.index = dr5.index.str.replace(" ", "_")


dr1.loc["Maturity", :] = dr1.loc["Maturity", :].astype(int)
dr1.loc["Face_Value", :] = dr1.loc["Face_Value", :].str.replace("$", "").str.replace(",", "").astype(int)
dr1.loc["Periods", :] = dr1.loc["Periods", :].astype(int)
dr1.loc["Coupon_Rate", :] = dr1.loc["Coupon_Rate", :].str.replace("%", "").astype(int) / 100
dr1.loc["YTM", :] = dr1.loc["YTM", :].str.replace("%", "").astype(int) / 100

dr3.loc["Maturity", :] = dr3.loc["Maturity", :].astype(int)
dr3.loc["Face_Value", :] = dr3.loc["Face_Value", :].str.replace("$", "").str.replace(",", "").astype(int)
dr3.loc["Periods", :] = dr3.loc["Periods", :].astype(int)
dr3.loc["Coupon_Rate", :] = dr3.loc["Coupon_Rate", :].str.replace("%", "").astype(int) / 100
dr3.loc["YTM", :] = dr3.loc["YTM", :].str.replace("%", "").astype(int) / 100

dr5.loc["Maturity", :] = dr5.loc["Maturity", :].astype(int)
dr5.loc["Face_Value", :] = dr5.loc["Face_Value", :].str.replace("$", "").str.replace(",", "").astype(int)
dr5.loc["Periods", :] = dr5.loc["Periods", :].astype(int)
dr5.loc["Coupon_Rate", :] = dr5.loc["Coupon_Rate", :].str.replace("%", "").astype(int) / 100
dr5.loc["YTM", :] = dr5.loc["YTM", :].str.replace("%", "").astype(int) / 100

print(dr1)

durations = []
for column_name in dr1.columns:

	bd_maturity = dr1.loc["Maturity", column_name]
	bd_facevalue = dr1.loc["Face_Value", column_name]
	bd_couponrate = dr1.loc["Coupon_Rate", column_name]
	bd_periods = dr1.loc["Periods", column_name]
	bd_YTM = dr1.loc["YTM", column_name]

	num_semesters = bd_maturity * bd_periods
	semesters = pd.Series([s for s in range(1, num_semesters + 1)] , name="Semesters")

	c_flows = []
	for n in range(num_semesters):
		cf = 0
		if n + 1 == num_semesters:
			cf = bp.coupon_pay(bd_facevalue, bd_couponrate, bd_periods) + bd_facevalue
			c_flows.append(cf)
		else:
			cf = bp.coupon_pay(bd_facevalue, bd_couponrate, bd_periods)
			c_flows.append(cf)

	cash_flow = pd.Series(c_flows, name="Cash_Flows")

	present_value = pd.Series(p_value(cash_flow, bd_YTM, bd_periods, semesters), name="Present_Value")

	pv_sum = present_value.sum()

	wt = pd.Series(present_value / pv_sum, name="Weight")

	wtT = pd.Series(wt * semesters, name="wt*T")

	dr2 = pd.concat([pd.DataFrame(semesters), cash_flow, present_value, wt, wtT], axis=1).set_index("Semesters")

	dr2.index.name = None
	dur = wtT.sum() / bd_periods
	durations.append(dur)
	print(column_name)
	#print(dr2)
	print("\n" + column_name + " Duration in by period: " + str(wtT.sum()))
	print(column_name + " Duration in by years: " + str(dur) + "\n")



durations3 = []
for column_name3 in dr3.columns:

	bd_maturity = dr3.loc["Maturity", column_name3]
	bd_facevalue = dr3.loc["Face_Value", column_name3]
	bd_couponrate = dr3.loc["Coupon_Rate", column_name3]
	bd_periods = dr3.loc["Periods", column_name3]
	bd_YTM = dr3.loc["YTM", column_name3]

	num_semesters = bd_maturity * bd_periods
	semesters = pd.Series([s for s in range(1, num_semesters + 1)] , name="Semesters")

	c_flows = []
	for n in range(num_semesters):
		cf = 0
		if n + 1 == num_semesters:
			cf = bp.coupon_pay(bd_facevalue, bd_couponrate, bd_periods) + bd_facevalue
			c_flows.append(cf)
		else:
			cf = bp.coupon_pay(bd_facevalue, bd_couponrate, bd_periods)
			c_flows.append(cf)

	cash_flow = pd.Series(c_flows, name="Cash_Flows")

	present_value = pd.Series(p_value(cash_flow, bd_YTM, bd_periods, semesters), name="Present_Value")

	pv_sum = present_value.sum()

	wt = pd.Series(present_value / pv_sum, name="Weight")

	wtT = pd.Series(wt * semesters, name="wt*T")

	dr4 = pd.concat([pd.DataFrame(semesters), cash_flow, present_value, wt, wtT], axis=1).set_index("Semesters")

	dr4.index.name = None
	dur = wtT.sum() / bd_periods
	durations3.append(dur)
	print(column_name3)
	#print(dr4)
	print("\n" + column_name + " Duration in by period: " + str(wtT.sum()))
	print(column_name + " Duration in by years: " + str(dur) + "\n")

durations5 = []
for column_name5 in dr5.columns:

	bd_maturity = dr5.loc["Maturity", column_name5]
	bd_facevalue = dr5.loc["Face_Value", column_name5]
	bd_couponrate = dr5.loc["Coupon_Rate", column_name5]
	bd_periods = dr5.loc["Periods", column_name5]
	bd_YTM = dr5.loc["YTM", column_name5]

	num_semesters = bd_maturity * bd_periods
	semesters = pd.Series([s for s in range(1, num_semesters + 1)] , name="Semesters")

	c_flows = []
	for n in range(num_semesters):
		cf = 0
		if n + 1 == num_semesters:
			cf = bp.coupon_pay(bd_facevalue, bd_couponrate, bd_periods) + bd_facevalue
			c_flows.append(cf)
		else:
			cf = bp.coupon_pay(bd_facevalue, bd_couponrate, bd_periods)
			c_flows.append(cf)

	cash_flow = pd.Series(c_flows, name="Cash_Flows")

	present_value = pd.Series(p_value(cash_flow, bd_YTM, bd_periods, semesters), name="Present_Value")

	pv_sum = present_value.sum()

	wt = pd.Series(present_value / pv_sum, name="Weight")

	wtT = pd.Series(wt * semesters, name="wt*T")

	dr6 = pd.concat([pd.DataFrame(semesters), cash_flow, present_value, wt, wtT], axis=1).set_index("Semesters")

	dr6.index.name = None
	dur = wtT.sum() / bd_periods
	durations5.append(dur)
	print(column_name5)
	#print(dr6)
	print("\n" + column_name + " Duration in by period: " + str(wtT.sum()))
	print(column_name + " Duration in by years: " + str(dur) + "\n")

fig = plt.figure()

ax1 = plt.subplot2grid((3,1), (0,0), rowspan=1, colspan=1, label="Coupon Rate-Duration")
plt.title("Duration Relationships", fontsize=15)
plt.ylabel("Coupon Rate(%)", color="#db553e", fontsize=10)
ax2 = plt.subplot2grid((3,1), (1,0), rowspan=1, colspan=1, label="Maturity-Duration")
plt.ylabel("Maturity(years)", color="#636363", fontsize=10)
ax3 = plt.subplot2grid((3,1), (2,0), rowspan=1, colspan=1, label="YTM-Duration")
plt.xlabel("Duration(years)", color="#134c67", fontsize=12)
plt.ylabel("Yield to Maturity(%)", color="#134c67", fontsize=10)

ax1.grid(True)
ax2.grid(True)
ax3.grid(True)

ax1.plot(durations, dr1.loc["Coupon_Rate", :] * 100, color="#db553e", ls="--")

ax2.plot(durations3, dr3.loc["Maturity", :], color="#636363", ls="--")

ax3.plot(durations5, dr5.loc["YTM", :] * 100, color="#134c67", ls="--")

ax1.xaxis.set_major_locator(mticker.MaxNLocator(nbins=8))
ax1.axes.xaxis.set_ticklabels([a for a in range(7, 25, 2)]) #optional

ax2.axes.xaxis.set_ticklabels([a for a in range(1, 19, 2)]) #optional
ax2.xaxis.set_major_locator(mticker.MaxNLocator(nbins=8))
ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=4))

ax3.axes.xaxis.set_ticklabels([a for a in range(6, 25, 2)]) #optional
ax3.xaxis.set_major_locator(mticker.MaxNLocator(nbins=8))
ax3.yaxis.set_major_locator(mticker.MaxNLocator(nbins=4))

ax1.legend(prop=dict(size=10)).get_frame().set_alpha(0.6)
ax2.legend(loc=7, prop=dict(size=10)).get_frame().set_alpha(0.6)
ax3.legend(prop=dict(size=10)).get_frame().set_alpha(0.6)

plt.show()
