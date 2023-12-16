from selenium import webdriver
from tempfile import mkdtemp
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import random
import time
import json
import platform

def handler(event=None, context=None):
    user = 'jarni066@gmail.com'
    password = 'python311'
    keyword = 'Data Scientist'
    url = 'https://www.linkedin.com/feed'


    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            "testing": main_scrape(url,user,password,keyword)
            # "location": ip.text.replace("\n", "")
        }),
    }




def save_cookie(driver, path):
    with open(path, 'w') as filehandler:
        json.dump(driver.get_cookies(), filehandler)

def load_cookie(driver, path):
     with open(path, 'rb') as cookiesfile:
         cookies = json.load(cookiesfile)
         for cookie in cookies:
             driver.add_cookie(cookie)



def main_scrape(url,user,password,keyword):
    os_name = platform.system()
    if os_name == "Windows":
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless=new")
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920x1080")
        options.add_argument("--single-process")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-dev-tools")
        options.add_argument("--no-zygote")
        options.add_argument(f"--user-data-dir={mkdtemp()}")
        options.add_argument(f"--data-path={mkdtemp()}")
        options.add_argument(f"--disk-cache-dir={mkdtemp()}")
        options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36')

        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        
        driver.get(url)

        try:
            try:
                login(driver,user, password)
                time.sleep(3)
                save_cookie(driver, 'cookie.json')
                time.sleep(3)
            except:
                print('Failed login')
                pass
            
        except:

            print('Failed Login')

        driver.close()
        driver.quit()

    elif os_name == "Linux":
        options = webdriver.ChromeOptions()
        service = webdriver.ChromeService("/opt/chromedriver")
        options.binary_location = '/opt/chrome/chrome'
        options.add_argument("--headless=new")
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-gpu")
        # options.add_argument("--window-size=1280x1696")
        options.add_argument("--window-size=1920x1080")
        options.add_argument("--single-process")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-dev-tools")
        options.add_argument("--no-zygote")
        options.add_argument(f"--user-data-dir={mkdtemp()}")
        options.add_argument(f"--data-path={mkdtemp()}")
        options.add_argument(f"--disk-cache-dir={mkdtemp()}")
        # options.add_argument("--remote-debugging-port=9222")
        # options.add_argument(f"--user-agent={user_agen}")
        options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36')

        driver = webdriver.Chrome(options=options, service=service)
        
        driver.get(url)
        load_cookie(driver, 'cookie.json')
        driver.get(url)

        try:
            try:
                login(driver,user, password)
            except:
                print('no login')
                pass
            
            print(f"On page : {driver.current_url}")
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            profile = soup.find('div',{'class':'t-16 t-black t-bold'}).text
            print(f"On account : {profile}")


            data = scrape_job_section(driver,keyword)
            
        except:

            print('Failed Login')
            data = None

        driver.close()
        driver.quit()
    else:
        print("Operating system not recognized as Windows or Linux")

    return data


def login(driver,user, password):
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/main/div/p/a')))
    print('Found SignIn button')
    
    signin_button = driver.find_element(By.XPATH,'/html/body/div[1]/main/div/p/a')
    signin_button.click()
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    page_title = soup.find('title').text
    
    print(page_title)
    print(f'on page {driver.current_url}')
    email_field = driver.find_element(By.XPATH,'/html/body/div/main/div[2]/div[1]/form/div[1]/input')
    
    password_field = driver.find_element(By.XPATH,'/html/body/div/main/div[2]/div[1]/form/div[2]/input')

    email_field.send_keys(user)
    time.sleep(random.uniform(1,2))
    password_field.send_keys(password)
    time.sleep(random.uniform(1,2))


    signin_but = driver.find_element(By.XPATH,'/html/body/div/main/div[2]/div[1]/form/div[3]/button')
    signin_but.click()
    print('Hit sign in')
    time.sleep(5)
   
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    page_title = soup.find('title').text
    
    print(page_title)

    print('on page',driver.current_url)

    # wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[5]/header/div/nav/ul/li[3]/a')))
    time.sleep(random.uniform(1,3))
    # print('logged in')

def scrape_job_section(driver,keyword):
    data = []
    print('Wait element job section')
    time.sleep(5)
    wait = WebDriverWait(driver, 20)

    save_cookie(driver, 'cookie.json')

    job_button = driver.find_element(By.XPATH,'/html/body/div[5]/header/div/nav/ul/li[3]/a')
    job_button.click()
    print('Click job search button')
    # time.sleep(1)
    time.sleep(random.uniform(1,3))
    wait.until(EC.presence_of_element_located((By.CLASS_NAME,'relative')))


    search_fi = driver.find_element(By.CLASS_NAME,'relative')
    search_fi.click()
    time.sleep(random.uniform(1,3))
    print('click job field')

    jobsearch_field = search_fi.find_element(By.XPATH,'/html/body/div[5]/header/div/div/div/div[2]/div[2]/div/div/input[1]')
    time.sleep(random.uniform(1,3))
    
    jobsearch_field.send_keys(keyword)
    jobsearch_field.send_keys(Keys.ENTER)
    wait.until(EC.presence_of_element_located((By.TAG_NAME,'footer')))

    time.sleep(random.uniform(2,4))
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    #Get job headers
    job_block = soup.find('ul',{'class':'scaffold-layout__list-container'})
    job_list = job_block.find_all('li',{'class':'ember-view jobs-search-results__list-item occludable-update p0 relative scaffold-layout__list-item'})
    time.sleep(5)
    print(len(job_list))
    data = data_item(job_list)

    return data

def data_item(job_list):
    data = []
    for job in job_list:
        try:
            job_title = job.find('a',{'class':'disabled ember-view job-card-container__link job-card-list__title'}).text.replace('\\n','').strip()
        except:
            job_title = None

        try:
            job_url = job.find('a',{'class':'disabled ember-view job-card-container__link job-card-list__title'}).attrs['href']
        except:
            job_url = None

        try:
            job_company = job.find('span',{'class':'job-card-container__primary-description'}).text.replace('\\n','').strip()
        except:
            job_company = None


        try:
            job_location = job.find('li',{'class':'job-card-container__metadata-item'}).text.replace('\\n','').strip()
        except:
            job_location = None


        record = {'title':job_title,'url':job_url,'company':job_company,'location':job_location}
        print(record)
        data.append(record)
    return data

handler()


