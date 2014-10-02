import os
import re
import logging
import string

from lcmutils import slashify

logger = logging.getLogger(__name__)


def make_lower(v):
    """makes a key lowercase

    >>> make_lower('ab')
    'ab'
    >>> make_lower('AB')
    'ab'
    >>> make_lower(('ab', 1, 'DE'))
    ('ab', 1, 'de')
    """

    if isinstance(v, str):
        v = v.lower()
    elif isinstance(v, tuple):
        v = tuple([make_lower(i) for i in v])
    return v


def wnshdb_ize(par):
    """
    >>> wnshdb_ize('32')
    'WNSHDB32'
    >>> wnshdb_ize('3')
    'WNSHDB3'
    """

    if par == ''.join([i for i in par if i in string.digits]):
        return 'WNSHDB' + str(int(par))
    return par


class ExtractLocationParameterFromMonDir:
    def __init__(self):
        
        self.expressions = {'instrument': {'section': re.compile(r'\[.*(?:Instrument.*header|Logger settings)', re.I),
                                           'id': re.compile(r'.*(?:Location|Locatie)[ \t]*=(.+)', re.I),
                                           },
                            'channel': {'section': re.compile(r'\[.*(?:Kanaal|Channel)[ ]*([0-9]+).*header', re.I),
                                        'id': re.compile(r'.*(?:Identification|Identificatie)[ ]+=(.+)', re.I),
                                        }}
        self.datastart_re = re.compile(r'\[Data\]')
        self.names = {'level': ['WNSHDB35', 'WNSHDB40'],
                      'pressure': ['WNSHDB35', 'WNSHDB40'],
                      'geleidbaarheid': ['WNSHDB27'],
                      'conductivity': ['WNSHDB27'],
                      'temperature': ['WNSHDB52'],
                      }
        pass

    def __call__(self, directory_name):
        """scan a directory for mon files and return a list of pairs
        """

        directory_name = slashify(directory_name)

        result = LcmDict()
        logger.debug("scanning %s for mon files" % directory_name)
        for filename in [k for k in os.listdir(directory_name) if k.lower().endswith('.mon')]:
            try:
                input = file(directory_name + filename)
                logger.debug("reading %s" % filename)
            except:
                logger.debug("unable to open %s" % filename)
                continue

            logger.debug("doing input file '%s'" % filename)
            objs = dict()
            in_section = None
            instrument_id = None
            objs[None] = []

            for line in input.xreadlines():
                line = line.strip("\n\r ")
                if not line:
                    continue

                if self.datastart_re.match(line):
                    logger.debug("we're done with this file, let's store the data collected.")
                    for instrument_id, parameter_ids in objs.items():
                        if not parameter_ids:
                            logger.warn("in '%s' found location '%s' with no parameters" % (filename, instrument_id))
                        elif instrument_id is None:
                            logger.warn("in '%s' found parameters '%s' for no location" % (filename, parameter_ids))
                        else:
                            for parameter_id in parameter_ids:
                                result[Pair(first=instrument_id,
                                            second=parameter_id).astuple()] = {'filename': filename}
                    break

                if line[0] == '[' and line[-1] == ']':
                    logger.debug("recognized line '%s' as the start of some section" % line)
                    in_section = None
                    for section in ['instrument', 'channel']:
                        if self.expressions[section]['section'].match(line):
                            in_section = section
                    logger.debug("we are now in section '%s'" % in_section)
                    continue

                if not in_section:
                    continue

                logger.debug("analyzing line '%s'" % line)
                at_identification = self.expressions[in_section]['id'].match(line)
                if at_identification:
                    if in_section == 'instrument':
                        instrument_id = at_identification.group(1).replace(' ', '')
                        objs[instrument_id] = []
                        logger.debug("found the id of instrument '%s'" % instrument_id)
                    elif in_section == 'channel':
                        channel_id = at_identification.group(1)
                        logger.debug("found channel '%s' for instrument '%s'" % (channel_id, instrument_id))
                        try:
                            parameter_ids = self.names[channel_id.lower().strip().split(' ')[-1]]
                        except KeyError, missing_key:
                            logger.debug("channel '%s' for instrument '%s' uses invalid name '%s'" % (channel_id, instrument_id, missing_key))
                            parameter_ids = []
                        for parameter_id in parameter_ids:
                            objs[instrument_id].append(parameter_id)
                            logger.debug("added parameter '%s' to instrument '%s'" % (parameter_id, instrument_id))

        return result


