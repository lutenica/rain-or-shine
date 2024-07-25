# Will It Rain or Shine?
These are the words of Alex who requested this tooling, I'm paraphrasing him a bit for dramatic effect:

```
I am terrible about remembering to bring an umbrella with me on rainy days and sunscreen on sunny days. Now I just
need a script that runs every day at 6am, checks the weather and lets me know whether I need to pack an umbrella or
sunscreen.
I need a tool that will look for the current weather in my locale using a public API. It will need to accept at least one command line argument with two options: rain,shine
If the rain argument is passed:
* Check today's percent chance for rain:
* Output the percent chance of rain
* If there is a greater than 5% chance of rain, return True

If the shine argument is passed:
* Check today's prediction for UV index:
* Output the predicted UV Index
* If the UV Index is predicted to be greater than 3, return True
The tool might need to accept a current location argument depending on which API we end up using. Some APIs will perform geo lookups based on IP while some require you to specify your location. Feel free to code this part however you see fit.
```
