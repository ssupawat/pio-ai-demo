#!/usr/bin/env python3
"""Detect connected microcontroller boards via USB.

Usage:
    python3 detect.py [--json]

Outputs board info. Use --json for machine-readable output.
"""

import subprocess, json, glob, sys

# Known board database: (vid, pid) -> info
BOARDS = {
    (0x2341, 0x0043): {
        "board_name": "Arduino Uno R3 (genuine)",
        "platformio_id": "uno",
        "usb_chip": "ATmega16U2",
        "framework": "arduino",
        "upload_method": "standard",
        "upload_note": "Use pio run -t upload"
    },
    (0x2341, 0x0001): {
        "board_name": "Arduino Uno R3 (genuine)",
        "platformio_id": "uno",
        "usb_chip": "ATmega16U2",
        "framework": "arduino",
        "upload_method": "standard",
        "upload_note": "Use pio run -t upload"
    },
    (0x1A86, 0x7523): {
        "board_name": "Arduino Uno R3 (CH340 clone)",
        "platformio_id": "uno",
        "usb_chip": "CH340G",
        "framework": "arduino",
        "upload_method": "ch340",
        "upload_note": "CH340 clone — use upload-ch340.py instead of pio run -t upload"
    },
    (0x1A86, 0x1A86): {
        "board_name": "Arduino Nano (CH340 clone)",
        "platformio_id": "nanoatmega328",
        "usb_chip": "CH340G",
        "framework": "arduino",
        "upload_method": "ch340",
        "upload_note": "CH340 clone — use upload-ch340.py instead of pio run -t upload"
    },
    (0x2341, 0x0010): {
        "board_name": "Arduino Mega 2560 (genuine)",
        "platformio_id": "megaatmega2560",
        "usb_chip": "ATmega16U2",
        "framework": "arduino",
        "upload_method": "standard",
        "upload_note": "Use pio run -t upload"
    },
    (0x2341, 0x0042): {
        "board_name": "Arduino Mega 2560 R3 (genuine)",
        "platformio_id": "megaatmega2560",
        "usb_chip": "ATmega16U2",
        "framework": "arduino",
        "upload_method": "standard",
        "upload_note": "Use pio run -t upload"
    },
    (0x0403, 0x6001): {
        "board_name": "Arduino clone (FTDI)",
        "platformio_id": "uno",
        "usb_chip": "FT232RL",
        "framework": "arduino",
        "upload_method": "standard",
        "upload_note": "Use pio run -t upload"
    },
    (0x10C4, 0xEA60): {
        "board_name": "Board with CP2102",
        "platformio_id": "unknown",
        "usb_chip": "CP2102",
        "framework": "arduino",
        "upload_method": "ch340",
        "upload_note": "CP2102 — use upload-ch340.py. Board ID may need manual override."
    },
    (0x2341, 0x8015): {
        "board_name": "Arduino Leonardo",
        "platformio_id": "leonardo",
        "usb_chip": "ATmega32U4",
        "framework": "arduino",
        "upload_method": "standard",
        "upload_note": "Use pio run -t upload"
    },
    (0x2341, 0x8036): {
        "board_name": "Arduino Leonardo",
        "platformio_id": "leonardo",
        "usb_chip": "ATmega32U4",
        "framework": "arduino",
        "upload_method": "standard",
        "upload_note": "Use pio run -t upload"
    },
    (0x239A, 0x8012): {
        "board_name": "Adafruit Feather M4 Express",
        "platformio_id": "adafruit_feather_m4",
        "usb_chip": "ATSAMD51",
        "framework": "arduino",
        "upload_method": "standard",
        "upload_note": "Use pio run -t upload"
    },
    (0x303A, 0x1001): {
        "board_name": "ESP32-S3 (native USB)",
        "platformio_id": "esp32-s3-devkitc-1",
        "usb_chip": "ESP32-S3 built-in",
        "framework": "arduino",
        "upload_method": "standard",
        "upload_note": "Use pio run -t upload"
    },
}

def get_usb_devices():
    """Get USB device info from ioreg (macOS)."""
    result = subprocess.run(
        ['ioreg', '-p', 'IOUSB', '-w0', '-r', '-c', 'IOUSBHostDevice'],
        capture_output=True, text=True, timeout=10
    )
    return result.stdout

