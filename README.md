# 1. Introduction
This tool was created at the request of my good friend Alex. For more details on the requirements for it checkout the [original specification](./spec.md).
For a brief overview it helps him track weather to bring an umbrella today or douse in sunscreen. The main concept is that it is to be ran on a CLI so it only returns True or False values and prints out the UV index when told to.
# 2. Installation
## 1. Requirements
The script is Python so it can be run as is but it does use features only available in >3.10. 
- Python > 3.10 *or*:
- Docker 24.0.5 (only tested on this version, probably works on others)
- The host where this is running needs to be able to access the API you are checking against (default for that is https://open-meteo.com)
- You need to know the latitude and longitude of the location you would like to check.
- Suncreen
- An umbrella.
## 2. Standalone
If you don't need to run the script in a container, I salute you and your bravery! 

Once you've installed Python 3.10 or greater and PIP, you can simply copy the source code from this repository e.g:

```
cd /where/i/want/the/code
git clone git@github.com:lutenica/rain-or-shine.git
```
Install the requirements:
```
pip install -r /where/i/want/the/code/rain-or-shine/requirements.txt
```
Then to execute you can simply do:
```
python /where/i/want/the/code/src/main.py --lat=X.X --long=Y.Y --url https://my-awesome-fake.api.fake/forecast --mode=rain
```
That's it!
## 3. Docker
Once you've installed Docker you can clone the repo again using the steps from the stand-alone install and then use the [Dockerfile](./Dockerfile) in the repo:
```
cd /where/i/want/the/code/rain-or-shine/
docker build . -t $WHAT_I_WANT_THE_APP_TO_BE_CALLED
```
The image should then build and you can proceed with executing commands on it following the steps in the next chapter.

# 3. Usage
## 1. For standalone:
Simply navigate to the directory where the tool is copied with one of the methods above and execute the command. Example usage:
```
python main.py --lat=42.6975 --long=23.3241 --mode=rain
```
Bingo-bango-bongo you have your results.
## 2. Docker:
For running it within docker the steps are simple. Once you've built the image to execute the script one needs to run:
```
docker run --rm rain-or-shine --lat=X.X --long=Y.Y --mode=mode_of_choice 
```
## All options:
Below is a comprehensive list of all available options and all of their values.
```
  -h, --help            show this help message and exit
  --mode {rain,shine}, -m {rain,shine}
                        What to check for as that changes behavior:

                                           rain:
                                               Returns the %-chance of rain today & true if >5 %
                                               so you know to pack an umbrella!

                                           shine:
                                               Returns the UV index for the day & true if >3
                                               so you can lather up in sunscreen.

  --lat LAT, --latitude LAT

                                        The latitude/longitude of your location in float
                                        e.g:
                                            --lat=42.70
                                            --long=23.32

  --long LONG, --longitude LONG

                                        The latitude/longitude of your location in float
                                        e.g:
                                            --lat=42.70
                                            --long=23.32

  --url URL             This is the URL for your API endpoint for forecasts.
                                        You can use this if you want to host your own open-meteo
                                        instance

```
# 4. Contributing
Thank you for your interest in contributing to my project to help Alex! There are a couple of things to note before suggesting your changes:
1. The main branch is write protected, so you would need to create a new branch and propose a PR.
2. The automation in place uses ruff for linting, syntax highlighting and all of the other fancy features it offers. Please make sure that your local IDE is set up to run with it. Any failures in ruff will be rejected.
3. Signed commits are required. You can read more about setting that up [here](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits).
4. Be nice and all of the usual things people say in these repos. Make sure that you read the [specifications](./spec.md) before contributing, so that you are sure your changes align with the actual end-user requirements.
# 5. Design choices
## 1. Python specifics
I decided to use argparse. Even though there are newer and faster options like [Click](https://click.palletsprojects.com/en/8.1.x/why/) and there are things which really annoy me about argparse (which you can see in my comments in code), I do place great value on the fact that argparse comes pre-packged into the stdlib, due to portability and faster build times (for containers).

Open-meteo do offer a library to handle their requests - [openmeteo-requests](https://pypi.org/project/openmeteo-requests/) which is more effecient due to using flat buffers, however, the amount of data being transferred doesn't warrant that and we come back to simplicity and maintainability. So I chose to use the regular requests library which is guaranteed to be kept up to date due to it's ubiquity.

Lastly, I choose to use [match-cases](https://docs.python.org/3/whatsnew/3.10.html#pep-634-structural-pattern-matching) as I really dislike the if-elif-else spaghetti Python can sometimes turn into. This is something that, as a person coming from Bash, where case has been around for quite a while (since the bourne shell (/bin/sh) which released the same year "A New Hope" came out), has urked me, but thankfully they addded it! 

## 2. Open-meteo
So why did I choose this no-name thing? Couple of reasons:

First they're the only actually open source weather API. Meaning one can easily host it locally, more details [here](https://github.com/open-meteo/open-meteo/tree/main). This makes any code here much more re-usable, where as otherwise we are left with working only with one source of data. Also sef-hosted is great! 

Second and more critical, all other sources didn't provide forcasting for free, so they were a bit of a non-starter. 

I really wanted an API which doesn't do latitude and longitude but rather city names with countries, so that it's more human friendly, but all of those wanted money and it's not a big deal at the moment. I did consider converting "City, Country" to actual coordinates, but that requires some ugly libraries which want usernames and passwords and would take much longer to write from scratch (connect to some sort of map api and get the lat and long that way, I'm looking into credible city database APIs).

## 3. Various other things
Currently all code contributions can be done via PR. Ideally when merged, it would trigger a github action to build but those require money to run, so I'm foregoing it at this time. We do have dependabot to monitor our requirements.txt for newer versions of libraries once a week though!
