import astropy.units as u
import matplotlib.colors as mcolor
import matplotlib.pyplot as plt
from matplotlib import widgets


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

        # Calculate number of axes
        fig, axs = plt.subplots(8, 8, gridspec_kw={'bottom': 0.2})
        axs_rav = axs.ravel()[::-1]
        tidx = 1
        ims = []
        for eidx, ax in zip(eidxs, axs_rav):
            im = ax.imshow(self._dist.counts[tidx, :, eidx, :].value,
                           norm=mcolor.LogNorm())
            ims.append(im)
            ax.set_title(self._e_str(tidx, eidx))
            ax.set_aspect('equal')
            ax.set_axis_off()

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
