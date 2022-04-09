# PyBak

A simple and powerfull backup program

## Features

- Full and incremental backups.
- Upload files with ftp

## Configuration

You need to create configuration.json file:
~~~
{
    "database":"sqlite:///database.db",
    "remote_path":"./output/",
    "local_path":"./folder_to_backup",
    "exclude_folders": [".git", "__pycache__"],
    "ftp_server":"server",
    "ftp_user":"username",
    "ftp_pass":"password"
}
~~~