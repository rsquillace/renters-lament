# Renters' Lament   

## An Exploration of the Affordability of Rent in Seattle Neighborhoods for Various Industry Wages   

Being a Seattle native, sky rocketing rent is an alarming reality I've consistently faced. As the wealth disparity in the city increases, the rental market caters less and less to those in the lower middle and lower class. There are arguments that wages have kept up with the increase in living costs, though personal experience says otherwise.  

Thus, I've embarked on an exploration of the affordability of rent for standard wages of various industries. In creating a comprehensive display of my findings, I offer a useful tool to advocates of putting systems in place that discourage the displacement of residents earning low wages.  

## _Data_  

I've sourced King County industry wage data from the Employment Security Department. Zillow provides median rental listing records broken down by zip code. It was missing a fair amount of data though, particularly in the earlier years of my investigation (I considered data from 2011 to 2017). To compensate for the missing data, I sourced residential and condo sale records from King County public records. I gathered sale information for residences between 1 and 4 bedrooms, as I felt that would display general trends overall. 

## _Assumptions_  

In working with this data, I had to make some assumptions. I assumed industry wage data for King County reflects that of full time Seattle employees. I also assumed that rental trends within specific zip codes mimic sale trends. My definition of affordable relies on the assumption that one should make three times their rent in a month. This assumption is rooted in personal experience though, as it's been a requirement of every lease I've signed in Seattle in the last decade.  

## _Extrapolation_  

To fill in my missing rental data, I smoothed sale trends for each zip code. I chose to do this because sale trends can be somewhat volatile. The buying market experiences regressions and spikes typically not seen in rental markets. Thus I decided to work with the rolling median of sale trends to extrapolate missing rent. I then normalized by the median sale price for the year corresponding to the earliest known rent, scaled my values and interpolated them. To fill in zip codes that were entirely missing, I examined the ratio of sale prices to the surroundng zip codes, and applied these ratios to known rents for 2017. Follwing, I extrapolated using the same method as above. 

## _Time Series_  

I've created forecasts for each industry wage and zip code individually using an auto ARIMA model. These forecasts are based on small amounts of data (only seven points each), so they likely aren't perfect but I believe they capture general trends. In cases where the trends were extremely unstable, the forecasts tended to be a constant line, but this happened with such a small minority of my data that I chose to use the model anyway. As more data is collected, the ARIMA models will provide better forecasts.   

## _Interactive Map_   

To display my findings, I created a static web app hosting an interactive map using Brython. It displays a map of Seattle zip codes, with drop down menus for both industries and bedrooms. Once those are chosen, the user can move the sliding year scale and the color coded map displaying affordable vs. unaffordable zip codes accordingly. Note, this web app is only running locally for the time being, but will be public on the web very soon!  

## _Moving Forward_  

Continuing on with this project, I intend to rework some of my data. I would like to map one  bedroom sales to one bedroom rent, two bedroom sales to two bedroom rents, etc. Similarly, I would like to consider more incremental data for my forecasts. I intend to use quarterly data for wages and monthly rental data to create Seasonal ARIMA forecasts. This will likely increase my predictive power as the model will have a lot more data to work with. Lastly, I will alter my map to display an affordability gradient rather than a boolean Affordable or not affordable. 




