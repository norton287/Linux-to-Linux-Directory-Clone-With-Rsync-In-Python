# Directory Sync Script

This Python script simplifies the synchronization of your directories between a master Linux server and a slave Linux server using `rsync`. It includes logging and automatic log rotation to keep your server tidy.

## Features

* **Efficient Synchronization:** Leverages `rsync` for fast, incremental file transfers.
* **Log Management:** Includes detailed logging to `/var/log/yourloggingdirectory/sync.log` with automatic rotation and cleanup of old logs.
* **Error Handling:** Robust error handling for both `rsync` failures and unexpected script errors.
* **Customizable:** Easily adapt the script to your specific server setup and preferences.

## Installation

* Clone Repository: Clone this repository to your master server:
```bash
   git clone https://github.com/norton287/Linux-to-Linux-Directory-Clone-With-Rsync-In-Python.git
```
## Install Dependencies:

```Bash
pip3 install logging
```
## Configuration:

Open `sync_www.py` in a text editor.

### Update the following variables to match your environment:
* master_ip (IP address of the master server)
* slave_ip (IP address of the slave server)
* remote_user (SSH username on the slave server)
* source_dir (Path to the directory you want to sync, including the trailing slash!)
* log_file (Path to the log file; default is /var/log/spindlecrank/sync.log)

## Make Executable and Move:

```Bash
chmod +x sync_www.py
sudo mv sync_www.py /usr/bin/sync_www 
```

## SSH Key Authentication:

* Ensure that you have set up passwordless SSH access from the master server to the slave server using SSH keys for seamless automation. (See below for instructions.)
* Update remote_user with the user associated with the correct ssh key.

## Usage

* You can now run the script from any directory using:

```Bash
sync_www.py
```

## Setting Up SSH Key Authentication

### Generate SSH Keys:

* On the master server, run:
```Bash
ssh-keygen
```

* Follow the prompts to create a new SSH key pair (you can leave the passphrase empty for automatic login).

 * Copy Public Key to Slave Server:

### On the master server, run:

```Bash
ssh-copy-id user@your_slave_ip
```

* Replace user with the SSH username on the slave server and your_slave_ip with the actual IP address.

## Contributing
* Feel free to fork this repository and extend or modify the script to suit your needs. If you have improvements, fixes, or new features, I encourage you to submit a pull request. Your contributions are always welcome!


## **Important Considerations:**

* Replace `your-username` and `your_slave_ip` with your actual server username and slave server IP address. 
* Make sure to update the configuration variables in the `sync_www.py` script as instructed.
* If the user running this script isn't root, you'll need to use `sudo` to move it to the `/usr/bin` directory.
