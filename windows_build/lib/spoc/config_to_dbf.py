import os
import logging

from dbfpy.dbf import Dbf

from spoc import models
from spoc.config_fields import dbf_configuration
from django.conf import settings

logger = logging.getLogger(__name__)


def add_field(dbf_file, field_options):
    dbf_file.addField(tuple(field_options))


def new_record(dbf_file):
    return dbf_file.newRecord()


def store_record(rec):
    rec.store()


def store_headers(out, location, headers):
    for header in headers:
        bron = location.oei_location.sort.sort
        id = location.oei_location.locationid
        naam =  location.oei_location.locationname
        gpgin = location.oei_location.gpgin
        gpguit = location.oei_location.gpguit
        gpginzp = location.oei_location.gpginzp
        gpginwp = location.oei_location.gpginwp
        gpguitzp = location.oei_location.gpguitzp
        gpguitwp = location.oei_location.gpguitwp
        status = location.oei_location.status
        debitf = location.oei_location.debitf
        datumbg = location.oei_location.datumbg
        regelbg = location.oei_location.regelbg
        inlaatf = location.oei_location.inlaatf
        x = location.oei_location.x
        y = location.oei_location.y
        
        if None in [bron, id, naam, gpgin]:
            logger.warn(
                "Escape header due None value by LOCATION - '{}'".format(id))
            continue

        rec = out.newRecord()
        rec['BRON'] = str(bron)
        rec['ID'] = str(id)
        rec['NAAM'] = str(naam)
        rec['SOORT_OBJE'] = str(bron) if bron is not None else ''
        rec['X'] = x if x is not None else 0
        rec['Y'] = y if y is not None else 0
        rec['GPGIN'] = str(gpgin) if gpgin is not None else ''
        rec['GPGINZP'] = str(gpginzp) if gpginzp is not None else ''
        rec['GPGINWP'] = str(gpginwp) if gpginwp is not None else ''
        rec['GPGUIT'] = str(gpguit) if gpguit is not None else ''
        rec['GPGUITZP'] = str(gpguitzp) if gpguitzp is not None else ''
        rec['GPGUITWP'] = str(gpguitwp) if gpguitwp is not None else ''
        rec['DEBITF'] = str(debitf) if debitf is not None else ''
        rec['STATUS'] = str(status) if status is not None else ''
        rec['DATUM_BG'] = str(datumbg) if datumbg is not None else ''
        rec['REGEL_BH'] = str(regelbg) if regelbg is not None else ''
        rec['INLAAT_F'] = str(inlaatf) if inlaatf is not None else ''
        rec['REF_H'] = ''
        rec['BARO'] = ''

        parameter = header.parameter
        if parameter is None:
            continue
        
        rec[str(parameter.id.upper())] = parameter.id

        validations = header.validation_set.all()
        for validation in validations:
            key = "{0}{1}".format(validation.field.field.prefix, parameter.id.upper())
            rec[key] = validation.value
        rec.store()


def store_data(out):
    locations = models.Location.objects.filter(fews=True)
    for location in locations:
        if location.oei_location is None:
            continue
        if location.scada_location is None:
            continue
        headers = location.scada_location.headers.all()
        if headers.exists() is False:
            continue
        
        store_headers(out, location, headers)
        

def fields_to_dbf(out):
    """
    Adds fields into dbf file.
    """
    dbf_fields = dbf_configuration()
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
            dbf_filepath = os.path.join(settings.DBF_DIR, 'configuratie.dbf')
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
