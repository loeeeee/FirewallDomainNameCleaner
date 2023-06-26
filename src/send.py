import socket
import sys
import dns.message

def send_dns_query(target_ip, target_port):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set a timeout for the socket
    sock.settimeout(5)

    # DNS query packet (example: requesting A record for "example.com")
    dns_query = b'\x00\x01\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07example\x03com\x00\x00\x01\x00\x01'

    try:
        # Send the DNS query to the target IP address and port
        sock.sendto(dns_query, (target_ip, target_port))

        # Receive the response from the server
        response, server_address = sock.recvfrom(4096)

        # Parse the DNS response using the dns.message.from_wire() function
        dns_response = dns.message.from_wire(response)

        # Extract relevant information from the response
        for answer in dns_response.answer:
            print("Response:", answer.to_text())

    except socket.timeout:
        print("DNS query timed out.")

    finally:
        # Close the socket
        sock.close()

DNSserverIP = sys.argv[1]
port = int(sys.argv[2])
# Example usage: send DNS query to IP address "8.8.8.8" on port 53
send_dns_query(DNSserverIP, port)
