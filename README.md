
# Kingston Housing Project

### By Jay M.
<hr>

## Concept
<hr>
The concept for this project was to make a way to see the current trends and average of housing sales in Kingston Ontario based off the data I was able to pull. I wanted to validate the data that is already listed and at the same time, learn how to grab data of my own.

## The Project
<hr>
I started with a web scraper in Python to pull data from sites that allowed it, (mainly Royal LePage), without crossing their robots.txt parameters and possibly getting into trouble. I made a few files; One to scrape the site for housing sales, one to scrape for rentals, one to update the MongoDB collection, in case there were discrepancies, and I started working on using an asyncronous method direct from python (instead of Express js)

After I had my web scraper working, I made a simple API using Express JS, just to pull in the data and handle sending it to the frontend. I used cors to allow resource sharing between my express server and my react frontend server. This made debugging 10x easier.

... Finish frontend


#### Working on it

The data gathering for the currently listed houses is done.
Next I will grab data for houses listed 5-50 years ago and make comparisons over time.
This step will be tricky as I need to make sure the data is for Houses listed, not houses sold.
If I gather inaccurate data, it won't work.

Sort financial data and figure out the average, low and high for all houses, old and new. 
Show the change in MatPlotLib.
Write a report on what you think, then what you find out.

Why does it feel like housing prices have jumped up 1000% It feels like 10 years ago, you could get a good house for 200k-300k.
Question: How much has the housing market inflated in Kingston Ontario over the last 50 years.

Prediction: Over the last 50 years, I feel the housing market has increased by at least 1000%
But this isn't just about houses for sale, this is about rentals. We will do the same for rentals if we can come up with prior data.
