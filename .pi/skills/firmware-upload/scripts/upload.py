#!/usr/bin/env python3
"""Upload firmware to CH340-based Arduino Uno clone.
Kills serial monitors, pulses DTR to trigger bootloader, retries up to 5 times.

Usage:
    python3 upload.py <demo-dir>
    python3 upload.py demos/01-led-patterns

Auto-builds if not yet compiled.
"""

import serial, time, subprocess, os, sys, glob

def kill_monitors():
    """Kill processes that might be using the serial port."""
    subprocess.run(['tmux', 'kill-session', '-t', 'serial'],
                   capture_output=True, timeout=5)
    for proc in ['pio device monitor', 'avrdude']:
        subprocess.run(['pkill', '-f', proc], capture_output=True, timeout=5)
    time.sleep(0.5)

def detect_port():
    """Find first CH340 serial port."""
    ports = glob.glob('/dev/cu.usbserial*')
    if not ports:
        print("ERROR: No CH340 serial port found. Is the board plugged in?")
        sys.exit(1)
    return ports[0]

def find_hex(demo_dir):
    """Find firmware hex file for a demo."""
    hex_path = os.path.join(demo_dir, '.pio/build/uno/firmware.hex')
    if not os.path.exists(hex_path):
        print(f'Building {demo_dir}...')
        subprocess.run(['pio', 'run'], cwd=demo_dir, timeout=60)
    if not os.path.exists(hex_path):
        print(f"ERROR: Build failed for {demo_dir}")
        sys.exit(1)
    return os.path.abspath(hex_path)

def upload(port, hex_file, max_attempts=5):
    """Pulse DTR and upload via avrdude with retry logic."""
    home = os.path.expanduser('~')
    avrdude = f'{home}/.platformio/packages/tool-avrdude/bin/avrdude'
    conf = f'{home}/.platformio/packages/tool-avrdude/avrdude.conf'

    if not os.path.exists(avrdude):
        print("ERROR: avrdude not found. Install PlatformIO first: brew install platformio")
        sys.exit(1)

    for attempt in range(max_attempts):
        try:
            s = serial.Serial(port, 115200)
            s.dtr = False
            time.sleep(0.1)
            s.dtr = True
            s.close()
            time.sleep(0.08)

            result = subprocess.run([
                avrdude, '-C', conf,
                '-p', 'atmega328p', '-c', 'arduino',
                '-P', port, '-b', '115200', '-D',
                '-U', f'flash:w:{hex_file}:i'
            ], capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                print(result.stdout)
                print(result.stderr)
                return True
            print(f'Attempt {attempt+1}/{max_attempts} failed, retrying...')
        except Exception as e:
            print(f'Attempt {attempt+1}/{max_attempts} error: {e}')
            time.sleep(0.5)

    print(f'\nFAILED after {max_attempts} attempts.')
    print('Try rebooting — CH340 driver may be corrupted.')
    return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 upload.py <demo-dir>")
        print("Example: python3 upload.py demos/01-led-patterns")
        sys.exit(1)

    demo_dir = sys.argv[1]
    if not os.path.isdir(demo_dir):
        print(f"ERROR: {demo_dir} not found")
        sys.exit(1)

    port = detect_port()
    hex_file = find_hex(demo_dir)

    print(f'Demo: {demo_dir}')
    print(f'Port: {port}')
    print(f'Hex:  {hex_file}')
    print('Cleaning up serial port...')
    kill_monitors()
    print('Uploading...')
    sys.exit(0 if upload(port, hex_file) else 1)

if __name__ == '__main__':
    main()
