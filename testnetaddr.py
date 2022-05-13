from OuiLookup import OuiLookup

man = list(OuiLookup().query("fc:04:1c:98:6a:c7")[0].values())[0]
print(man)

