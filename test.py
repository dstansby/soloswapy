from soloswapy.dist import DistributionFunction
import matplotlib.pyplot as plt

dist = DistributionFunction('/Users/dstansby/Data/solo/swa/eas/solo_L1_swa-eas1-NM3D_20200506121000-20200506191440_V01.cdf')
dist.peek(energies=[32, 60])
