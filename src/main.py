from gfwatch import GFWatch
from dnslib import DNSRecord
from typing import Union
import socket

class UpstreamDNS:
    def __init__(self,
                 ip_adress: int,
                 port: int,
                 ) -> None:
        self.ip_address = ip_adress
        self.port = port

    def _forward(self, request):
        """
        Forward the request and listen for respond
        """
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5)  # Set a timeout for the socket operations

        try:
            # Send the DNS request to the upstream DNS server
            sock.sendto(request.pack(), (self.ip_address, self.port))

            # Receive the response from the upstream DNS server
            data, _ = sock.recvfrom(1024)

            # Create a DNSRecord object from the response data
            response = DNSRecord.parse(data)

            return response
        except socket.timeout:
            print("Timeout occurred while forwarding DNS request")
            return None
        finally:
            sock.close()
            return


class DNSCleaner:
    def __init__(self,
                 foreign_upstream: Union[list, UpstreamDNS],
                 domestic_upstream: Union[list, UpstreamDNS],
                 GFWatch_dir: str,
                 ) -> None:
        """
        Select which server to forward to
        """
        self.foreign_upstream = foreign_upstream
        self.domestic_upstream = domestic_upstream
        self.classifier = GFWatch(GFWatch_dir)

    def run(self) -> None:
        """
        The main loop for the DNS cleaner
        """
        while True:
            # Create a UDP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((listen_ip, listen_port))

            print(f"Listening for DNS requests on {listen_ip}:{listen_port}...")
            
            while True:
                try:
                    # Receive DNS request data and address from the client
                    data, addr = sock.recvfrom(1024)
                    
                    # Create a DNSRecord object from the received data
                    request = DNSRecord.parse(data)

                    # Forward the DNS request to the upstream DNS server
                    response = forward_dns_request(request, upstream_dns_server)

                    if response:
                        # Send the DNS response back to the client
                        sock.sendto(response.pack(), addr)
                    else:
                        print("Failed to receive DNS response")
                except KeyboardInterrupt:
                    print("DNS server stopped")
                    break

            sock.close()




def forward_dns_request(request, upstream_dns_server):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)  # Set a timeout for the socket operations

    try:
        # Send the DNS request to the upstream DNS server
        sock.sendto(request.pack(), upstream_dns_server)

        # Receive the response from the upstream DNS server
        data, _ = sock.recvfrom(1024)

        # Create a DNSRecord object from the response data
        response = DNSRecord.parse(data)

        return response
    except socket.timeout:
        print("Timeout occurred while forwarding DNS request")
        return None
    finally:
        sock.close()

def listen_dns_requests(listen_ip, listen_port, upstream_dns_server):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((listen_ip, listen_port))

    print(f"Listening for DNS requests on {listen_ip}:{listen_port}...")
    
    while True:
        try:
            # Receive DNS request data and address from the client
            data, addr = sock.recvfrom(1024)
            
            # Create a DNSRecord object from the received data
            request = DNSRecord.parse(data)

            # Forward the DNS request to the upstream DNS server
            response = forward_dns_request(request, upstream_dns_server)

            if response:
                # Send the DNS response back to the client
                sock.sendto(response.pack(), addr)
            else:
                print("Failed to receive DNS response")
        except KeyboardInterrupt:
            print("DNS server stopped")
            break

    sock.close()

# Example usage
if __name__ == "__main__":
    # Set the listening IP and port
    listen_ip = '127.0.0.1'  # Replace with the desired listening IP
    listen_port = 8000  # Replace with the desired listening port

    # Set the upstream DNS server details
    upstream_dns_server = ('192.168.163.40', 53)  # Google DNS server

    # Start listening for DNS requests and forwarding them
    listen_dns_requests(listen_ip, listen_port, upstream_dns_server)

