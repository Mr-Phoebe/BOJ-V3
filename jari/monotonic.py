import time
import platform
import ctypes
import ctypes.util

if platform.system() == 'FreeBSD':
    CLOCK_MONOTONIC = 4
else:
    CLOCK_MONOTONIC = 1

class timespec(ctypes.Structure):
    _fields_ = [
            ('tv_sec', ctypes.c_long),
            ('tv_nsec', ctypes.c_long)
            ]

librt_filename = ctypes.util.find_library('rt')
librt = ctypes.CDLL(librt_filename)
_clock_gettime = librt.clock_gettime
_clock_gettime.argtypes = (ctypes.c_int, ctypes.POINTER(timespec))

def monotonic_time():
    """
    Clock that cannot be set and represents monotonic time since some
    unspecified starting point. The unit is a second.
    """
    t = timespec()
    if _clock_gettime(CLOCK_MONOTONIC, ctypes.pointer(t)) != 0:
        errno_ = ctypes.get_errno()
        raise OSError(errno_, os.strerror(errno_))
    return t.tv_sec + t.tv_nsec * 1e-9

#if __name__ == '__main__':
    #print monotonic_time()
    #time.sleep(3)
    #print monotonic_time()

