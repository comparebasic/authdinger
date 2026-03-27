import random, time, hashlib, os


def time_bytes(t):
    return int(t*1000000).to_bytes(8)


def time_from_bytes(v):
    return time.strftime(
        '%Y-%m-%d %H:%M:%S',
        time.localtime(float(int.from_bytes(v, "big"))/1000000.0))


def get_token(content):
    h = hashlib.sha256()

    if not isinstance(content, (bytes)):
        content = content.encode("utf-8")

    h.update(content)
    h.update(time_bytes(time.time()))
    h.update(random.randbytes(4))
    return h.hexdigest() 


def get_six(tk):
    if not isinstance(tk, (bytes)):
        tk = tk.encode("utf-8")

    offset = tk[0] % 7
    return int.from_bytes(tk[offset:offset+8], "big") % 999999


def check_six(six, tk):
    if not isinstance(tk, (bytes)):
        tk = tk.encode("utf-8")

    if not isinstance(six, (int)):
        six = int(six)

    offset = tk[0] % 7
    return six == int.from_bytes(tk[offset:offset+8], "big") % 999999


def get_short_token(content):
    return get_token(content)[32:]


def rfc822(dt):
    ctime = dt.ctime()
    return "{}, {} {} {} {}".format(
        ctime[:3], ctime[8:10], ctime[4:7], ctime[20:24], dt.strftime("%H:%M:%S %z (%Z)"))
