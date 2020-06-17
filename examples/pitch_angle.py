from soloswapy.data import load

moms = load('/Users/dstansby/Data/solo/swa/eas/solo_L1_swa-eas-2DBurstc_20200606063947-20200606190451_V01.cdf')
moms.peek(energies=[16, 32])
