import numpy as np
import re

def read(file):
    f = open(file, "rb")
    magic = f.read(30)

    # Other versions are not supported
    assert magic == b"CST Data File Version 20101216"

    # Seek to header size
    f.seek(0x32)

    # Decode header size
    number = ""
    while (a := f.read(1)) != b";":
        number += a.decode("ascii")
    try:
        header_bytes = int(number)
    except ValueError:
        print("Error parsing header size. Please inform maintainer.")

    # Seek back to beginning and decode whole header
    f.seek(0)
    header_str = f.read(header_bytes).decode("ascii")

    # Pattern matching to parse header into dict
    header = {}
    header["CST Data File Version"] = header_str[22:30]
    for line in header_str.split("\n"):
        # Match header key
        key = re.findall(r"(\S+) =", line)
        if len(key) == 0:
            continue
        # Match header values
        header[key[0]] = re.findall(r" (\S+);", line)

    # All known types are floats of varying precision
    types = {32: np.float32, 64: float}
    data = {}

    # Use header information to decode binary file contents
    for field, size, dtype in zip(
        header["QuantityNames"], header["DataFieldBytes"], header["QuantityTypes"]
    ):
        # Parse header type string (e.g. SerialVector3x64 => (3, 64))
        dim, bits = map(int, re.findall(r"SerialVector(\d)x(\d+)", dtype)[0])
        # Calculate number of values for np.fromfile
        count = int(size) // (bits // 8)
        # Decode binary data and reshape properly
        data[field] = np.fromfile(f, dtype=types[bits], count=count).reshape(-1, dim).T
    f.close()
    return header, data
