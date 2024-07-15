res = {'Annual return': 378126.8079310716, 'Cumulative returns': 0.22612273789537696, 'Annual volatility': 2.0746836512890066, 'Sharpe ratio': 9.156573968110553, 'Calmar ratio': 2354541430.983128, 'Stability': 0.7494090607814704, 'Max drawdown': -0.00016059467162282486, 'Omega ratio': 1409.2328630370305, 'Sortino ratio': 12906.667381983145, }

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

res1 = {}

for k,v in res.items():
	if is_number(v):
          v = round(v,3)
          print(v)
          res1[k] = v 
			
print(res1)