import os
import logging

from dbfpy.dbf import Dbf

from spoc import models
from spoc.config_fields import dbf_debiet
from django.conf import settings

logger = logging.getLogger(__name__)


def add_field(dbf_file, field_options):
    dbf_file.addField(tuple(field_options))


def new_record(dbf_file):
    return dbf_file.newRecord()


def store_record(rec):
    rec.store()


def store_formulas(out, location, formulas):
    for formula in formulas:
        id = location.scada_location.locationid
        name = location.scada_location.locationname
        start = formula.dstart
        end = formula.dstop
        debitf = formula.formula_type.code
        coef01 = formula.coef01
        coef02 = formula.coef02
        coef03 = formula.coef03
        coef04 = formula.coef04
        coef05 = formula.coef05
        coef06 = formula.coef06
        coef07 = formula.coef07
        coef08 = formula.coef08
        coef09 = formula.coef09
        coef10 = formula.coef10
        coef11 = formula.coef11
        coef12 = formula.coef12

        rec = out.newRecord()
        rec['ID'] = str(id)
        rec['NAAM'] = str(name)
        rec['DATE_START'] = start if start is not None else ''
        rec['DATE_END'] = end if end is not None else ''
        rec['DEBIETF'] = str(debitf) if debitf is not None else ''
        
        rec['COEF01'] = coef01 if coef01 is not None else ''
        rec['COEF02'] = coef02 if coef02 is not None else ''
        rec['COEF03'] = coef03 if coef03 is not None else ''
        rec['COEF04'] = coef04 if coef04 is not None else ''
        rec['COEF05'] = coef05 if coef05 is not None else ''
        rec['COEF06'] = coef06 if coef06 is not None else ''
        rec['COEF07'] = coef07 if coef07 is not None else ''
        rec['COEF08'] = coef08 if coef08 is not None else ''
        rec['COEF09'] = coef09 if coef09 is not None else ''
        rec['COEF10'] = coef10 if coef10 is not None else ''
        rec['COEF11'] = coef11 if coef11 is not None else ''
        rec['COEF12'] = coef12 if coef12 is not None else ''

        rec.store()


def store_data(out):
    locations = models.Location.objects.filter(fews=True)
    for location in locations:
        if location.oei_location is None:
            continue

        if location.scada_location is None:
            continue
        
        formulas = models.HeaderFormula.objects.filter(
            header__location=location.scada_location)
        if formulas.exists() is False:
            continue
        
        store_formulas(out, location, formulas)
        

def fields_to_dbf(out):
    """
    Adds fields into dbf file.
    """
    dbf_fields = dbf_debiet()
    for field in dbf_fields:
        out.addField(field)


def create_dbf():
    """
    Creates a dbf file.
    """
    success = False

    try:
        if settings.DBF_DIR is None:
            logger.error('DBF_DIR setting is NOT available')
            return
        else:
            dbf_filepath = os.path.join(settings.DBF_DIR, 'configuratie_debietberekening.dbf')
        logger.info("Create en open dbf file='{}'.".format(dbf_filepath))
        out = Dbf(dbf_filepath, new=True)
        logger.info("Add fields.")
        fields_to_dbf(out)
        logger.info("Store data.")
        store_data(out)
        logger.info("Close file.")
        out.close()
        success = True
    except Exception as ex:
        logger.error(','.join(map(str, ex.args)))
        return success
