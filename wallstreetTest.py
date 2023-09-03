from wallstreet import Stock,Call,Put

g = Call('GooG',d=8,m=9,y=2023,strike=140)

print(123)
print('Google Option Strike 140',g.price)
print('Google Option Delta',g.delta())
print('Google Option Gamma',g.gamma())
print(g.strikes)