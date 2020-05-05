import os
import re
import struct
import numpy as np
import time

def read_Chemstation_file(fname):
    f = open(fname, "rb")

    f.seek(0x1075)
    sig_name = f.read(2 * struct.unpack(">B", f.read(1))[0]).decode("utf-16")
    # wavelength the file was collected at
    wv = sig_name #float(re.search("Sig=(\d+),(\d+)", sig_name).group(1))

    f.seek(0x127C)
    del_ab = struct.unpack(">d", f.read(8))[0]

    # data = np.array([])
    data = []

    f.seek(0x1800)
    while True:
        x, nrecs = struct.unpack(">BB", f.read(2))
        if x == 0 and nrecs == 0:
            break
        for _ in range(nrecs):
            inp = struct.unpack(">h", f.read(2))[0]
            if inp == -32768:
                inp = struct.unpack(">i", f.read(4))[0]
                data.append(del_ab * inp)
            elif len(data) == 0:
                data.append(del_ab * inp)
            else:
                data.append(data[-1] + del_ab * inp)

    # generate the time points if this is the first trace

    f.seek(0x244)
    yunits = f.read(struct.unpack(">B", f.read(1))[0]).decode()
    f.seek(0x11A)
    st_t = struct.unpack(">i", f.read(4))[0] / 60000.0
    en_t = struct.unpack(">i", f.read(4))[0] / 60000.0
    f.close()

    times = np.linspace(st_t, en_t, len(data))
    f.close()
    return wv, times, np.array(data)


# Constants used for binary file parsing
ENDIAN = '>'
STRING = ENDIAN + '{}s'
UINT8 = ENDIAN + 'B'
UINT16 = ENDIAN + 'H'
INT16 = ENDIAN + 'h'
INT32 = ENDIAN + 'i'

def chemstation_metadata(fname):
    file_ = open(fname, "rb")
    metadata = {}
    """Parse the header"""
    # Fields is a table of name, offset and type. Types 'x-time' and 'utf16' are specially
# handled, the rest are format arguments for struct unpack
    fields = (
        ('sequence_line_or_injection', 252, UINT16),
        ('injection_or_sequence_line', 256, UINT16),
        ('start_time', 282, 'x-time'),
        ('end_time', 286, 'x-time'),
        ('version_string', 326, 'utf16'),
        ('description', 347, 'utf16'),
        ('sample', 858, 'utf16'),
        ('operator', 1880, 'utf16'),
        ('date', 2391, 'utf16'),
        ('inlet', 2492, 'utf16'),
        ('instrument', 2533, 'utf16'),
        ('method', 2574, 'utf16'),
        ('software version', 3601, 'utf16'),
        ('software name', 3089, 'utf16'),
        ('software revision', 3802, 'utf16'),
        ('units', 4172, 'utf16'),
        ('detector', 4213, 'utf16'),
        ('yscaling', 4732, ENDIAN + 'd'))
        # Parse and check version
    length = struct.unpack(UINT8, file_.read(1))[0]
    parsed = struct.unpack(STRING.format(length), file_.read(length))
    version = int(parsed[0])
#     if version not in self.supported_versions:
#         raise ValueError('Unsupported file version {}'.format(version))
    metadata['magic_number_version'] = version

    # Parse all metadata fields
    for name, offset, type_ in fields:
        file_.seek(offset)
        if type_ == 'utf16':
            metadata[name] = parse_utf16_string(file_)
        elif type_ == 'x-time':
            metadata[name] = struct.unpack('>i', file_.read(4))[0] / 60000
        else:
            metadata[name] = struct.unpack(type_, file_.read(struct.calcsize(type_)))[0]

    # Convert date
    metadata['datetime'] = time.strptime(metadata['date'], '%d-%b-%y, %H:%M:%S')
    return metadata

def parse_utf16_string(file_, encoding='UTF16'):
    """Parse a pascal type UTF16 encoded string from a binary file object"""
    # First read the expected number of CHARACTERS
    string_length = struct.unpack(UINT8, file_.read(1))[0]
    # Then read and decode
    parsed = struct.unpack(STRING.format(2 * string_length),
                    file_.read(2 * string_length))
    return parsed[0].decode(encoding)
