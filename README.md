## Affordability of Rent in Seattle Neighborhoods Based on the Income of Various Industries  

My goal is to create an interactive map showing Seattle divided by neighborhood, and displaying the affordability of rent for residents working in various industries over the last seven years. I am currently in the early stages of development, and working on data cleaning and aggregation.  

Being a Seattle native, the affordability of the rent in the city has been an alarming reality I've consistently faced, as well as most people I know. As the wealth disparity in the city increases, the rental market caters less and less to people in the lower class. I believe a visual representation of this trend will be a useful tool for those interested in studying rental trends, as well as those trying to decipher which neighborhoods tend to be more stable and accommodating to their wages.  

I am sourcing data from Zillow, public records of King County home sales, as well as the Employment Security Department. To extrapolate rental data that is not readily available through Zillow, I intend to look at home sale prices and normalize this data by zip-code and year, then apply that to metric to Seattle rent averages. This is possible under the assumption that home sale prices and rental rates are directly related.     

The industry wage data available through the Employment Security Department is divided by county, of which I am examining King County only. There is likely a wage difference between King County as a whole and the City of Seattle, but for the sake of time I will assume that they coincide, with the exception of industries that typically operate on a minimum wage basis. I will examine the average annual wages and see which fall below the average of a minimum wage worker, and redirect that industry wage to the minimum for years which are applicable.      

From here, I will create time series predictions for industry wages and rental trends to display the potential future of this relationship. Following, I will design a web app that contains a map of Seattle divided by neighborhood. It will have two drop down menus: one for generalized industries, and another for subsects of the industry chosen. There will also be a sliding scale of the years entailed. When adjusted, the shading in the map will change to display whether each neighborhood is generally affordable to someone earning the wages of said industry for the indicated year.   

The metric I am using to consider rent 'affordable' is the requirement an individual makes three times the monthly rent in a month. This is based on personal experience, and having that be a requirement of every rental unit I have applied to over the last decade. Initially I will only consider one bedroom rental units. As time allows, I will consider half of a two bedroom price for a single person, a third of three bedroom prices, etc. 




