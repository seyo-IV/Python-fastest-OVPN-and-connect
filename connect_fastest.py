import os
import subprocess
import re
import speedtest

def find_fastest_vpn_server(vpn_dir):
    fastest_server = None
    highest_speed = 0
    for filename in os.listdir(vpn_dir):
        if not filename.endswith('.ovpn'):
            continue
        filepath = os.path.join(vpn_dir, filename)
        server_address = extract_server_address_from_ovpn_file(filepath)
        st = speedtest.Speedtest()
        st.download_target = server_address
        speed = st.download() / 1e6  # Convert to Mbps
        if speed > highest_speed:
            highest_speed = speed
            fastest_server = {
                'address': server_address,
                'username': 'your_username',
                'password': 'your_password'
            }
    return fastest_server


vpn_dir = '/path/to/vpn/files'
fastest_server = find_fastest_vpn_server(vpn_dir)

# Connect to fastest server using openvpn command
command = f'sudo openvpn --config {fastest_server["address"]} --auth-user-pass <(echo "{fastest_server["username"]}\n{fastest_server["password"]}")'
subprocess.run(command, shell=True, check=True)
