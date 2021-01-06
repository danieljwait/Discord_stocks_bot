# Discord stocks bot
A program to generate fake stocks daily and a Discord bot to view the stocks from a Discord server


## Installation
Run `setup.cmd`, which will do the following:
  - Create a python virtual environment
  - Install all the necessary packages
  - Add your Discord bot token as an environment variable
  - Create the file structure
  - Create a scheduled task to run the `stocks.py` daily


## Usage

#### Automatic

`stocks.py` will automatically run daily to update the stocks

#### Manual

To run either of the programs manually, execute `run.cmd` and pass the python file name as an argument

```shell script
$ run.cmd bot.py
```

Note: __Running `stocks.py` more than once per day will progress the stocks by more than one day__


## Compatibility

The program has only been tested on the following, other versions or software may cause instabilities
- Windows 10 (version 1909)
- Python 3.8.5
- The python packages listed in `requirements.txt`

## Features to add/fix

#### bot.py
- Add `£help` to the bot
- Only allow whitelisted users to user `£update`
- Limit maximum number of days passed to `£graph [days]`

#### stocks.py
- Dynamically change the maximum value on y-axis of graphs
- Add ability to backup data files
