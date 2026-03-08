from .. import BSTREAM_MAX

def from_array(arr):
    s = b""
    for seg in arr:
        if isinstance(seg, str):
            seg = bytes(seg, "utf-8")
        s += len(seg).to_bytes(2, "big")
        s += seg
    return s

def read_next(stream):
    if hasattr(stream, 'recv'):
        length_s = stream.recv(2)
    else:
        length_s = stream.read(2)

    length = int.from_bytes(length_s, "big")
    if length > BSTREAM_MAX:
        raise ValueError("Length exeeds max", length)

    if length == 0:
        return None

    if hasattr(stream, 'recv'):
        b = stream.recv(length)
    else:
        b = stream.read(length)
    if len(b) != length:
        raise TypeError(
            "Byte length {} does not match expected length {}".format(
                len(b), length 
            )
        )

    return b.decode("utf-8")

def arr_to_dict(arr):
    data = {}
    for i in range(0, len(arr), 2):
        data[arr[i]] = arr[i+1]

    if len(arr) % 2:
        data[arr[-1]] = True

    return data
