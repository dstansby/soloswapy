import astropy.units as u
from cdflib.cdfread import CDF as CDF_cdflib
from cdflib.epochs_astropy import CDFAstropy

__all__ = ['CDF']

unit_dict = {'Degrees': u.deg,
             'ElectronVolts': u.eV,
             'Counts/Accum': u.dimensionless_unscaled,
             'Total Counts': u.dimensionless_unscaled}


def parse_units(unit_str):
    if unit_str in unit_dict:
        return unit_dict[unit_str]
    return u.Unit(unit_str)


class CDF(CDF_cdflib):
    """
    `cdflib.CDF` with additional convenience methods and properties.
    """
    def varget_units(self, variable):
        """
        Get a variable as an astropy Quantity.
        """
        var = self.varget(variable)
        units = self.varattsget(variable)['UNITS']
        return var * parse_units(units)

    def varget_time(self, variable):
        """
        Get a variable and return it as astropy Time.
        """
        var = self.varget(variable)
        return CDFAstropy.convert_to_astropy(var)

    @property
    def descriptor(self):
        return self.globalattsget()['Descriptor']

    @property
    def zvars(self):
        return self.cdf_info()['zVariables']
