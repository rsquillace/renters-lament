## Affordability of Rent in Seattle Neighborhoods Based on the Income of Various Industries  

My goal is to create an interactive map showing Seattle divided by neighborhood, and displaying the affordability of rent for residents working in various industries over the last seven years. Currently, I am developing a basic web application that will contain a drop down features, from which the user will select an industry and year and recieve a list of affordable zip-codes based on my calculations.  

Being a Seattle native, the affordability of the rent in the city has been an alarming reality I've consistently faced, as well as most people I know. As the wealth disparity in the city increases, the rental market caters less and less to people in the lower middle and lower classes. I believe a visual representation of this trend will be a useful tool for those interested in studying rental trends, as well as those trying to decipher which neighborhoods tend to be more stable and accommodating to their income level.  

I am sourcing rental data from Zillow, property sale records from King County, and average industry wages from the Employment Security Department. To extrapolate rental data that was not readily available through Zillow, I found median residential sale prices and normalized this data based on the zip-code that seemed to output rents closest to those I already know when applied. This is possible under the assumption that sale price relative to location reflects relative rental rates.     

The industry wage data available through the Employment Security Department is divided by county, of which I am examining King County only. There is likely a wage difference between King County as a whole and the City of Seattle, but for the sake of time I'm assuming they coincide, with the exception of industries that typically operate on a minimum wage basis. For industries where average annual wages fall below the average of a minimum wage worker, I will redirect that industry wage to the minimum for years which are applicable.      

From here, I'm create time series predictions for industry wages and rental trends to display the potential future of this relationship. Eventually, I will design a web app that contains a map of Seattle divided by neighborhood. It will have a drop down menu from which an industry chosen, as well as a sliding scale of the years entailed. When adjusted, the shading in the map will change to display whether each neighborhood is generally affordable to someone earning the wages of said industry for the indicated year.   

The metric I am using to consider rent 'affordable' is the requirement an individual makes three times the monthly rent in a month. This is based on personal experience, and having that be a requirement of every rental unit I have applied to over the last decade. Initially I will only consider one bedroom rental units. As time allows, I will consider half of a two bedroom price for a single person, a third of three bedroom prices, etc. 




