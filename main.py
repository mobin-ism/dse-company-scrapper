from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from fastapi import FastAPI

app = FastAPI()

@app.get("/get-ipo-company-name/{trade_code}")
async def get_ipo_company_name(trade_code: str):
    PATH = "/Users/mobinism/Documents/Obboy Labs/webscrapper/msedgedriver"
    option = webdriver.EdgeOptions()
    option.add_argument('headless')
    driver = webdriver.Edge(PATH, options=option)
    baseUrl = "https://www.dse.com.bd/displayCompany.php?name=" + trade_code
    driver.get(baseUrl)
    elements = driver.find_element(by=By.CLASS_NAME, value="BodyHead")
    companyNames = elements.find_elements(by=By.TAG_NAME, value="i")
    for e in companyNames:
        f = open("res/ipo-company-details.txt", "a")
        f.write(trade_code + ":" + e.text + ",\n")
        f.close()
        return e.text
        
    driver.quit()


@app.get("/get-ipo-company-details")
async def readingTradeCodes():
    # cleaning up the file first
    f = open("res/ipo-company-details.txt", "a")
    f.truncate(0)
    f.close()

    ipoCompanies = open("res/trade-codes.txt", "r")
    ipoCompanyNames = ipoCompanies.readline()
    ipoCompanyNames = ipoCompanyNames.split(",")
    for ipoCompanyName in ipoCompanyNames:
        print(await get_ipo_company_name(ipoCompanyName))
    
    ipoCompanies.close()