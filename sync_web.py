#!/usr/bin/python3
import subprocess
import logging
import logging.handlers
import os
import glob

def sync_www():
    master_ip = "192.168.1.29"
    slave_ip = "192.168.1.25"
    remote_user = "dupeit"
    source_dir = "/var/www/"  # Added trailing slash
    rsync_options = ["-avz", "--delete"]

    log_file = "/var/log/spindlecrank/sync.log"
    log_dir = os.path.dirname(log_file)
    os.makedirs(log_dir, exist_ok=True)  # Create log directory if it doesn't exist

    logger = logging.getLogger("sync_logger")
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=1048576, backupCount=4  # 1 MB
    )
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    try:
        logger.info("Starting synchronization...")
        cmd = ["rsync"] + rsync_options + [source_dir, f"{remote_user}@{slave_ip}:{source_dir}"]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            logger.info("Synchronization complete!")
        else:
            logger.error(f"Synchronization failed with error:\n{result.stderr}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

    # Cleanup old logs
    log_files = sorted(glob.glob(f"{log_file}.*"), key=os.path.getmtime)
    if len(log_files) > 4:  # Keep only 4 archived logs
        for old_log in log_files[:-4]:
            os.remove(old_log)


if __name__ == "__main__":
    sync_www()
