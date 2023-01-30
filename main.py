# Please enter the year, make and model of the car you are looking for inside the quotations
year = "2010"
make = "Ford"
model = "Mustang"

# Please enter the minimum year and maximum year for the vehicle
minYear = "2010"
maxYear = "2020"

# Please enter your zip code, and the radius for your search
zip = "48091"
radius = "300"

# Please enter the maximum and minimum mileage and cylinders
maxMiles = "50000"
cylinders = "8"

# Please enter where you would like to store the file
fileLocation = "/Users/tasniamahzabin/Documents/"
fileName = "Cars"

#-----------------------------------------DO NOT TOUCH ANYTHING BELOW--------------------------------------------
import time;
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

# Sort
def sorting(x):
    return x[1]

# generating the url for the specific car
url = "https://www.autotempest.com/results?make=" + make.lower() + "&model=" + model.lower() + "&zip=" + zip + \
      "&radius=" + radius + "&minyear=" + minYear + "&maxyear=" + maxYear + "&maxmiles=" + maxMiles + "&cylinders=" + cylinders

# set up web driver
options = Options()
options.add_argument("start-maximized")
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
driver.get(url)

time.sleep(5)

# Variables
dataList = []       # The list of data to send to a csv file
currentCar = 1      # To keep track of which car the head is currently at
cars = driver.find_elements(By.XPATH, "(//div[@class='result-wrap'])")   # List of all of the cars
timestr = time.strftime(" %m-%d-%Y")

time.sleep(2)

for car in cars:
    head = driver.find_element(By.XPATH, ("(//a[@class='listing-link image-link'])[" + str(currentCar) + "]"))
    link = head.get_attribute("href")
    descriptions = car.text.split("\n")
    descriptions.remove("Share")
    descriptions.append(link)

    if len(descriptions) == 8 or len(descriptions) == 7:
        if len(descriptions) == 7:
            descriptions.insert(5, "No dealer")

        if len(descriptions) == 8 and descriptions[1] != "Inquire":
            descriptions[1] = int(descriptions[1].strip("$").replace(",", ""))
            dataList.append(descriptions)

    currentCar += 1


dataList.sort(key=sorting)
df = pd.DataFrame(dataList, columns=['Car Name', 'Price', 'Mileage', 'Date Posted', 'Location (Distance)', 'Seller', 'Description', 'Link'])
df.to_csv(fileLocation+fileName+timestr+".csv", index=True, encoding= 'utf-8')

driver.close()
