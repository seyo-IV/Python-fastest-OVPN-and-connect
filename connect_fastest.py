import os
import subprocess
import re
import speedtest

def extract_server_address_from_ovpn_file(filename):
    with open(filename) as f:
        content = f.read()
    server_address = re.findall('remote\s+(\S+)', content)[0]
    return server_address


def find_fastest_vpn_server(vpn_files):
    fastest_server = None
    highest_speed = 0
    for vpn_file in vpn_files:
        server_address = extract_server_address_from_ovpn_file(vpn_file)
        st = speedtest.Speedtest()
        st.download_target = server_address
        speed = st.download() / 1e6  # Convert to Mbps
        if speed > highest_speed:
            highest_speed = speed
            fastest_server = server_address
    return fastest_server





ovpn_directory = '/path/to/ovpn/files'
ovpn_files = [os.path.join(ovpn_directory, f) for f in os.listdir(ovpn_directory) if f.endswith('.ovpn')]

fastest_server = find_fastest_vpn_server(ovpn_files)

# Connect to fastest server using openvpn command
command = f'sudo openvpn --config {fastest_server}'
subprocess.run(command, shell=True, check=True)
