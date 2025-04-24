import psutil
import tkinter as tk
from tkinter import messagebox, scrolledtext


class ResourceManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Resource Manager")
        self.root.geometry("600x500")

        # Label
        self.label = tk.Label(self.root, text="System Resource Manager", font=("Arial", 16))
        self.label.pack(pady=10)

        # CPU Usage Label
        self.cpu_label = tk.Label(self.root, text="CPU Usage: --%", font=("Arial", 12))
        self.cpu_label.pack(pady=5)

        # Memory Usage Label
        self.memory_label = tk.Label(self.root, text="Memory Usage: --%", font=("Arial", 12))
        self.memory_label.pack(pady=5)

        # Disk Usage Label
        self.disk_label = tk.Label(self.root, text="Disk Usage: --%", font=("Arial", 12))
        self.disk_label.pack(pady=5)

        # Network Activity Label
        self.network_label = tk.Label(self.root, text="Network Activity: --", font=("Arial", 12))
        self.network_label.pack(pady=5)

        # Process Usage Label
        self.process_label = tk.Label(self.root, text="Top Resource-Using Processes:", font=("Arial", 12))
        self.process_label.pack(pady=5)

        # Textbox to display top processes
        self.process_text = scrolledtext.ScrolledText(self.root, width=60, height=10)
        self.process_text.pack(pady=5)

        # Refresh Button (manual refresh)
        self.refresh_button = tk.Button(self.root, text="Refresh", command=self.refresh_resources)
        self.refresh_button.pack(pady=10)

        # Start live updates
        self.update_resources()

    def update_resources(self):
        """Live update the system resource statistics every 2 seconds."""
        try:
            # Get CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)

            # Get Memory usage
            memory = psutil.virtual_memory()
            memory_usage = memory.percent

            # Get Disk usage
            disk = psutil.disk_usage('/')
            disk_usage = disk.percent

            # Get Network activity (bytes sent/received)
            net = psutil.net_io_counters()
            network_activity = f"Sent: {self.convert_bytes(net.bytes_sent)} | Received: {self.convert_bytes(net.bytes_recv)}"

            # Update the labels with current values
            self.cpu_label.config(text=f"CPU Usage: {cpu_usage}%")
            self.memory_label.config(text=f"Memory Usage: {memory_usage}%")
            self.disk_label.config(text=f"Disk Usage: {disk_usage}%")
            self.network_label.config(text=f"Network Activity: {network_activity}")

            # Update process usage
            self.update_process_usage()

            # Schedule next update in 2000 ms (2 seconds)
            self.root.after(2000, self.update_resources)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while fetching system stats: {e}")

    def update_process_usage(self):
        """Fetch and display top CPU and memory-consuming processes."""
        try:
            processes = []
            for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_percent']):
                processes.append(proc.info)

            # Sort processes by CPU and memory usage
            processes = sorted(processes, key=lambda p: (p['cpu_percent'], p['memory_percent']), reverse=True)[:5]

            # Display process information
            self.process_text.delete(1.0, tk.END)
            for proc in processes:
                self.process_text.insert(tk.END,
                                         f"{proc['name']} (PID {proc['pid']}): CPU {proc['cpu_percent']}% | Mem {proc['memory_percent']:.2f}%\n")
        except Exception as e:
            self.process_text.insert(tk.END, f"Error fetching process data: {e}\n")

    def refresh_resources(self):
        """Manual refresh of the resource stats."""
        self.update_resources()

    def convert_bytes(self, bytes_value):
        """Convert bytes to a more readable format (KB, MB, GB)."""
        if bytes_value < 1024:
            return f"{bytes_value} B"
        elif bytes_value < 1048576:
            return f"{bytes_value / 1024:.2f} KB"
        elif bytes_value < 1073741824:
            return f"{bytes_value / 1048576:.2f} MB"
        else:
            return f"{bytes_value / 1073741824:.2f} GB"


def main():
    root = tk.Tk()
    app = ResourceManagerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
