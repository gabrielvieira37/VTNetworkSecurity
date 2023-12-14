# Data Quality Security: A Zero Trust Architecture Approach


This is the simulation used in the ECE5585 Team 2 Project. The simulation is our zero trust architecture to protect data quality integrity, and was primarily used to investigate the effectivness of a couple MITM attacks on a normal data quality and decision making process, the effectivness of our solution and the changes in efficiency caused by our solution.


## Installation
Testing was done in python 3.10.12
To install dependencies, run the below command in the directory with requirements.txt
```sh
pip install -r requirements.txt
```


## Use
In order to use the simulation, first run reciever.py and mitm.py with no arguments.
Next run sender.py, which takes a few different optional arguments, including -h or --help to get a list while in the command line.
- -ha or --hash, with the syntax '-ha [hash]'. [hash] being one of a list of lowercase valid hashes to use, such as sha256 or md5
- -l or --loop, with the syntax '-l [integer]'. [integer] being the amount of times to loop
- -c or --control, with the syntax '-c'. This flag turns off the digital signature functionality for control testing.


Without the -c flag, the MITM attack should cause the reciever to notify the console of the attack, this is expected behavior. If the MITM attack does not happen or the -c flag is enabled, the reciever will call the decision maker. An alternate to the -l flag is the python_job.sh, which will call sender.py and loop 5 times.

## Running multiple requests
To execute the sender.py multiple times we create a bash script in the file `python_job.sh`.
It receives two positional arguments, the first is the number of times we are going to execute and the second is the hash name.

In that way, to execute `1000` times the sender.py script using the `SHA512` hash, we would have to do the following.

```
chmod +x python_job.sh
./python_job.sh 1000 sha512
```

After executing 1000 requests for each of the hashes `MD5`, `SHA1`, `SHA256`, and `SHA512`. We
can execute the python script `grouped_plots.py` to generate the plots comparing each hash.

```
python grouped_plots.py
```

## Credits
This simulator was written by Samuel Stewart, Gabriel dos Santos Vieira and Lamica AlBaayno for ECE5585 at Virginia Tech.







