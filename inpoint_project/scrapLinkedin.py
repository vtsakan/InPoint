import csv
from parsel import Selector
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

writer = csv.writer(open('output.csv', 'w+', encoding='utf-8-sig', newline=''))
writer.writerow(['Name', 'Position', 'Company', 'Education', 'Location', 'URL'])


#driver = webdriver.Chrome('C://Users//Hritik//Downloads//chromedriver')
driver = webdriver.Chrome("/usr/bin/chromedriver")
driver.get('https://www.linkedin.com/')

username = driver.find_element_by_name("session_key")
username.send_keys('vasilistsakanikas@gmail.com')
sleep(0.5)

password = driver.find_element_by_name('session_password')
password.send_keys('6972745067')
sleep(0.5)

sign_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')
sign_in_button.click()
sleep(2)

driver.get('https://www.google.com/')
search_query = driver.find_element_by_name('q')
search_query.send_keys('site:linkedin.com/in AND "used cars" AND "Patra"')
search_query.send_keys(Keys.RETURN)
sleep(0.5)

#urls = driver.find_elements_by_xpath('//*[@class = "g"]/ul')

soup = BeautifulSoup(driver.page_source, 'html.parser')
# soup = BeautifulSoup(r.text, 'html.parser')
urls = []
search = soup.find_all('div', class_="g")
for h in search:
    urls.append(h.a.get('href'))


print(urls)
#urls = [url.get_attribute('href') for url in urls]
sleep(0.5)

for url in urls:
    driver.get(url)
    sleep(2)

    sel = Selector(text = driver.page_source)

    name = sel.xpath('//*[@class = "inline t-24 t-black t-normal break-words"]/text()').extract_first().split()
    name = ' '.join(name)
    print(name);

    position = sel.xpath('//*[@class = "mt1 t-18 t-black t-normal break-words"]/text()').extract_first().split()
    position = ' '.join(position)

    experience = sel.xpath('//*[@class = "pv-top-card-v3--experience-list"]')
    company = experience.xpath('./li[@data-control-name = "position_see_more"]//span/text()').extract_first()
    company = ''.join(company.split()) if company else None
    education = experience.xpath('.//li[@data-control-name = "education_see_more"]//span/text()').extract_first()
    education = ' '.join(education.split()) if education else None

    location = ' '.join(sel.xpath('//*[@class = "t-16 t-black t-normal inline-block"]/text()').extract_first().split())

    url = driver.current_url

    print('\n')
    print('Name: ', name)
    print('Position: ', position)
    print('Company: ', company)
    print('Education: ', education)
    print('Location: ', location)
    print('URL: ', url)
    print('\n')

    writer.writerow([name,
                 position,
                 company,
                 education,
                 location,
                 url])

driver.quit()
