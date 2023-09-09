import math

class BSM():

    def pdf(self, x):
        return math.exp(-x**2/2) / math.sqrt(2*math.pi)

    def cdf(self, x):
        return (1 + math.erf(x / math.sqrt(2))) / 2

    def d1(self, S, K, V, T):
        return (math.log(S / float(K)) + (V**2 / 2) * T) / (V * math.sqrt(T))

    def d2(self, S, K, V, T):
        return self.d1(S, K, V, T) - (V * math.sqrt(T))

    def theo(self, S, K, V, T, dT):
        if dT == 'C':
            return S * self.cdf(self.d1(S, K, V, T)) - K * self.cdf(self.d2(S, K, V, T))
        else:
            return K * self.cdf(-self.d2(S, K, V, T)) - S * self.cdf(-self.d1(S, K, V, T))

    def delta(self, S, K, V, T, dT):
        if dT == 'C':
            delta = self.cdf(self.d1(S, K, V, T))
        elif dT == 'P':
            delta = self.cdf(self.d1(S, K, V, T)) - 1
        else:
            delta = 1
        return delta

    def vega(self, S, K, V, T):
        vega = (S * math.sqrt(T) * self.pdf(self.d1(S, K, V, T))) / 100
        return vega

    def theta(self, S, K, V, T):
        theta = -((S * V * self.pdf(self.d1(S, K, V, T))) / (2 * math.sqrt(T))) / 365
        return theta

    def gamma(self, S, K, V, T):
        gamma = self.pdf(self.d1(S, K, V, T))/(S * V * math.sqrt(T))
        return gamma
    

class RiskBSM():

    def pdf(self, x):
        return math.exp(-x**2/2) / math.sqrt(2*math.pi)

    def cdf(self, x):
        return (1 + math.erf(x / math.sqrt(2))) / 2

    def d1(self, S, K, V, T, r):
        return (math.log(S / K) + (r + (V**2 / 2)) * T) / (V * math.sqrt(T))

    def d2(self, S, K, V, T, r):
        return self.d1(S, K, V, T, r) - (V * math.sqrt(T))

    def theo(self, S, K, V, T, dT, r):
        if dT == 'C':
            return S * self.cdf(self.d1(S, K, V, T, r)) - K * math.exp(-r * T) * self.cdf(self.d2(S, K, V, T, r))
        else:
            return K * math.exp(-r * T) * self.cdf(-self.d2(S, K, V, T, r)) - S * self.cdf(-self.d1(S, K, V, T, r))

    def delta(self, S, K, V, T, dT, r):
        if dT == 'C':
            delta = self.cdf(self.d1(S, K, V, T, r))
        elif dT == 'P':
            delta = self.cdf(self.d1(S, K, V, T, r)) - 1
        else:
            delta = 1
        return delta

    def vega(self, S, K, V, T, r):
        vega = (S * math.sqrt(T) * self.pdf(self.d1(S, K, V, T, r))) / 100
        return vega

    def theta(self, S, K, V, T, r):
        d1 = self.d1(S, K, V, T, r)
        d2 = self.d2(S, K, V, T, r)
        theta = -((S * V * self.pdf(d1)) / (2 * math.sqrt(T))) / 365 - r * K * math.exp(-r * T) * self.pdf(d2) / (2 * math.sqrt(T)) / 365
        return theta


    def gamma(self, S, K, V, T, r):
        d1 = self.d1(S, K, V, T, r)
        gamma = self.pdf(d1) / (S * V * math.sqrt(T))
        return gamma

