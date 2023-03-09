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
            fastest_server = vpn_file
    return fastest_server


ovpn_directory = '/opt/ovpn'
ovpn_files = [os.path.join(ovpn_directory, f) for f in os.listdir(ovpn_directory) if f.endswith('.ovpn')]

fastest_server_file = find_fastest_vpn_server(ovpn_files)
if fastest_server_file is None:
    print("Could not find any VPN files in the directory.")
    exit(1)
fastest_server = extract_server_address_from_ovpn_file(fastest_server_file)

# Connect to fastest server using openvpn command and log output to file
log_file = '/var/log/ovpn.log'
command = f'sudo openvpn --config {fastest_server_file} >> {log_file} 2>&1'
try:
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(result.stdout.decode())
except subprocess.CalledProcessError as e:
    print(f"Error occurred: {e}")
    print(e.stderr.decode())
