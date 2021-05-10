import os
import re
from gzip import GzipFile



def getTempDir():
	import tempfile
	return tempfile.gettempdir()+os.sep

def getFileExt(filename):
	extension = os.path.splitext(filename)[1][1:]
	return extension

def getXMLfromP7m(filename):
    from OpenSSL import crypto
    from OpenSSL._util import (
        ffi as _ffi,
        lib as _lib,
    )

    # Or, alternatively:
    # from cryptography.hazmat.bindings.openssl.binding import Binding
    # _lib = Binding.lib
    # _ffi = Binding.ffi

    with open(filename, 'rb') as f:
        p7data = f.read()
    #p7 = crypto.load_pkcs7_data(crypto.FILETYPE_ASN1, p7data)
    p7 = crypto.load_pkcs7_data(crypto.FILETYPE_ASN1, p7data)

    bio_out =crypto._new_mem_buf()
    res = _lib.PKCS7_verify(p7._pkcs7, _ffi.NULL, _ffi.NULL, _ffi.NULL, bio_out, _lib.PKCS7_NOVERIFY)

    '''
    if res == 1:
        databytes = crypto._bio_to_string(bio_out)
        databytes = databytes.decode('utf8')
        databytes = databytes.replace('\ufeff', "")
        print(databytes)

    else:
        errno = _lib.ERR_get_error()
        errstrlib = _ffi.string(_lib.ERR_lib_error_string(errno))
        errstrfunc = _ffi.string(_lib.ERR_func_error_string(errno))
        errstrreason = _ffi.string(_lib.ERR_reason_error_string(errno))
    '''

    databytes = crypto._bio_to_string(bio_out)
    xmlFileName=getTempDir()+'tmpFatt.xml'
    open(xmlFileName, 'wb').write(databytes)


    return xmlFileName
