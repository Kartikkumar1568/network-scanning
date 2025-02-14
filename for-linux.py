import subprocess
import pyfiglet
import re

def list_wifi_networks():
    try:
        # Display ASCII Art Title
        print(pyfiglet.figlet_format("Parrot"))

        # Run the Linux command to scan for Wi-Fi networks
        networks = subprocess.check_output(["nmcli", "-t", "-f", "SSID,BSSID,CHAN,SIGNAL,FREQ", "dev", "wifi"], text=True, encoding='utf-8', errors='ignore')

        network_details = []
        seen_ssids = {}

        # Process each line of output
        for line in networks.splitlines():
            parts = line.split(":")
            if len(parts) < 5:
                continue  # Skip malformed lines

            ssid, bssid, channel, signal, frequency = parts

            if ssid not in seen_ssids:
                seen_ssids[ssid] = {
                    "SSID": ssid,
                    "BSSIDs": [],
                    "Channel": channel,
                    "Signal": signal + "%",
                    "Band": "5 GHz" if "5" in frequency else "2.4 GHz"
                }
            
            seen_ssids[ssid]["BSSIDs"].append(bssid)

        # Convert dictionary to list for display
        network_details = list(seen_ssids.values())

        # Print formatted network details
        for network in network_details:
            print("\n=========================================")
            print(f"SSID: {network.get('SSID', 'N/A')}")
            print(f"BSSIDs: {', '.join(network.get('BSSIDs', []))}")
            print(f"Channel: {network.get('Channel', 'N/A')}")
            print(f"Signal Strength: {network.get('Signal', 'N/A')}")
            print(f"Band: {network.get('Band', 'N/A')}")
        print("=========================================")

    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e}")
    except FileNotFoundError:
        print("The 'nmcli' command is not available. Install NetworkManager or use 'iwlist' instead.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    list_wifi_networks()
