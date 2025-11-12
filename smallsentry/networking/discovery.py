# smallsentry/network/discovery.py

def octet_first() -> int:
    return 10


def octet_second(c_num: int) -> int:
    """Return 111 for the first half of containers, 222 for the rest."""
    return 111 if c_num < 22 else 222


def octet_third(c_num: int, dhcp: bool) -> int:
    """Compute the third octet based on container index and DHCP flag."""
    sub = 2 if dhcp else 1
    return c_num * 2 - sub


def generate_ip_list(dhcp: bool = True):
    """Yield (container_number, ip) tuples for all miner containers."""
    first = octet_first()
    for c_num in range(1, 40):  # C01–C39
        second = octet_second(c_num)
        third = octet_third(c_num, dhcp)
        for fourth in range(1, 256):
            yield c_num, f"{first}.{second}.{third}.{fourth}"


def generate_debug_list():
    """
    Yield (container_number, dev_target) tuples for local testing.
    Maps everything to 192.168.50.243:[23901-24155].
    """
    host = "192.168.50.243"
    for fourth in range(1, 256):
        yield 1, f"{host}:{23900 + fourth}"


def ip_pairs(debug: bool = False, dhcp: bool = True) -> list[tuple[int, str]]:
    """Return full (container_number, address) pairs."""
    gen = generate_debug_list if debug else generate_ip_list
    return list(gen(dhcp)) if not debug else list(gen())
