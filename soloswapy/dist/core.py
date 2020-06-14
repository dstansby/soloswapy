import abc

from .util import CDF


registry = []


class DistributionFunctionBase(abc.ABC):
    @abc.abstractmethod
    def peek(self):
        """
        Show an interactive overview of the data.
        """

    @staticmethod
    @abc.abstractmethod
    def _is_source_for(cdf):
        """
        Return True if class is a source for *cdf*.
        """


class DistributionFunctionFactory:
    """
    A distribution function.
    """
    def __init__(self):
        pass

    def __call__(self, fname):
        """
        Parameters
        ----------
        fname : path-like
            Path to a .cdf file.
        """
        cdf = CDF(fname)
        sources = [cls for cls in registry if cls._is_source_for(cdf)]
        if len(sources) > 1:
            raise RuntimeError('CDF file matched more than one source')
        elif len(sources) == 0:
            raise RuntimeError('No sources found for CDF file')
        return sources[0](cdf)


DistributionFunction = DistributionFunctionFactory()
