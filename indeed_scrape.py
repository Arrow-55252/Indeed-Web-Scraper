from bs4 import BeautifulSoup
from curl_cffi import requests
import time
import abbreviation
import csv

class IndeedScrape:

    def input(self):

        occupation_input = input("Please enter occupation to search: ").strip().lower().replace(" ", "+")

        city_input = input("What city do you want to search? ").strip().upper()

        state_input = input("What state would you like to search? ").strip().lower()

        return occupation_input, city_input, state_input
    

    def error_check(self, search_input):
        
        #Checks if job, city, and state is entered
        if search_input[0] and search_input[1] and search_input[2]:

            state_abbrev = abbreviation.abbrev_list()
            #Gives the correct state abbreviation 
            if search_input[2] in state_abbrev:
                state_abbrev = state_abbrev[search_input[2]]
            else:
                print("Sorry the state does not exist, please try again")

        else:
            if not search_input[0]:
                print("The occupation is missing")
            if not search_input[1]:
                print("The city is missing")
            if not search_input[2]:
                print("The state is missing")
        
        return search_input[0], search_input[1], state_abbrev


    def official_scrape(self, input_check):
        HEADERS = {
            "accept" : "*/*",
            "accept-encoding" : "gzip, deflate, br, zstd",
            "accept-language" : "en-US,en;q=0.9",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Mobile Safari/537.36 Edg/145.0.0.0"
        }

        url = f"https://www.indeed.com/jobs?q={input_check[0]}&l={input_check[1]}%2C+{input_check[2]}"

        # impersonate bypasses Indeed's bot detection
        indeed_url = requests.get(url, headers=HEADERS, impersonate="chrome124")

        if indeed_url.status_code != 200:
            print(f" Status Code: {indeed_url.status_code}")

        # Delay prevents rate limiting from Indeed
        time.sleep(3)

        soup = BeautifulSoup(indeed_url.text, "html.parser")

        results = soup.find("ul", class_="css-pygyny eu4oa1w0")
        #Checks if the job exists in the area of search
        if results == None:
            print("Sorry this job listing doesn't exist in this area")
            return
        else:
            job_cards = results.find_all("div", class_="job_seen_beacon")

        #Creates a new csv file named "indeed_jobs"
        with open('indeed_jobs.csv','w', newline='') as csvfile:
            fieldnames = ["Job Title", "Company Name", "Location", "Salary"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
                  
            for job_card in job_cards:
                title = job_card.find("a", class_="jcs-JobTitle css-1baag51 eu4oa1w0")
                company = job_card.find("span", class_="css-19eicqx eu4oa1w0")
                location = job_card.find("div", class_="css-1f06pz4 eu4oa1w0")
                salary = job_card.find("span", class_= "css-zydy3i e1wnkr790")

                #Checks if salary is listed and what the salary listed as
                salary_text = salary.text.strip() if salary and '$' in salary.text.strip() else "Salary Not Listed"

                writer.writerow({
                    "Job Title": title.text.strip(),
                    "Company Name": company.text.strip(),
                    "Location": location.text.strip(),
                    "Salary": salary_text
                })


    def main(self):
        search_input = self.input()
        input_check = self.error_check(search_input)
        scrape = self.official_scrape(input_check)

user = IndeedScrape()
user.main()