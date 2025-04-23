Thanks for using this dashboard. 
The "UK Specialty Training Competition Ratios" dashboard was designed by Dr Tom Brisk as part of a project for a "Clinical Data Science" course. 
Any queries should be directed to tombrisk@gmail.com.

This dashboard is designed primarily to demonstrate the trends in competition for a UK specialty training place and make 
visualising the data easier than reading through tables on separate NHS webpages.
It has not been designed to make any political points, nor has it been designed to guide career choices.

Data collected via the feedback form may be used as part of a publication in the future. 
The project and data collection has been discussed with a member of the local NHS trust's research team who 
has agreed that ethics approval is not needed.

Technical notes: 

"Average (outliers removed)", has been calculated by removing any values with fewer than 100 applicants and then 
applying a basic statistical technique of removing values less than or greater than 1.5 * the interquartile range to remove outliers. A mean has then been calculated across all specialties remaining for each year.

The data used is taken from NHS England for competition ratios at ST1 / CT1 level. The future predictions are from a polynomial regression model (4 degrees). These predictions are purely to illustrate recent trends rather than to guide or influence decision making. 
Future competition ratios will almost certainly be very different to the predictions shown here due to the political nature of the problem.
I will update the page with 2025 data when it is released.

"Oxbridge" competition ratios refer to average competition ratios for entry to an 
undergraduate course at the universities of Oxbridge and Cambridge (6:1). 