from .. import weapons


def create_feature(**params):
    """Create a new subclass of ``Feature`` with given default parameters.
    
    Useful for features that haven't been entered into the ``features.py``
    file yet.
    
    Parameters
    ----------
    params : optional
      Saved as attributes of the new class.
    
    Returns
    -------
    NewFeature
      New feature class, subclass of ``Feature``, with given params.
    """
    NewFeature = type('UnknownFeature', (Feature,), params)
    return NewFeature


class Feature():
    """
    Provide full text of rules in documentation
    """
    name = "Generic Feature"
    owner = None
    source = ''  # race, class, background, etc.
    spells_known = ()
    spells_prepared = ()
    needs_implementation = False  # Set to True if need to find way to compute stats

    def __init__(self, owner=None):
        self.owner = owner
        self.spells_known = [S() for S in self.spells_known]
        self.spells_prepared = [S() for S in self.spells_prepared]

    def __eq__(self, other):
        return (self.name == other.name) and (self.source == other.source)

    def __hash__(self):
        return 0

    def __str__(self):
        return self.name

    def __repr__(self):
        return "\"{:s}\"".format(self.name)
    
    def weapon_func(self, weapon: weapons.Weapon, **kwargs):
        """
        Updates weapon based on the Feature property

        Parameters
        ----------
        weapon
           The weapon to be tested for special bonuses
        kwargs
           Any other key-word arguments the function may require

        Returns
        -------
        weapon
            Updated weapon (perhaps changed damage bonus, etc.)

        """
        return weapon


class FeatureSelector(Feature):
    """
    A feature with multiple possible choices.
    """
    options = dict()
    name = ''
    source = ''

    def __new__(t, owner, feature_choices=[]):
        # Look for matching feature_choices
        new_feat = Feature.__new__(Feature, owner=owner)
        new_feat.__doc__ = t.__doc__
        new_feat.name = t.name
        new_feat.source = t.source
        new_feat.needs_implementation = True
        for selection in feature_choices:
            if selection.lower() in t.options:
                new_feat = t.options[selection.lower()](owner=owner)
                new_feat.source = t.source
        return new_feat
