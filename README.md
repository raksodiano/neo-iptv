# NeoIPTV - IPTV Player in Python

**NeoIPTV** is an IPTV application built with **Python**, **PyQt6**, and **MPV**. It allows you to stream IPTV
channels directly inside a **PyQt6** window. The app is designed to be simple and easy to use, with basic controls
such as volume adjustment and playback.

## Requirements

Before running the application, ensure you have the following installed on your **openSUSE** system:

- **Python 3.x**: The application was developed and tested with Python 3.
- **MPV**: Required to stream IPTV channels.
- **PyQt6**: For the graphical user interface (GUI).
- **pip**: For installing Python dependencies.

### Installation

It is recommended to install the application inside a **virtual environment** to keep dependencies organized and avoid
conflicts with other projects. Below are the steps for setting up the environment and the app on **openSUSE**:

### 1. Install dependencies (MPV, Python, and PyQt6)

First, ensure that Python 3, `pip`, and MPV are installed. You can install these on **openSUSE** using the following
commands:

#### Install Python 3 and MPV:

```bash
sudo zypper install python3 python3-pip
sudo zypper install mpv mpv-devel
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