# NeoIPTV - IPTV Player in Python

**NeoIPTV** is an IPTV application built with **Python**, **PyQt6**, and **MPV**. It allows you to stream IPTV
channels directly inside a **PyQt6** window. The app is designed to be simple and easy to use, with basic controls
such as volume adjustment and playback.

## Requirements

Before running the application, ensure you have the following installed on your **openSUSE** system:

- **Python 3.x**: The application was developed and tested with Python 3.
- **MPV**: Required to stream IPTV channels.
- **MPV development libraries**: Necessary for building and linking MPV.
- **pip**: For installing Python dependencies.
- **PyQt6**: For the graphical user interface (GUI).
- **ipytv**: A Python library for handling IPTV playlists.

### Installation

It is recommended to install the application inside a **virtual environment** to keep dependencies organized and avoid
conflicts with other projects. Below are the steps for setting up the environment and the app on **openSUSE**,
**Debian**, and **Fedora**:

### 1. Install dependencies (Python and MPV)

First, ensure that `Python 3`, `pip`, and `MPV` are installed. You can install these using the following commands:

#### On openSUSE:

```bash
sudo zypper install python3 python3-pip
sudo zypper install mpv mpv-devel
```

#### On Debian:

```bash
sudo apt update
sudo apt install python3 python3-pip
sudo apt install mpv libmpv-dev
```

#### On Fedora:

```bash
sudo dnf install python3 python3-pip
sudo dnf install mpv mpv-libs
```

### 2. Create and activate a virtual environment

After installing the required system dependencies, create a virtual environment for the project:

```bash
python3 -m venv venv
source venv/bin/activate
```

This will create and activate a virtual environment in the venv directory.

### 3. Install the Python dependencies

Once the virtual environment is activated, install the required Python dependencies using pip. Run the following
command:

```bash
pip install -r requirements.txt
```

### 4. Run the application

Once the dependencies are installed, you can run the application. Make sure the virtual environment is activated and
then run the following command:

```bash 
python -m iptv
```

### License

This project is licensed under the MIT License. Please see the LICENSE file for more details.