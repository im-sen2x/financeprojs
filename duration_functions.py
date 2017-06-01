"""Helper Function"""

import pandas as pd
import bond_price as bp

def p_value(fv, ir, n, semesters):
	return fv / (1 + ir/n) ** semesters

def get_semesters(num_semesters, name):
	return pd.Series([s for s in range(1, num_semesters + 1)] , name=name)

def get_cashflows(num_sems, fv, cr, periods, name):
	flows = []
	cf = 0

	for n in range(num_sems):
		if n + 1 == num_sems:
			cf = bp.coupon_pay(fv, cr, periods) + fv
		else:
			cf = bp.coupon_pay(fv, cr, periods)
		flows.append(cf)

	return pd.Series(flows, name=name)

def get_present_value(cash_flows, ir, n, semesters, name):
	return pd.Series(p_value(cash_flows, ir, n, semesters), name=name)

def get_weight(present_value, pv_sum, name):
	return pd.Series(present_value / pv_sum, name=name)

def get_weightT(weight, semesters, name):
	return pd.Series(weight * semesters, name=name)



