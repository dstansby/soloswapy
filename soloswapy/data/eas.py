import astropy.units as u
import cdflib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolor
import pandas as pd
from sunpy.timeseries import GenericTimeSeries


from .core import registry, DistributionFunctionBase, DataBase
from soloswapy.visualisation import DistributionFunctionVisualiser, PitchAngleVisualiser

__all__ = ['EAS3DDistribution', 'EAS2DPitchAngles', 'EASPartialMoms']


class EASDistribution(DistributionFunctionBase):
    pass


class EAS3DDistribution(EASDistribution):
    def __init__(self, cdf):
        """
        Parameters
        ----------
        cdf : CDF
            An open CDF file.
        """
        self.cdf = cdf
        if not self._is_source_for(cdf):
            raise ValueError('This is not a source for the given CDF')

        self._times = cdf.varget_time('SWA_EAS1_SCET')
        self._elevation = cdf.varget_units('SWA_EAS_ELEVATION')
        self._azimuth = cdf.varget_units('SWA_EAS_AZIMUTH')
        self._energy = cdf.varget_units('SWA_EAS1_ENERGY')
        self._data = cdf.varget_units('SWA_EAS1_Data')

    def __add__(self, other):
        raise NotImplementedError()

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

    def peek(self, energies='all'):
        """
        Show an interactive overview of the data.
        """
        anim = DistributionFunctionVisualiser(self, energies)
        plt.show()

    @staticmethod
    def _is_source_for(cdf):
        """
        Returns true if *cdf* is a 3D EAS distribution function.
        """
        return cdf.descriptor == 'SWA-EAS1-NMc'


class EAS2DPitchAngles(EASDistribution):
    def __init__(self, cdf):
        """
        Parameters
        ----------
        cdf : CDF
            An open CDF file.
        """
        self.cdf = cdf
        if not self._is_source_for(cdf):
            raise ValueError('This is not a source for the given CDF')

        self._times = cdf.varget_time('SWA_EAS_SCET')
        self._elevation = cdf.varget_units('SWA_EAS_ELEVATION')
        # self._elevation_d_upper = cdf.varget_units('SWA_EAS_ELEVATION_delta_upper')
        # self._elevation_d_lower = cdf.varget_units('SWA_EAS_ELEVATION_delta_lower')
        self._azimuth = cdf.varget_units('SWA_EAS_AZIMUTH')
        self._energy = cdf.varget_units('SWA_EAS_ENERGY')
        self._data = cdf.varget_units('SWA_EAS_BM_Data')

        self._mode = cdf.varget('SWA_EAS_Mode')
        self._validity = cdf.varget('SWA_EAS_Validity')
        self._eas_used = cdf.varget('SWA_EAS_EasUsed')
        self._elevation_used = cdf.varget('SWA_EAS_ElevationUsed')
        self._mag_data = cdf.varget_units('SWA_EAS_MagDataUsed')

    def __add__(self, other):
        raise NotImplementedError()

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
        Indexing is [time, elevation, energy, azimuth]
        """
        return self._data

    def peek(self):
        vis = PitchAngleVisualiser(self)
        plt.show()

    @staticmethod
    def _is_source_for(cdf):
        """
        Returns true if *cdf* is a EAS 2D pitch angle product.
        """
        return cdf.descriptor == 'SWA-EAS-2DBurstc'


class EASPartialMoms(DataBase):
    def __init__(self, cdf):
        """
        Parameters
        ----------
        cdf : CDF
            An open CDF file.
        """
        self.cdf = cdf
        if not self._is_source_for(cdf):
            raise ValueError('This is not a source for the given CDF')

        times1 = cdf.varget_time('SWA_EAS1_SCET')
        # times2 = cdf.varget_time('SWA_EAS2_SCET')

        # TODO: extract head 2 data
        df1 = pd.DataFrame(index=times1.to_datetime())
        units1 = {}
        for var in cdf.zvars:
            if 'SWA_EAS1' in var:
                if var[-1] == 'N':
                    var_data = cdf.varget_units(var)
                    df1[var] = var_data.value
                    units1[var] = var_data.unit
                elif var[-1] == 'V':
                    var_data = cdf.varget_units(var)
                    for i in range(3):
                        var_name = f'{var}_{i}'
                        df1[var_name] = var_data[:, i]
                        units1[var_name] = var_data.unit
                elif var[-1] == 'P':
                    var_data = cdf.varget_units(var)
                    for i in range(6):
                        var_name = f'{var}_{i}'
                        df1[var_name] = var_data[:, i]
                        units1[var_name] = var_data.unit
                elif var[-1] == 'H':
                    var_data = cdf.varget_units(var)
                    for i in range(3):
                        var_name = f'{var}_{i}'
                        df1[var_name] = var_data[:, i]
                        units1[var_name] = var_data.unit
        self.ts1 = GenericTimeSeries(df1, units=units1)

    def __add__(self, other):
        raise NotImplementedError()

    def peek(self):
        fig, axs = plt.subplots(nrows=4, sharex=True)
        for var in self.ts1.to_dataframe():
            for var_type, ax in zip(['N', 'V', 'P', 'H'], axs):
                if var[-1] == var_type or var[-3] == var_type:
                    ax.plot(self.ts1.index, self.ts1.quantity(var), label=var)

        for ax in axs:
            ax.legend()
        plt.show()

    @staticmethod
    def _is_source_for(cdf):
        """
        Returns true if *cdf* is a EAS partial moments.
        """
        return cdf.descriptor == 'SWA-EAS-PartMoms'


registry += [EAS3DDistribution, EAS2DPitchAngles, EASPartialMoms]
