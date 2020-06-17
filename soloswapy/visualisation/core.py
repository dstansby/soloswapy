import astropy.units as u
import matplotlib.colors as mcolor
import matplotlib.pyplot as plt
from matplotlib import widgets
import numpy as np


class DistributionFunctionVisualiser:
    def __init__(self, distribution, energies='all'):
        """
        Parameters
        ----------
        distribution : DistributionFunctionBase
        energies : str, list
            The minimum and maximum energy bin to limit plotting to.
        """
        # Indexing is [time, elevation, energy, azimuth]
        self._dist = distribution
        # Parse energies
        if energies == 'all':
            energies = [0, self._dist.counts.shape[2]]
        ntime = self._dist.counts.shape[0]
        nenergy = energies[1] - energies[0]
        eidxs = list(range(*energies))

        nax = int(np.ceil(np.sqrt(nenergy)))
        # Calculate number of axes
        fig, axs = plt.subplots(nax, nax, gridspec_kw={'bottom': 0.2})
        axs_rav = axs.ravel()[::-1]
        for ax in axs_rav:
            ax.set_aspect('equal')
            ax.set_axis_off()

        tidx = 1
        ims = {}
        for eidx, ax in zip(eidxs, axs_rav):
            im = ax.imshow(self._dist.counts[tidx, :, eidx, :].value,
                           norm=mcolor.LogNorm())
            ims[eidx] = im
            ax.set_title(self._e_str(tidx, eidx))

        # Add slider
        axtime = plt.axes([0.1, 0.1, 0.65, 0.03])
        stime = widgets.Slider(axtime, 'Time', valmin=0, valmax=ntime - 1,
                               valinit=tidx, valstep=1)

        # Add update function for slider
        def update(val):
            tidx = int(stime.val)
            for eidx, ax in zip(eidxs, axs_rav):
                ims[eidx].set_data(self._dist.counts[tidx, :, eidx, :].value)
            ax.set_title(self._e_str(tidx, eidx))
            stime.valtext.text = str(self._dist.times[tidx])

        stime.on_changed(update)
        plt.show()

    def _e_str(self, tidx, eidx):
        return str(int(self._dist.energy[tidx, eidx].to_value(u.eV))) + ' eV'


class PitchAngleVisualiser:
    def __init__(self, distribution, energies='all'):
        """
        Parameters
        ----------
        distribution : DistributionFunctionBase
        energies : str, list
            The minimum and maximum energy bin to limit plotting to.
        """
        # Indexing is [time, elevation, energy, azimuth]
        self.dist = distribution
        # Parse energies
        if energies == 'all':
            energies = [0, self.dist.total_counts.shape[2]]
        ntime = self.dist.total_counts.shape[0]
        nenergy = energies[1] - energies[0]
        eidxs = list(range(*energies))

        # Calculate number of axes
        fig, axs = plt.subplots(
            nenergy, 1, gridspec_kw={'bottom': 0.1, 'hspace': 0.02},
            sharex=True, sharey=True
        )
        axs_rav = axs.ravel()[::-1]
        tidx = 1
        ims = []
        for eidx, ax in zip(eidxs, axs_rav):
            im = ax.pcolormesh(self.dist.times[1:].to_datetime(),
                               self.dist.azimuth.to_value(u.deg),
                               self.dist.total_counts[1:, 0, eidx, :].value.T,
                               norm=mcolor.LogNorm())
            # ims.append(im)
            ax.text(-0.1, 0.5, self._e_str(tidx, eidx), transform=ax.transAxes, ha='center')
            # ax.set_aspect('equal')
            ax.set_axis_off()
        axs_rav[0].set_axis_on()

        plt.show()

    def _e_str(self, tidx, eidx):
        return str(int(self.dist.energy[tidx, eidx].to_value(u.eV))) + ' eV'
