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
    "number_incrementals":3,
    "exclude_folders": [".git", "__pycache__"],
    "upload_files":false,
    "ftp_server":"ftp_server",
    "ftp_user":"username",
    "ftp_pass":"password",
    "ftp_home":"",
    "delete_after_upload":false
}
~~~

You need to create the folder log on the project path.

## Use

1. First you need to create the database, for that run:
~~~
python3 first_run.py
~~~

With that you create the database.db file.

2. For run backup run:
~~~
python3 Backup.py
~~~