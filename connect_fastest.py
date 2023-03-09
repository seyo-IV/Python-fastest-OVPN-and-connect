import os
import subprocess
import re
import speedtest

def extract_server_address_from_ovpn_file(filename):
    print(f"Extracting server address from {filename}")
    with open(filename) as f:
        content = f.read()
    server_address = re.findall('remote\s+(\S+)', content)[0]
    print(f"Server address: {server_address}")
    return server_address


def find_fastest_vpn_server(vpn_files):
    print("Finding fastest VPN server...")
    fastest_server = None
    highest_speed = 0
    for vpn_file in vpn_files:
        print(f"Testing server in {vpn_file}")
        server_address = extract_server_address_from_ovpn_file(vpn_file)
        st = speedtest.Speedtest()
        st.download_target = server_address
        speed = st.download() / 1e6  # Convert to Mbps
        print(f"Download speed: {speed:.2f} Mbps")
        if speed > highest_speed:
            highest_speed = speed
            fastest_server = vpn_file
    print(f"Fastest server: {fastest_server}")
    return fastest_server


ovpn_directory = '/opt/ovpn'
ovpn_files = [os.path.join(ovpn_directory, f) for f in os.listdir(ovpn_directory) if f.endswith('.ovpn')]

fastest_server_file = find_fastest_vpn_server(ovpn_files)
fastest_server = extract_server_address_from_ovpn_file(fastest_server_file)

# Connect to fastest server using openvpn command
print(f"Connecting to fastest server: {fastest_server}")
command = f'sudo openvpn --config {fastest_server_file}'
result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
print(result.stdout.decode())