class LcmDict(dict):
    """a dictionary with a few more useful functions:

    >>> d = LcmDict()
    >>> 'project' in dir(d)
    True
    >>> 'matches' in dir(d)
    True
    >>> 'setcompatible' in dir(d)
    True
    >>> 'setresettable' in dir(d)
    True
    >>> 'join' in dir(d)
    True
    """

    def __init__(self, *args, **kwargs):
        """
        >>> d = LcmDict()
        >>> d._resettable
        set([])
        >>> d._altered
        set([])

        """
        dict.__init__(self, *args, **kwargs)
        items = [i for i in self.items()]
        self.clear()
        for k, v in items:
            k = make_lower(k)
            super(LcmDict, self).__setitem__(k, v)
        self._resettable = set()
        self._altered = set()

    def __setitem__(self, key, value):
        super(LcmDict, self).__setitem__(make_lower(key), value)

    def get(self, key, d=None):
        """

        keys in dictionary are case insensitive
        >>> d = LcmDict()
        >>> d['a'] = 1
        >>> d.get('A')
        1
        >>> d.get('B')

        works also with tuples!
        >>> d[('a', 1)] = 1
        >>> d.get(('A', 1))
        1
        >>> d.get(('B', 2))
        """

        return super(LcmDict, self).get(make_lower(key), d)

    def __getitem__(self, key):
        """
        >>> d = LcmDict()
        >>> d['a'] = 1
        >>> d['A']
        1
        >>>
        """
        return super(LcmDict, self).__getitem__(make_lower(key))

    def __contains__(self, key):
        """
        >>> d = LcmDict()
        >>> d['aa'] = 1
        >>> 'Aa' in d
        True
        >>> 'AA' in d
        True
        >>> 'aa' in d
        True
        >>> 'aA' in d
        True
        >>>
        """
        return super(LcmDict, self).__contains__(make_lower(key))

    def project(self, iterable, other=None):
        """returns a new dictionary with only the keys from iterable.

        if `other` is not None, it projects `other` instead of `self`.
        This can be used to project a normal python dictionary into a
        LcmDict.

        >>> d = LcmDict()
        >>> d[1] = 1
        >>> d[2] = 2
        >>> d.project([2,3])
        {2: 2}

        """

        if other is None:
            other = self
        faster = set(iterable)
        return LcmDict([(k, v) for (k, v) in other.iteritems() if k in faster])

    def setresettable(self, keys=None):
        """controls the behaviour of the setcompatible method.

        making a dictionary 'resettable' will allow accepting a
        conflicting definition.  after the first definition is
        received, the dictionary goes back to the normal behaviour:
        'non resettable'.

        >>> d = LcmDict()
        >>> d[1] = 5
        >>> d.setresettable()
        >>> d.setcompatible(1,6)
        True
        >>> d
        {1: 6}

        """

        if keys is None:
            keys = self.keys()
        elif isinstance(keys, types.StringTypes):
            keys = list(keys)
        for key in keys:
            if isinstance(self[key], LcmDict):
                self[key].setresettable()
        self._resettable = set(keys)
        self._altered = set()

    def setdefault(self, key, value):
        return super(LcmDict, self).setdefault(make_lower(key), value)

    def setcompatible(self, key, value):
        """controlled (re)definition of key.
        returns a boolean indicating if the key was redefined.

        if key is not already here: set the value.

        elif the new value is None: do nothing.

        elif the new value is unchanged: do nothing.

        elif both objects are dictionaries, update the old object
        redefining key by key.

        elif key is resettable: reset the entry and emit a warning.

        else emit a warning and associate key to None.

        makes the key not resettable.

        >>> d = LcmDict()
        >>> d[1] = 5
        >>> d.setresettable()
        >>> d.setcompatible(1,6)
        True
        >>> d
        {1: 6}
        >>> d.setcompatible(1,7)
        True
        >>> d
        {1: None}

        >>> d = LcmDict()
        >>> d[1] = 5
        >>> d
        {1: 5}
        >>> d.setcompatible(1,5)
        False
        >>> d
        {1: 5}

        >>> d = LcmDict()
        >>> d[1] = 5
        >>> d.setcompatible(1,6)
        True
        >>> d
        {1: None}

        setting something to None has no effect.
        >>> d = LcmDict()
        >>> d.setcompatible(1, None)
        False
        >>> 1 in d
        False
        >>> d.setcompatible(1, 6)
        True
        >>> d
        {1: 6}

        """

        key = make_lower(key)
        did_it = True
        if value is None:
            did_it = False
        elif key not in self:
            self[key] = value
            self._altered.add(key)
        elif value == self[key]:
            did_it = False
        elif isinstance(value, dict) and isinstance(self[key], LcmDict):
            logger.debug("update: redefining '%s' key by key." % key)
            # not sure whether we should consider two dictionaries equal or not...
            #did_it = False?
            for inner_key in sorted(value):
                logger.debug("update: redefining '%s'[%s]" % (key, inner_key))
                self[key].setcompatible(inner_key, value[inner_key])
        elif key in self._resettable:
            logger.info("modified field '%s' to %s" % (key, value))
            self._altered.add(key)
            self[key] = value
        elif self[key] is None:
            logger.debug("definition had already been removed.  no warning is necessary.")
        else:
            logger.warn("definitions of '%s' are incompatible (old: %s, new: %s).  removing." % (key, self[key], value))
            self[key] = None
        if did_it:
            self._resettable.discard(key)
        return did_it

    def matches(self, other):
        """check whether all common keys define the same values

        >>> d = LcmDict({1:1, 2:2, 3:3})
        >>> d.matches(d)
        True
        >>> e = LcmDict({2:2, 3:3, 4:4})
        >>> d.matches(e)
        True
        >>> f = LcmDict({1:3, 3:2, 4:4})
        >>> f.matches(e)
        False
        >>> f.matches(d)
        False
        """

        my_key_set = set(self.iterkeys())
        other_key_set = set(other.iterkeys())
        common_key_set = my_key_set & other_key_set
        return self.project(common_key_set) == self.project(common_key_set, other)

    def update(self, other):
        "redefining a dictionary value, updates rather than overwrites"

        for key, value in other.items():
            if isinstance(value, dict):
                # this will raise an exception if self[key] is already
                # present and is not a dict
                self.setdefault(key, LcmDict()).update(value)
            else:
                self[key] = value

    def join(self, key, field, values):
        """adds `field` to self.

        joining on numeric values
        >>> this = LcmDict({1:1, 2:2, 3:3})
        >>> this.join(1, 4, {1: 1.5, 33: 1.5})
        >>> this[4]
        1.5
        >>> this.join(2, 5, {1: 1.5, 33: 1.5})
        >>> this.get(5)

        the field is there, the value is None
        >>> this[5]

        joining on string values
        >>> this = LcmDict({1:'AA', 2:'bb', 3:'Cc'})
        >>> other = LcmDict({'aa': 1.5, 'BB': 1.25, 'c+': 2})

        match is case insensitive
        >>> this.join(1, 4, other)
        >>> this.get(4)
        1.5
        >>> this.join(2, 5, other)
        >>> this.get(5)
        1.25

        values dictionary can use regular expressions in keys
        >>> this.join(3, 6, other)
        >>> this.get(6)
        2
        >>>
        """

        if key in self:
            self.setdefault(field, None)
            if self[key] in values:
                self[field] = values[self[key]]
            elif isinstance(self[key], str):
                for extern in values.keys():
                    import re
                    if re.match('^' + extern + '$', self[key], re.IGNORECASE):
                        self[field] = values[extern]


