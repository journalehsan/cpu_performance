import csv
import os
import subprocess
import sys
from prettytable import PrettyTable
from tqdm import tqdm

# Class for adjusting CPU priority based on CSV file
class AdjustCPU:
    PRIORITY_MAP = {
        'low': 10,
        'medium': 0,
        'high': -10,
        'important': -20
    }

    def __init__(self, csv_file):
        self.csv_file = csv_file

    def apply_priority(self):
        """Reads CSV and applies CPU priorities."""
        print("\nApplying CPU priorities:")
        with open(self.csv_file, newline='') as file:
            reader = csv.reader(file)
            for row in tqdm(reader, desc="Adjusting priorities"):
                if len(row) < 2:
                    continue
                process_name, priority_label = row[0], row[1].lower()
                if priority_label in self.PRIORITY_MAP:
                    priority_value = self.PRIORITY_MAP[priority_label]
                    # Use 'renice' to adjust CPU priority
                    self.set_process_priority(process_name, priority_value)

    def set_process_priority(self, process_name, priority):
        """Set process priority using 'renice'."""
        try:
            pid = subprocess.check_output(["pidof", process_name]).decode().strip()
            print(f"\nSetting priority {priority} for {process_name} (PID: {pid})")
            subprocess.run(["renice", str(priority), "-p", pid], check=True)
        except subprocess.CalledProcessError:
            print(f"Process {process_name} not found. Skipping...")

# Class for creating Ananicy configs and restarting Ananicy service
class ConfigAndRestartAnanicy:
    def __init__(self, csv_file, ananicy_config_path="/etc/ananicy.d"):
        self.csv_file = csv_file
        self.ananicy_config_path = ananicy_config_path

    def create_configs(self):
        """Creates Ananicy config files for each process."""
        print("\nCreating Ananicy configs:")
        with open(self.csv_file, newline='') as file:
            reader = csv.reader(file)
            for row in tqdm(reader, desc="Writing config files"):
                if len(row) < 2:
                    continue
                process_name, priority_label = row[0], row[1].lower()
                config_file = os.path.join(self.ananicy_config_path, f"{process_name}.cfg")
                self.write_config(process_name, priority_label, config_file)

        print("\nRestarting Ananicy service...")
        subprocess.run(["systemctl", "restart", "ananicy"], check=True)

    def write_config(self, process_name, priority_label, config_file):
        """Writes individual Ananicy config file."""
        priority_value = AdjustCPU.PRIORITY_MAP.get(priority_label, 0)
        config_content = f"[{process_name}]\nNice={priority_value}\n"
        with open(config_file, "w") as file:
            file.write(config_content)
        print(f"Config for {process_name} written to {config_file}")

# Function to kill all zombie processes
def kill_zombie_processes():
    """Kill all zombie processes in the system."""
    print("\nKilling all zombie processes...")
    zombie_processes = subprocess.check_output(
        "ps aux | awk '{ if ($8 == \"Z\") print $2 }'", shell=True).decode().strip()
    if zombie_processes:
        for pid in zombie_processes.split("\n"):
            print(f"Killing zombie process with PID: {pid}")
            subprocess.run(["kill", "-9", pid])
    else:
        print("No zombie processes found.")

# Main application
def main_menu():
    table = PrettyTable()
    table.field_names = ["Option", "Description"]
    table.add_row(["1", "Adjust CPU priority now"])
    table.add_row(["2", "Generate Ananicy config and restart Ananicy"])
    table.add_row(["3", "Kill all zombie processes"])
    table.add_row(["exit", "Exit the program"])

    while True:
        print(table)
        choice = input("Select an option: ")
        if choice == "1":
            adjust_cpu()
        elif choice == "2":
            config_and_restart_ananicy()
        elif choice == "3":
            kill_zombie_processes()
        elif choice == "exit":
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice. Please select again.")

def adjust_cpu():
    csv_file = "process_priority.csv"  # Assuming the file is in the current directory
    adjuster = AdjustCPU(csv_file)
    adjuster.apply_priority()

def config_and_restart_ananicy():
    csv_file = "process_priority.csv"
    configurer = ConfigAndRestartAnanicy(csv_file)
    configurer.create_configs()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if "--apply-now" in sys.argv:
            adjust_cpu()
        elif "--ananicy" in sys.argv:
            config_and_restart_ananicy()
        else:
            print("Invalid option. Use --apply-now or --ananicy.")
    else:
        main_menu()
