"""
Small script to check if one should bring an umbrella
or sunscreen (or both) today, based on the forecast,
provided graciously by open-meteo.
"""
import argparse
import sys
import requests


def setup_arg_parser() -> argparse.ArgumentParser:
    """
    Set up argument parser for command-line options.

    Params: none
    Returns: ArgumentParser object
    """
    descr = "This tool checks the weather against the OpenWeather API."
    # Default to URL for open-meteo API when nothing was passed
    def_url = "https://api.open-meteo.com/v1/forecast"
    url_help = """This is the URL for your API endpoint for forecasts.
                You can use this if you want to host your own open-meteo
                instance"""
    check_options = ["rain", "shine"]
    ros_descr = """What to check for as that changes behavior:

                   rain:
                       Returns the %%-chance of rain today & true if >5 %%
                       so you know to pack an umbrella!

                   shine:
                       Returns the UV index for the day & true if >3
                       so you can lather up in sunscreen.
                """
    l_descr = """
                The latitude/longitude of your location in float
                e.g:
                    --lat=42.70
                    --long=23.32
              """
    # I want to format my own text tyvm.
    parser = argparse.ArgumentParser(
                            formatter_class=argparse.RawTextHelpFormatter,
                            description=descr)
    parser.add_argument(
                        "--mode", "-m", choices=check_options, help=ros_descr,
                        required=True
                       )
    parser.add_argument("--lat", "--latitude", required=True, help=l_descr)

    parser.add_argument("--long", "--longitude", required=True, help=l_descr)
    parser.add_argument("--url", default=def_url, help=url_help)

    return parser


def get_weather(url: str, latitude: float, longitude: float) -> dict:
    """
    Function that actually makes the request to the api.

    Params:
        url - string, the URL of our openmeteo install.
        latitude - float, The latitude of the locaton.
        longitude - float, The longitude of the location.
    Returns:
        A requests object
    """
    params = {
	    "latitude": latitude,
	    "longitude": longitude,
	    "daily": ["uv_index_max", "precipitation_probability_max"],
	    "forecast_days": 1
    }
    response = requests.get(url, params=params, timeout=15)
    data = response.json()

    return data


def run():
    """
    Main logic.
    Params: none
    Returns:
        - bool True if mode is rain and probability > 5 %% else False
        - bool True if mode is shine and uv > 3 else False, will output UV
        either way.
    """
    parser = setup_arg_parser()
    # One of the problems I have with argparse is that when you give it nothing
    # it doesn't default to the full help, but rather shows only required args.
    # This is a philosophical debate but I think there should be an easier
    # way... alas this is what the argparse Gods say is good.
    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])
    weather_data = get_weather(url=args.url, latitude=args.lat, longitude=args.long)
    # match case is much easier to read and extend in future
    match args.mode:
        case "rain":
            rain_chance = weather_data['daily']['precipitation_probability_max'][0]
            print(rain_chance)
            return bool(rain_chance > 5)

        case "shine":
            uv_index = weather_data['daily']['uv_index_max'][0]
            print(uv_index)
            return bool(uv_index > 3)

        case _:
            # Default case which shouldn't happen as we would catch it on
            # previous stages. Doesn't hurt to be safe though.
            sys.exit("You shouldn't be seeing this!")

if __name__ == "__main__":
    run()
