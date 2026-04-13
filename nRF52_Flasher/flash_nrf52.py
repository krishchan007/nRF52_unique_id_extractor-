import subprocess
import os

def flash_firmware():
    # Change to the directory where the script is located
    script_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(script_dir)
    # Define the firmware file and check if it exists in the current directory
    firmware_file = "zephyr.hex"
    
      # Get the current directory and list files for debugging
    current_dir = os.getcwd()
    print(f"Current Directory: {current_dir}")
    print("Files in Directory:", os.listdir(current_dir))
    
    # Check if the firmware file exists and is readable
    if not os.path.isfile(firmware_file):
        print(f"Error: Firmware file '{firmware_file}' not found in the current directory.")
        return
    elif not os.access(firmware_file, os.R_OK):
        print(f"Error: Firmware file '{firmware_file}' is not readable.")
        return
    # OpenOCD command
    openocd_cmd = [
        "openocd",
        "-f", "interface/rpi5-test.cfg",
        "-f", "target/nrf52.cfg",
        "-c", "init",
        "-c", "reset init",
        "-c", "halt",
        "-c", "nrf52_recover",
        "-c", f"program {firmware_file} verify",
        "-c", "reset",
        "-c", "exit"
    ]

    try:
        # Run the OpenOCD command
        print("Flashing firmware...")
        result = subprocess.run(openocd_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Print the output and errors (if any)
        print("OpenOCD Output:\n", result.stdout)
        if result.stderr:
            print("OpenOCD Errors:\n", result.stderr)

        # Check if the process was successful
        if result.returncode == 0:
            print("Firmware flashed successfully!")
        else:
            print("Failed to flash firmware. Check the errors above.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    flash_firmware()
