from soloswapy.dist import DistributionFunction
import matplotlib.pyplot as plt

dist = DistributionFunction('/Users/dstansby/Data/solo/swa/eas/solo_L1_swa-eas-2DBurstc_20200606063947-20200606190451_V01.cdf')
print(dist.times.isot)
