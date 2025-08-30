import random

def _2nd_half_mac():

    bytes = [random.randint(0x00, 0xff) for _ in range(3)]
    first_half_mac= '00:11:22'
    sec_half_mac = ':'.join(f"{b:02x}" for b in bytes)
    print(sec_half_mac)
    final_mac = f"{first_half_mac}:{sec_half_mac}"
    print(final_mac)

_2nd_half_mac()