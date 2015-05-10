The script should be run in the same directory as the folder you would like to sort is placed in.
The script takes in two parameter: First: The name of the directory that tou would like to be sorted.
Second: The name of the directory that you would like the sorted files to be placed in (if that directory
does not exist, one will be created)

Example:


>>> ls
    CleanUp.py	  downloads

>>> python CleanUp.py 'downloads' 'Clean'
    Done

>>> ls
    CleanUp.py    downloads   Clean
