import subprocess
import time

# Start OpenOCD in the background
print("Starting OpenOCD...")
openocd_proc = subprocess.Popen(
    ["openocd", "-f", "interface/rpi5-test.cfg", "-f", "target/nrf52.cfg", "-s", "tcl"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

# Wait for OpenOCD to initialize
time.sleep(5)
print(f"OpenOCD started with PID: {openocd_proc.pid}. It should now be ready for connections.")

# Keep the process running until manually terminated
try:
    openocd_proc.wait()  # Wait for OpenOCD to keep running in the foreground
except KeyboardInterrupt:
    pass  # Allow for graceful termination if stopped with Ctrl+C

# Clean up on termination
#openocd_proc.terminate()
#print("OpenOCD terminated.")
