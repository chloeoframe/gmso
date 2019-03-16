import warnings
from topology.exceptions import TopologyError

class Connection(object):
    """ An abstract object that lists bonded partners and their type
    This functions as a super-class for any bonded groups (bonds,
    angles, dihedrals, etc), with a property for the conection_typie
    
    Parameters
    ----------
    bond_partners : list of topology.Site
        A list of constituents in this bond. Should be in order
    connection_type : topology.Potential
        An instance of topology.Potential that describes
        the potential function and parameters of this interaction
        """
    def __init__(self, bond_partners=[], connection_type=None):
        self._bond_partners = _validate_bond_partners(bond_partners)
        self._connection_type = _validate_connection_type(connection_type)
        self._update_partners()

    @property
    def bond_partners(self):
        return self._bond_partners

    @bond_partners.setter
    def bond_partners(self, bond_partners):
        self._bond_partners = _validate_bond_partners(bond_partners)

    @property
    def connection_type(self):
        return self._connection_type

    @connection_type.setter
    def connection_type(self, ctype):
        self_connection_type = _validate_connection_type(ctype)

    def _update_partners(self):
        for partner in self.bond_partners:
            if self not in partner.connections:
                partner.add_connection(self)

    def __repr__(self):
        descr = '<{}-partner Connection, id {}, '.format(
                len(self.bond_partners), id(self))
        descr += 'type {}>'.format(self.connection_type)
        return descr

    def __eq__(self, other):
        bond_partner_match = (self.bond_partners == other.bond_partners)
        ctype_match = (self.connection_type == other.connection_type)
        return all([bond_partner_match, ctype_match])


def _validate_bond_partners(bond_partners):
    from topology.core.site import Site
    for partner in bond_partners:
        if not isinstance(partner, Site):
            raise TopologyError("Supplied non-Site {}".format(partner))
    return bond_partners

def _validate_connection_type(c_type):
    from topology.core.potential import Potential
    if c_type is None:
        warnings.warn("Non-parametrized Connection detected")
    elif not isinstance(c_type, Potential):
        raise TopologyError("Supplied non-Potential {}".format(c_type))
    return c_type
