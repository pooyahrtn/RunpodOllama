import socket


def is_port_free(port: int) -> bool:
    """
    Check if a port is free
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) != 0
