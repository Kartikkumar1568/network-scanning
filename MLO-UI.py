import subprocess
import tkinter as tk
from tkinter import messagebox, scrolledtext
print("Developer: Kartik") 

def list_wifi_networks():
    try:
        # Run the command to get detailed network information, including BSSID (MAC address)
        networks = subprocess.check_output(["netsh", "wlan", "show", "networks", "mode=bssid"], text=True)

        # Parse the output for specific details
        network_details = []
        current_network = {}
        bssid_list = []

        for line in networks.splitlines():
            line = line.strip()

            # Extract SSID
            if line.startswith("SSID"):
                if current_network:  # Save the previous network details
                    current_network["BSSID"] = bssid_list
                    network_details.append(current_network)
                current_network = {"SSID": line.split(":")[1].strip()}
                bssid_list = []  # Clear previous BSSID list for each new SSID

            # Extract BSSID (MAC address)
            elif line.startswith("BSSID"):
                # Capture the full BSSID (MAC address) and ensure it's fully captured
                bssid = line.split(":")[1].strip()
                if bssid and len(bssid.split(":")) == 6:  # Ensure it has 6 parts (valid MAC address)
                    bssid_list.append(bssid)  # Add the BSSID to the list

            # Extract Channel
            elif line.startswith("Channel"):
                current_network["Channel"] = line.split(":")[1].strip()

            # Extract Signal Strength
            elif line.startswith("Signal"):
                current_network["Signal"] = line.split(":")[1].strip()

            # Extract Band (2.4 GHz or 5 GHz)
            elif "GHz" in line:
                current_network["Band"] = line.split(":")[-1].strip()  # Remove the extra text

            # Extract Authentication
            elif line.startswith("Authentication"):
                current_network["Authentication"] = line.split(":")[1].strip()

            # Extract Encryption
            elif line.startswith("Encryption"):
                current_network["Encryption"] = line.split(":")[1].strip()

            # Extract Radio Type
            elif line.startswith("Radio type"):
                current_network["Radio Type"] = line.split(":")[1].strip()

            # Extract QoS Support
            elif line.startswith("QoS"):
                qos_key = line.split(":")[0].strip()
                current_network[qos_key] = line.split(":")[1].strip()

            # Extract Basic Rates (Mbps)
            elif line.startswith("Basic rates"):
                current_network["Basic Rates (Mbps)"] = line.split(":")[1].strip()

            # Extract Other Rates (Mbps)
            elif line.startswith("Other rates"):
                current_network["Other Rates (Mbps)"] = line.split(":")[1].strip()

        # Add the last network
        if current_network:
            current_network["BSSID"] = bssid_list
            network_details.append(current_network)

        return network_details

    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Command failed with error: {e}")
    except FileNotFoundError:
        messagebox.showerror("Error", "The 'netsh' command is not available. Make sure you are running this on a Windows system.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def show_wifi_networks():
    networks = list_wifi_networks()
    
    if networks:
        output_text.delete(1.0, tk.END)  # Clear previous output
        for network in networks:
            output_text.insert(tk.END, f"SSID: {network.get('SSID', 'N/A')}\n")
            bssids = network.get('BSSID', [])
            for i, bssid in enumerate(bssids, 1):
                output_text.insert(tk.END, f"BSSID {i}: {bssid}\n")  # Display full BSSID (MAC address)
            output_text.insert(tk.END, f"Channel: {network.get('Channel', 'N/A')}\n")
            output_text.insert(tk.END, f"Signal Strength: {network.get('Signal', 'N/A')}\n")
            output_text.insert(tk.END, f"Band: {network.get('Band', 'N/A')}\n")
            output_text.insert(tk.END, f"Authentication: {network.get('Authentication', 'N/A')}\n")
            output_text.insert(tk.END, f"Encryption: {network.get('Encryption', 'N/A')}\n")
            output_text.insert(tk.END, f"Radio Type: {network.get('Radio Type', 'N/A')}\n")
            output_text.insert(tk.END, f"QoS MSCS Supported: {network.get('QoS MSCS Supported', 'N/A')}\n")
            output_text.insert(tk.END, f"QoS Map Supported: {network.get('QoS Map Supported', 'N/A')}\n")
            output_text.insert(tk.END, f"Basic Rates (Mbps): {network.get('Basic Rates (Mbps)', 'N/A')}\n")
            output_text.insert(tk.END, f"Other Rates (Mbps): {network.get('Other Rates (Mbps)', 'N/A')}\n")
            output_text.insert(tk.END, "=" * 40 + "\n")
    else:
        output_text.insert(tk.END, "No networks found or an error occurred.\n")

def animate_label_color(label, colors=["red", "green", "blue"]):
    """Animation to change the label color every 500ms."""
    current_color = colors.pop(0)
    label.config(fg=current_color)
    colors.append(current_color)
    label.after(500, animate_label_color, label, colors)  # Keep animating every 500ms

# GUI setup
root = tk.Tk()
root.title("Wi-Fi Networks List")

# Change background color
root.config(bg="lightblue")

# Create a frame for the content
frame = tk.Frame(root, bg="lightblue")
frame.pack(padx=20, pady=20)

# Label with animation (color changing)
label = tk.Label(frame, text="Available Wi-Fi Networks", font=("Helvetica", 16), fg="black", bg="lightblue")
label.pack(pady=10)
animate_label_color(label)  # Start the animation

# ScrolledText widget for output with customized colors
output_text = scrolledtext.ScrolledText(frame, width=80, height=20, bg="lightgray", fg="black", font=("Courier", 12))
output_text.pack(pady=10)

# Refresh button with custom background and font color
refresh_button = tk.Button(frame, text="Refresh", command=show_wifi_networks, font=("Helvetica", 12), bg="green", fg="white")
refresh_button.pack(pady=10)

# Run the initial Wi-Fi list
show_wifi_networks()

# Run the GUI
root.mainloop()
