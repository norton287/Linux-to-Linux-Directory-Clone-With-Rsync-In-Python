#!/usr/bin/python3
import subprocess
import logging
import logging.handlers
import os
import glob
import shutil

def sync_www():
    master_ip = "ipofservertodupe"
    slave_ip = "ipofservertodumpto"
    remote_user = "useraccountonremoteserver"
    source_dir = "/var/www/"  # Added trailing slash
    rsync_options = ["-avz", "--delete"]
    exclude_dir = "/var/www/html/dirtoexclude"  # Directory to exclude

    log_file = "/var/log/yourlogdir/sync.log"
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
        # Exclude the directory before rsync
        remote_exclude_dir = f"{remote_user}@{slave_ip}:{exclude_dir}"
        if os.path.exists(exclude_dir):
            logger.info(f"Excluding directory: {exclude_dir}")
            shutil.move(exclude_dir, f"{exclude_dir}.tmp")  # Temporarily move the directory

        logger.info("Starting synchronization...")
        cmd = ["rsync"] + rsync_options + [source_dir, f"{remote_user}@{slave_ip}:{source_dir}"]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            logger.info("Synchronization complete!")
        else:
            logger.error(f"Synchronization failed with error:\n{result.stderr}")

        # Restore the excluded directory
        if os.path.exists(f"{exclude_dir}.tmp"):
            shutil.move(f"{exclude_dir}.tmp", exclude_dir)

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

    # Cleanup old logs
    log_files = sorted(glob.glob(f"{log_file}.*"), key=os.path.getmtime)
    if len(log_files) > 4:  # Keep only 4 archived logs
        for old_log in log_files[:-4]:
            os.remove(old_log)


if __name__ == "__main__":
    sync_www()