import subprocess
import time
import re

# Start Netcat to connect to OpenOCD
print("Connecting with Netcat...")
nc_proc = subprocess.Popen(
    ["nc", "localhost", "4444"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    bufsize=0  # Unbuffered mode for binary data
)

# Function to send commands to Netcat and retrieve raw binary output
def send_nc_command(command):
    # Send command
    print(f"Sending command: {command}")
    nc_proc.stdin.write((command + "\n").encode('ascii'))
    nc_proc.stdin.flush()  # Ensure the command is sent immediately
    time.sleep(0.5)  # Brief delay to allow command processing

    # Read the output in raw binary
    output = b''
    while True:
        chunk = nc_proc.stdout.read(1024)  # Read in chunks
        if not chunk:
            break
        output += chunk
        if b'>' in chunk:  # Detect OpenOCD prompt as raw binary data
            break

    return output

# Send halt and memory read commands
print("Sending halt command...")
send_nc_command("halt")
print("Reading memory from 0x100000A4...")
output = send_nc_command("mdw 0x100000A4 2")

# Process the raw output and decode for regex matching
output_text = output.decode('ascii', errors='ignore')  # Decode for regex parsing

# Extract values for 0x100000A4 using regex
a4_match = re.search(r"0x100000a4:\s+([0-9a-fA-F]+)\s+([0-9a-fA-F]+)", output_text)

if a4_match:
    # Extract the two values and format them as one continuous hex string
    a4_value_1 = a4_match.group(2)  # Second match is MSB
    a4_value_2 = a4_match.group(1)  # First match is LSB
    print(f"Expected Output: {a4_value_1}{a4_value_2}")  # Combined output in requested order
else:
    print("Error: Could not read registers")

# Terminate Netcat process
nc_proc.terminate()
print("Netcat terminated.")
