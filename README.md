# MusicBank

The MusicBank project aside from developing tools to manage large digital collection the project defines standards for these collections. These standards are the basis of the tools that are used to establish and maintain a well ordered collection.

## Setup

The code and data for the MusicBank project was developed on Debian 11/12 but written so that it will work on any Unix-ish system like Linux, FreeBSD, Solaris, etc. There are a number of steps necessary to start using these tools. The base assumption is the user has sudo privileges to their system.

* Set the env variable MUSIC_ROOT to point to the starting directory of the music library.

* If necessary install sudo and add the following line to /etc/sudoers
```
    ${USER} ALL=(ALL) NOPASSWD:ALL
```

* Run the script, setup.sh

## Environmant
The environment variable, **MUSIC_ROOT** points to the fully qualified path of the directory that music files are being storied. 
## Data

<hr noshade="noshade">

[Appendix](docs/appendix.md)

[Standards](docs/standards.md)

[Tools](docs/tools.md)

