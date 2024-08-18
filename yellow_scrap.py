"""
-*- coding: utf-8 -*-
========================
Python Yellow Pages Email Scrapper
========================
Developed by: Adam Blansett
Email: adam.blansett@gmail.com
========================
"""

import requests
from bs4 import BeautifulSoup
import argparse
import csv


class YellowScrapper():

    def get_url(self, s, l, p):
        r = requests.get("https://www.yellowpages.com/search?search_terms="+s+"&geo_location_terms="+l+"&page="+str(p))
        soup = BeautifulSoup(r.content, 'html.parser')
        data = soup.find_all("div", {"class": "info"})
        x = soup.find_all("div", {"class": "pagination"})
        self.get_data(data,s)
        try:
            if x[0].find_all("a", {"class": "next ajax-page"})[0].text == "Next":
                return True
            else:
                return  False
        except:
            exit("No more pages to scrap")

    def get_data(self, data, cat):
        data_file1 = open( cat + "_data_file.csv", "w")
        data_file = csv.writer(data_file1)
        row = []
        for item in data:
            try:
                name = item.contents[0].find_all("a", {"class": "business-name"})[0].text
                print(name)
                row.append(name)

            except:
                pass
            try:
                address = item.contents[1].find_all("p", {"itemprop": "address"})[0].text
                print(address)
                row.append(address)
            except:
                pass
            try:
                phone = item.contents[1].find_all("div", {"class": "phones phone primary"})[0].text
                print(phone)
                row.append(phone)
            except:
                pass
            try:
                url = "https://www.yellowpages.com" + item.contents[0].find_all("a", {"class": "business-name"})[0].get('href')
                print(url)
                row.append(url)
                er = requests.get(url)
                soup = BeautifulSoup(er.content, 'html.parser')
                erdata = soup.find_all("dd")
                for i in erdata:
                    try:
                        for ci in i.contents:
                            a_tag = ci.find("a",{"class": "email-business"})
                            if a_tag is not None:
                                email = a_tag['href'].split(":")[1]
                                print(email)
                                row.append(email)
                    except:
                        pass
            except:
                pass
            print('**************************************************')
            data_file.writerow(row)
        data_file1.close()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-l', help="location")

    args = parser.parse_args()
    if not args.l:
        exit("Please enter location")

    a = YellowScrapper()

    for i in range(100):
        categories = [
            'Storage Units',
            'Plumbers',
            'Electricians',
            'Carpet Cleaning',
            'Moving Companies',
            'Pest Control Services',
            'Self Storage',
            'Appliance Repair',
            'Garage Door Repair',
            'Appliance Parts',
            'Cleaning Services',
            'Lawn Mower Repair',
            'Moving Truck Rental',
            'AC Repair',
            'Home Security System Installation',
            'Garden Centers',
            'Refrigerator Repair',
            'Plant Nurseries',
            'Tree Service',
            'General Contractors',
            'Dentists',
            'Dermatologists',
            'Optometrists',
            'Physical Therapy',
            'Hospitals',
            'Endocrinologists',
            'Gynecologists',
            'Podiatrists',
            'Neurologists',
            'Ophthalmologists',
            'Gastroenterologists',
            'Pediatricians',
            'Orthodontists',
            'Urologists',
            'Rheumatologists',
            'Obgyn',
            'Physicians',
            'Cardiologists',
            'Radiology',
            'Pediatric Dentists',
            'Auto Parts',
            'Oil Change',
            'Tire Shops',
            'Auto Repair',
            'Window Tinting',
            'Towing',
            'Auto Body Shops',
            'Car Detailing',
            'Roadside Assistance',
            'Auto Glass Repair',
            'Tire Repair',
            'Auto Salvage',
            'Auto Glass',
            'Car Accessories',
            'Wheel Alignment',
            'Used Car Parts',
            'Car Transport',
            'Paintless Dent Repair',
            'Radiator Repair',
            'Car Alarm Installation'
        ]
        for cat in categories:
            print(cat)
            get_next = a.get_url(cat, args.l, i+1)
            if get_next:
                continue
            else:
                break