class Pair:
    """2-tuple with a few tricks useful here in the LCM.

    >>> d = Pair()
    >>> 'iscomplete' in dir(d)
    True
    >>> 'astuple' in dir(d)
    True
    >>> 'astuplelist' in dir(d)
    True

    """
    def __init__(self, name=None, delim=None, ploc=None, ppar=None, first=None, second=None):
        """

        per default, a Pair contains nothing.
        >>> a = Pair()
        >>> a.first == a.second == None
        True

        you can initialize it with a file name, indicating how to split it:
        >>> filename, delim, loc_field_no, para_field_no = 'test_abc_m23_2.txt', '_', 2, 1
        >>> a = Pair(filename, delim, loc_field_no, para_field_no)
        >>> a.first
        'MPN23'
        >>> a.second
        'abc'

        or you can initialize its parts explicitly
        >>> Pair(first='123', second='654').first
        '123'

        >>> Pair(first='test', second='2').first
        'test'

        """
        if first and second:
            self.first = first
            self.second = second
            return
        if not (name is None or delim is None or ploc is None or ppar is None):
            parts = name.split(delim)
            self.first = 'MPN' + parts[ploc][1:]
            self.second = parts[ppar]
            return
        self.first = self.second = None

    def iscomplete(self):
        """
        >>> Pair().iscomplete()
        False
        >>> Pair(second='222').iscomplete()
        False
        >>> Pair(first='1', second='2').iscomplete()
        True
        """
        return not (self.first is None or self.second is None)

    def astuple(self):
        """
        >>> Pair(first='test', second='2').astuple()
        ('TEST', 'WNSHDB2')
        """
        return self.first.upper(), wnshdb_ize(self.second)

    def astuplelist(self):
        """a Pair can contain as second coordinate a list.
        >>> Pair(first='test', second=['2']).astuplelist()
        [('TEST', 'WNSHDB2')]
        >>> Pair(first='test', second=['1', '2', '3']).astuplelist()
        [('TEST', 'WNSHDB1'), ('TEST', 'WNSHDB2'), ('TEST', 'WNSHDB3')]
        >>>
        """
        return [(self.first.upper(), wnshdb_ize(item)) for item in self.second]
