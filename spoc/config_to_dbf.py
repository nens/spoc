import os
import logging

from dbfpy.dbf import Dbf

from spoc import models
from config_fields import DBF_FIELDS
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
        gpgident = location.oei_location.gpgident
        x = location.oei_location.x
        y = location.oei_location.y
        zp = str(location.oei_location.gpgzmrpl)
        wp = str(location.oei_location.gpgwntpl)
        
        if None in [bron, id, naam, gpgident]:
            logger.warn(
                "Escape header due None value by LOCATION - '{}'".format(id))
            continue
        if x is None:
            x = 0
        if y is None:
            y = 0

        rec = out.newRecord()
        rec['BRON'] = bron
        rec['ID'] = id
        rec['NAAM'] = naam
        rec['SOORT_OBJE'] = bron
        rec['X'] = x
        rec['Y'] = y
        
        rec['GPGIDENT'] = gpgident
        if zp is not None:
            rec['ZP'] = str(zp)
        if wp is not None:
            rec['WP'] = str(wp)

        scada = location.scada_location
        parameter = header.parameter
        hardmin = header.hardmin
        hardmax = header.hardmax
        
        if parameter is not None:
            rec['V{}'.format(parameter.id).upper()] = parameter.id
            if hardmin is not None:
                rec['B{}'.format(parameter.id).upper()] = str(hardmin)
            if hardmax is not None:
                rec['T{}'.format(parameter.id).upper()] = str(hardmax)
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
    for field in DBF_FIELDS:
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
