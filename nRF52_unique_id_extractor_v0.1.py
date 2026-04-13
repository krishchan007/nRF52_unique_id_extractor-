import subprocess

def execute_openocd_command(command_list):
    """
    Executes the given OpenOCD command and returns stderr output as a list of lines.
    Raises an exception if the command fails.
    """
    process = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stderr_output = []
    
    for line in process.stderr:
        stderr_output.append(line.strip())
    
    process.wait()
    
    if process.returncode != 0:
        raise Exception("OpenOCD command failed.")
    
    return stderr_output

def recover_nrf_chip():
    """Issues the nrf52_recover command to unlock and erase the nRF chip."""
    command = [
        "openocd",
        "-f", "interface/rpi5-test.cfg",
        "-f", "target/nrf52.cfg",
        "-c", "init",
        "-c", "nrf52_recover",
        "-c", "exit"
    ]
    
    try:
        print("Recovering and unlocking the chip...")
        stderr_output = execute_openocd_command(command)
        
        for line in stderr_output:
            if "successfully erased and unlocked" in line:
                print("Chip successfully recovered and unlocked.")
                return True
        
        print("Chip recovery failed.")
        return False

    except Exception as e:
        print("Recovery operation failed with exception:", e)
        return False

def read_nrf_unique_id():
    """Reads the unique ID from the nRF chip after recovery."""
    # Ensure chip recovery before reading the unique ID
    if not recover_nrf_chip():
        print("Failed to recover chip. Unique ID read aborted.")
        return None

    # OpenOCD command to read the unique ID register
    command = [
        "openocd", 
        "-f", "interface/rpi5-test.cfg", 
        "-f", "target/nrf52.cfg", 
        "-c", "init", 
        "-c", "mdw 0x100000A4 2", 
        "-c", "exit"
    ]
    
    try:
        print("Reading unique ID...")
        stderr_output = execute_openocd_command(command)
        
        # Search for the unique ID line
        unique_id = None
        for line in stderr_output:
            if "0x100000a4:" in line:
                parts = line.split()
                if len(parts) >= 3:
                    unique_id_high = parts[-2]
                    unique_id_low = parts[-1]
                    unique_id = unique_id_low + unique_id_high
                    break
        
        if unique_id:
            print("Unique ID:", unique_id)
            return unique_id
        else:
            print("Unique ID not found.")
            return None

    except Exception as e:
        print("An exception occurred during unique ID read:", e)
        return None

# Run the function to recover chip and read the unique ID
read_nrf_unique_id()
