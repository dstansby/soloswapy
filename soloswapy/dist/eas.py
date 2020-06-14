import astropy.units as u
import cdflib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolor

from .core import registry, DistributionFunctionBase
from soloswapy.visualisation import DistributionFunctionVisualiser

__all__ = ['EAS3DDistribution']


class EAS3DDistribution(DistributionFunctionBase):
    def __init__(self, cdf):
        """
        Parameters
        ----------
        cdf : CDF
            An open CDF file.
        """
        if not self._is_source_for(cdf):
            raise ValueError('This is not a source for the given CDF')

        self._times = cdf.varget_time('SWA_EAS1_SCET')
        self._elevation = cdf.varget_units('SWA_EAS_ELEVATION')
        self._azimuth = cdf.varget_units('SWA_EAS_AZIMUTH')
        self._energy = cdf.varget_units('SWA_EAS1_ENERGY')
        self._data = cdf.varget_units('SWA_EAS1_Data')

    @property
    def times(self):
        """
        Times of the measurements.
        """
        return self._times

    @property
    def elevation(self):
        """
        Elevation angles of the measurements.
        """
        return self._elevation

    @property
    def azimuth(self):
        """
        Azimuthal angles of the measurements.
        """
        return self._azimuth

    @property
    def energy(self):
        """
        Energies of the measurements.
        """
        return self._energy

    @property
    def counts(self):
        """
        Indexing is [time, elevation, energy, azimuth]
        """
        return self._data

    def peek(self):
        """
        Show an interactive overview of the data.
        """
        anim = DistributionFunctionVisualiser(self)
        plt.show()

    @staticmethod
    def _is_source_for(cdf):
        """
        Returns true if *cdf* is a 3D EAS distribution function.
        """
        return cdf.descriptor == 'SWA-EAS1-NMc'


class EAS2DPitchAngles(DistributionFunctionBase):
    def __init__(self, cdf):
        """
        Parameters
        ----------
        cdf : CDF
            An open CDF file.
        """
        if not self._is_source_for(cdf):
            raise ValueError('This is not a source for the given CDF')

        print(cdf.zvars)

        self._times = cdf.varget_time('SWA_EAS1_SCET')
        self._elevation = cdf.varget_units('SWA_EAS_ELEVATION')
        self._elevation_d_upper = cdf.varget_units('SWA_EAS_ELEVATION_delta_upper')
        self._elevation_d_lower = cdf.varget_units('SWA_EAS_ELEVATION_delta_lower')
        self._azimuth = cdf.varget_units('SWA_EAS_AZIMUTH')
        self._energy = cdf.varget_units('SWA_EAS_ENERGY')
        self._mod = cdf.varget_units('SWA_EAS_Mode')
        self._data = cdf.varget_units('SWA_EAS1_Data')

    @property
    def times(self):
        """
        Times of the measurements.
        """
        return self._times

    @property
    def elevation(self):
        """
        Elevation angles of the measurements.
        """
        return self._elevation

    @property
    def azimuth(self):
        """
        Azimuthal angles of the measurements.
        """
        return self._azimuth

    @property
    def energy(self):
        """
        Energies of the measurements.
        """
        return self._energy

    @property
    def total_counts(self):
        """

        """
        return self._data

    def peek(self):
        anim = DistributionFunctionVisualiser(self)
        plt.show()

    @staticmethod
    def _is_source_for(cdf):
        """
        Returns true if *cdf* is a EAS 2D pitch angle product.
        """
        return cdf.descriptor == 'SWA-EAS-2DBurstc'


registry += [EAS3DDistribution, EAS2DPitchAngles]
