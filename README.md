# YetAnotherSwapManager (YAS)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python: 3.x](https://img.shields.io/badge/Python-3.x-green.svg)](https://python.org)

**YetAnotherSwapManager** is a lightweight Python script designed to simplify swap file management on Linux systems. Whether you need to quickly add more virtual memory or manage existing swap space, YAS makes it as easy as "downloading more RAM."

## ✨ Features

* **Quick Creation**: Create and enable swap files with a single command.
* **Btrfs Support**: Automatically handles `chattr +C` for Btrfs filesystems to disable Copy-on-Write (CoW).
* **UUID Detection**: Easily get the UUID of your swap file for persistent configuration in `/etc/fstab`.
* **Safety**: Sets appropriate permissions (`600`) automatically.
* **Interactive & CLI Modes**: Use the guided menu or pass arguments directly.

## 🛠 Requirements

* **Operating System**: Linux.
* **Interpreter**: Python 3.x.
* **Privileges**: Root/sudo access is required for most operations (managing files in `/` and system swap).
* **Dependencies**: `util-linux` (provides `mkswap`, `swapon`, etc. - usually pre-installed).

## Installation

Clone the repository and use the included `Makefile`:

```bash
git clone [https://github.com/YourUsername/YetAnotherSwapManager.git](https://github.com/YourUsername/YetAnotherSwapManager.git)
cd YetAnotherSwapManager
sudo make install
```

This will install the script as `swapman` to `/usr/local/bin/`.

## Usage

### CLI Mode
You can perform actions directly from the terminal:
* **Create 2GB swap**: `swapman create 2G --now`
* **List active swaps**: `swapman list`
* **Show UUID**: `swapman uuid --name swapfile`
* For more just use `swapman help`

### Interactive Mode
Simply run the script without arguments to enter the interactive menu:
```bash
swapman
```

## ⚠️ Disclaimer
*Creating swap files on some filesystems (like Btrfs) requires specific steps which this script tries to automate, but always ensure you have backups of your `/etc/fstab` before manual editing.*

## Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request.

## License
This project is licensed under the **GNU GPL 3.0**. See the `LICENSE` file for details.
