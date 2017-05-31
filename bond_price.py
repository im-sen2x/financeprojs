def coupon_pay(fv, cr, n):
	return  (fv * cr) / n

def annuity_operation(Coupon_Pay, ir,  n, T):
	Y = ir / n
	N = n * T

	return Coupon_Pay/Y *  (1 - 1/(1+Y)**N)

def maturity_operation(fv, ir, n, T):
	Y = ir / n
	N = n * T
	return fv / (1 + Y) ** N
