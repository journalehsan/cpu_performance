# CPU Priority Manager & Ananicy Configurator

This Python script provides a command-line utility to adjust the CPU priority of running processes or generate configuration files for Ananicy based on a CSV input. It allows you to:

1. Adjust CPU priorities of running processes.
2. Generate Ananicy config files to manage CPU priority automatically.
3. Kill all zombie processes in the system.

## Features
- Adjust CPU priority for any process using `renice`.
- Generate Ananicy config files for processes and restart the Ananicy service.
- Kill zombie processes in your system with ease.
- Interactive menu with command-line switches for fast execution.
- Progress bars to track the status of tasks.

## Table of Contents
1. [Installation](#installation)
2. [CSV File Format](#csv-file-format)
3. [Usage](#usage)
   - [Interactive Menu](#interactive-menu)
   - [Command-Line Arguments](#command-line-arguments)
4. [Zombie Process Management](#zombie-process-management)
5. [Example](#example)
6. [Contributing](#contributing)
7. [License](#license)

---

## Installation

### Prerequisites
Ensure that you have the following installed:
- Python 3.7+
- `pip` (Python package installer)
- `renice` (available on most Unix-based systems)
- `Ananicy` (for Ananicy configurations)

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/cpu-priority-manager.git
cd cpu-priority-manager
```

### 2. Install Required Python Libraries
Run the following command to install necessary Python libraries:
```bash
pip install -r requirements.txt
```

The `requirements.txt` includes:
- `tqdm` for progress bars
- `prettytable` for displaying the menu in a neat table format

You can also install them manually:
```bash
pip install tqdm prettytable
```

---

## CSV File Format

The CSV file defines the processes and their corresponding CPU priority. The file should have two columns:
- **First Column**: The name of the process (as shown in `ps` or `top`).
- **Second Column**: The priority label (`low`, `medium`, `high`, `important`).

Example (`process_priority.csv`):
```csv
firefox,high
python3,medium
nginx,important
chrome,low
```

The priority levels are mapped as:
- `low` → `10`
- `medium` → `0`
- `high` → `-10`
- `important` → `-20`

---

## Usage

You can run the script in two ways:
1. **Interactive Menu**: Run the script without any arguments to access the interactive menu.
2. **Command-Line Arguments**: Use command-line switches to directly execute tasks.

### Interactive Menu

Simply run the script with no arguments to access the interactive menu:
```bash
python main.py
```

You will be presented with a table menu with the following options:
- **1**: Adjust CPU priorities based on the CSV file.
- **2**: Generate Ananicy config files and restart the Ananicy service.
- **3**: Kill all zombie processes.
- **exit**: Exit the program.

### Command-Line Arguments

Alternatively, you can use command-line arguments for faster execution:

#### 1. Adjust CPU Priorities
To immediately adjust CPU priorities of running processes:
```bash
python main.py --apply-now
```

#### 2. Generate Ananicy Config and Restart Ananicy
To generate Ananicy config files and restart the Ananicy service:
```bash
python main.py --ananicy
```

If no valid command-line option is passed, the script will show an error message and suggest valid options.

---

## Zombie Process Management

A zombie process is a process that has completed execution but still has an entry in the process table. This script allows you to kill all zombie processes easily.

In the interactive menu, select option **3** to kill zombie processes, or add this functionality to your script by calling the function directly.

---

## Example

Here’s an example of the workflow:

1. Prepare your CSV file (`process_priority.csv`) as described above.
2. Run the script interactively:
    ```bash
    python main.py
    ```

3. In the menu, select:
   - **Option 1** to adjust CPU priorities immediately.
   - **Option 2** to generate Ananicy configuration and restart the Ananicy service.

You can also use command-line options directly, like:
```bash
python main.py --apply-now
```

---

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.

Please ensure your code follows Python best practices and is well-documented.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Additional Notes

### Logging
- Add logging to keep track of priority adjustments or errors during execution.

### Customization
- You can specify a different CSV file or Ananicy config directory by modifying the paths in the script or passing them as additional command-line arguments.