def parse_usb_devices(ioreg_output):
    """Parse ioreg output into list of devices with vid/pid."""
    devices = []
    current = {}
    
    for line in ioreg_output.split('\n'):
        line = line.strip()
        if '"idVendor"' in line:
            try:
                current['vid'] = int(line.split('=')[1].strip().rstrip(','))
            except (ValueError, IndexError):
                pass
        elif '"idProduct"' in line:
            try:
                current['pid'] = int(line.split('=')[1].strip().rstrip(','))
            except (ValueError, IndexError):
                pass
        elif '"USB Product Name"' in line:
            try:
                name = line.split('=')[1].strip().strip('"').rstrip(',')
                current['name'] = name
            except (IndexError):
                pass
        elif 'IOUSBHostDevice' in line and '-o' in line:
            if current.get('vid') and current.get('pid'):
                devices.append(current.copy())
            current = {}
    
    # Don't forget last device
    if current.get('vid') and current.get('pid'):
        devices.append(current.copy())
    
    return devices

def find_serial_port():
    """Find available serial ports."""
    ports = []
    for pattern in ['/dev/cu.usbserial*', '/dev/cu.usbmodem*', '/dev/cu.wch*']:
        ports.extend(glob.glob(pattern))
    return ports

def detect():
    """Detect connected boards."""
    ports = find_serial_port()
    
    if not ports:
        return {
            "error": "No serial ports found. Is a board connected?",
            "ports": [],
            "boards": []
        }
    
    ioreg_output = get_usb_devices()
    usb_devices = parse_usb_devices(ioreg_output)
    
    boards = []
    for port in ports:
        port_info = {
            "port": port,
            "port_type": "usbserial" if "usbserial" in port else "usbmodem" if "usbmodem" in port else "unknown"
        }
        
        # Match port to USB device
        # usbserial* → CH340/CH341/CP2102 clones
        # usbmodem* → genuine Arduino or native USB
        
        board_info = None
        
        if "usbserial" in port:
            # Likely CH340 — check USB devices for VID
            for dev in usb_devices:
                if dev.get('vid') == 0x1A86:  # CH340/CH341
                    key = (dev['vid'], dev['pid'])
                    if key in BOARDS:
                        board_info = BOARDS[key].copy()
                        board_info["vid"] = f"0x{dev['vid']:04X}"
                        board_info["pid"] = f"0x{dev['pid']:04X}"
                        if 'name' in dev:
                            board_info["usb_product_name"] = dev['name']
                        break
            
            if not board_info:
                board_info = {
                    "board_name": "Unknown CH340/CH341 board",
                    "platformio_id": "uno",
                    "usb_chip": "CH340G (assumed)",
                    "framework": "arduino",
                    "upload_method": "ch340",
                    "upload_note": "CH340 clone detected — use upload-ch340.py",
                    "vid": "0x1A86",
                    "pid": "unknown"
                }
        
        elif "usbmodem" in port:
            # Genuine Arduino or native USB
            for dev in usb_devices:
                key = (dev.get('vid'), dev.get('pid'))
                if key in BOARDS:
                    board_info = BOARDS[key].copy()
                    board_info["vid"] = f"0x{dev['vid']:04X}"
                    board_info["pid"] = f"0x{dev['pid']:04X}"
                    if 'name' in dev:
                        board_info["usb_product_name"] = dev['name']
                    break
            
            if not board_info:
                board_info = {
                    "board_name": "Unknown board (usbmodem)",
                    "platformio_id": "unknown",
                    "usb_chip": "unknown",
                    "framework": "arduino",
                    "upload_method": "standard",
                    "upload_note": "Try pio run -t upload. Board ID may need manual override.",
                    "vid": "unknown",
                    "pid": "unknown"
                }
        
        if board_info:
            board_info["port"] = port
            boards.append(board_info)
    
    return {
        "ports": ports,
        "boards": boards
    }

def main():
    use_json = '--json' in sys.argv
    result = detect()
    
    if use_json:
        print(json.dumps(result, indent=2))
    else:
        if result.get('error'):
            print(f"ERROR: {result['error']}")
            sys.exit(1)
        
        if not result['boards']:
            print("No boards detected.")
            print(f"Serial ports found: {result['ports']}")
            sys.exit(1)
        
        for board in result['boards']:
            print(f"Board:  {board['board_name']}")
            print(f"Port:   {board['port']}")
            print(f"Chip:   {board['usb_chip']}")
            print(f"VID:    {board.get('vid', 'unknown')}")
            print(f"PID:    {board.get('pid', 'unknown')}")
            print(f"Pio ID: {board['platformio_id']}")
            print(f"Note:   {board['upload_note']}")
            print()

if __name__ == '__main__':
    main()
