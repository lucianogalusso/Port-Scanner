import socket
from urllib.parse import urlparse
import common_ports
import re

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)

def is_ip(input):
    match = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", input)
    if match:
        return True
    else:
        return False
    
def get_host_from_ip(ip):
    try:
        addr_info = socket.getaddrinfo(ip, None)
        for info in addr_info:
            if info[0] == socket.AF_INET:
                return info[3]
    except socket.gaierror:
        return None


#get_open_ports("209.216.230.240", [440, 445])
#get_open_ports("www.stackoverflow.com", [79, 82])
def get_open_ports(target, port_range, verbose = False):
    open_ports = []
    start = port_range[0]
    end = port_range[1]
    if (is_ip(target)):
        ip = target
        host = get_host_from_ip(ip)
        if host == None:
            return "Error: Invalid IP address"
    else:
        host = target
        try:
            ip = socket.gethostbyname(target)
        except (socket.gaierror, AttributeError):
            return "Error: Invalid hostname"           
    
    if verbose:
        # Open ports for {URL} ({IP address})
        # PORT     SERVICE
        if host != '':
            open_ports = f"""
            Open ports for {host} ({ip})\nPORT     SERVICE\n"""
        else:
            open_ports = f"""
            Open ports for {ip}\nPORT     SERVICE\n"""

        open_ports = open_ports.strip()
        
    for i in range(start, end + 1):
        connect = s.connect_ex((ip, i))
        if connect == socket.errno.ECONNREFUSED:
            print("Conexión rechazada")
        elif connect == socket.errno.ETIMEDOUT:
            print("Tiempo de espera agotado")
        elif connect != 0:
            continue
        if verbose:
            # {port}   {service name}
            if i in common_ports.ports_and_services:
                serviceName = common_ports.ports_and_services.get(i)
            else:
                serviceName = "" 
            open_ports += f"\n{i}    {serviceName}"
        else:
            open_ports.append(i)

    return(open_ports)