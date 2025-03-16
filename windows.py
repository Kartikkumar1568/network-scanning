import subprocess
import  pyfiglet

text = pyfiglet.figlet_format("parrot")
print(text)

def list_wifi_networks():
    try:
        # Run the command to get detailed network information, including BSSID (MAC address)
        networks = subprocess.check_output(["netsh", "wlan", "show", "networks", "mode=bssid"], text=True)

        # Print raw output for debugging
        print("Raw output from 'netsh wlan show networks mode=bssid':")
        print(networks)
        
        # Parse the output for specific details
        network_details = []
        current_network = {}

        for line in networks.splitlines():
            line = line.strip()

            # Extract SSID
            if line.startswith("SSID"):
                if current_network:  # Save the previous network details
                    network_details.append(current_network)
                current_network = {"SSID": line.split(":")[1].strip()}

            # Extract BSSID (MAC address)
            elif line.startswith("BSSID"):
                bssid = line.split(":")[1].strip()  # Extract the MAC address part
                current_network["BSSID"] = bssid

            # Extract Channel
            elif line.startswith("Channel"):
                current_network["Channel"] = line.split(":")[1].strip()

            # Extract Signal Strength
            elif line.startswith("Signal"):
                current_network["Signal"] = line.split(":")[1].strip()

            # Extract Band (2.4 GHz or 5 GHz)
            elif "GHz" in line:
                current_network["Band"] = line.split(":")[-1].strip()  # Remove the extra text

        # Add the last network
        if current_network:
            network_details.append(current_network)

        # Print parsed network details
        for network in network_details:
            print("=========================================")
            print(f"SSID: {network.get('SSID', 'N/A')}")
            print(f"BSSID: {network.get('BSSID', 'N/A')}")
            print(f"Channel: {network.get('Channel', 'N/A')}")
            print(f"Signal Strength: {network.get('Signal', 'N/A')}")
            print(f"Band: {network.get('Band', 'N/A')}")

    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e}")
    except FileNotFoundError:
        print("The 'netsh' command is not available. Make sure you are running this on a Windows system.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    list_wifi_networks()
