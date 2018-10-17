# IMDb_Scrapper
This is a project for Innovaccer Hacker Camp 2019 

This script requires email address and list of favourite TV series for multiple users as input.Store the input data in MySQLdb table(s).A single email is sent to the input email address with all the appropriate response for every TV series. The content of the mail could depend on the following use cases:

  1. Exact date is mentioned for next episode.
  2. Only year is mentioned for next season.
  3. All the seasons are finished and no further details are available.
  
## Initial Configurations

Input your mail details into the from variable and password variable in the script. Also, while using Gmail, enable the Access to less secure apps in order to allow the python script to be able to send mails via it.

## Requirements

1. Python2 must be preinstalled
2. bs4 package - for scraping the web using python
3. Mysql, mysql.connector must be preinstalled.
4. Internet connectivity

## Working
  
### Input format

 Enter the email id and the TV Shows for which you want to find out the release dates of the next episode separated by commas.
![email_input](https://github.com/Akshit312/IMDb_Scrapper/blob/master/data/email_input.png)

 The script will scrape the search results from IMDb and will ask you for a choice, for each TV Series you mentioned. It is         assumed that the desired TV Series is in the top 5 search results when searched in the TV category on IMDb website.
![index_input](https://github.com/Akshit312/IMDb_Scrapper/blob/master/data/index_input.png)

### Output
 The output on the terminal will be as follows, for the TV Shows you’ve entered -
![terminal_output](https://github.com/Akshit312/IMDb_Scrapper/blob/master/data/terminal_output.png)

 Mail will be sent to the given email ID with all the information for The TV Series entered in the input in the following format :
 <p align="center">
<img src="https://github.com/Akshit312/IMDb_Scrapper/blob/master/data/Screenshot_2018-10-17-12-15-17.png" height = "360" width="202.5"> 
  </p>
