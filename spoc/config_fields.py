"""
Contain list of tuples with fields metadata
for fews configuration dbf-file
"""

from spoc import models



def dbf_configuration():
    """Return dbf fields for configuration.dbf."""
    dbf_fields = [
        ('BRON','C',25),
        ('ID','C',10),
        ('NAAM','C',53),
        ('SOORT_OBJE','C',25),
        ('X','N',18,2),
        ('Y','N',19,2),
        ('GPGIN','C',10),
        ('GPGINZP','C',5),
        ('GPGINWP','C',5),
        ('GPGUIT','C',10),
        ('GPGUITZP','C',5),
        ('GPGUITWP','C',5),
        ('DEBITF','C',25),
        ('STATUS','C',25),
        ('DATUM_BG','C',25),
        ('REGEL_BH','C',30),
        ('INLAAT_F','C',30),
        ('REF_H','C',20),
        ('BARO','C',20),
    ]
    t = 'C'
    l = 20
    parameters = models.Parameter.objects.all()
    for parameter in parameters:
        dbf_fields.append((parameter.id, t, l))
        validation_fields = parameter.validationfield_set.values_list(
            *['field__prefix', 'parameter__id']).order_by('field__name')
        for field in validation_fields:
            dbf_fields.append(("".join(field), t, l))
    return dbf_fields


def dbf_debiet():
    """Return dbf fields for debietbereking.dbf."""
    dbf_fields = [
        ('ID','C',10),
        ('NAAM','C',53),
        ('DATE_START','C',20),
        ('DATE_END','C',20),
        ('DEBIETF','C', 20),
    ]
    # add 12 COEF-fields
    for i in range(1, 10):
        dbf_fields.append(('COEF0{}'.format(i),'C','20'))
    for i in range(10, 13):
        dbf_fields.append(('COEF{}'.format(i),'C','20'))
    return dbf_fields
