import datetime
from selenium import webdriver # import selenium to the file
from time import sleep
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from faker import Faker

fake = Faker(locale=['en_CA', 'en_US'])

s = Service(executable_path='../chromedriver')
driver = webdriver.Chrome(service=s)

#--------parabank web App DATA PARAMETERS ----------------
app = 'Parabank'
base_url = 'https://parabank.parasoft.com/'
home_page_url = 'https://parabank.parasoft.com/parabank/index.htm'
home_page_title = 'ParaBank | Welcome | Online Banking'
register_page_url = 'https://parabank.parasoft.com/parabank/register.htm'
register_page_title = 'ParaBank | Register for Free Online Account Access'
# ---------------------------
firstname = fake.first_name()
lastname = fake.last_name()
fullname = f' {firstname} {lastname}'
address = fake.street_address()
city = fake.city()
state = fake.province_abbr()
postalcode = fake.postalcode()
phone = fake.phone_number()
ssn = fake.ssn()
username = f'{fake.user_name()}{fake.pyint(111,999)}'
password = fake.password()

list_id = ['customer.firstName', 'customer.lastName', 'customer.address.street', 'customer.address.city', 'customer.address.state', 'customer.address.zipCode', 'customer.phoneNumber', 'customer.ssn', 'customer.username', 'customer.password', 'repeatedPassword']
list_val = [firstname, lastname, address, city, state, postalcode, phone, ssn, username, password, password]
# ---------------------------


def setup():
    print(f'Launch {app} App')
    print(f'----------------***-----------------')
    # make browser full screen
    driver.maximize_window()

    # give browser up to 30 seconds to respond
    driver.implicitly_wait(30)

    # navigate to App website
    driver.get(base_url)

    # check that URL and the home page title are as expected
    if driver.current_url == home_page_url and driver.title == home_page_title:
        print(f'Yey! {app} website launched successfully :)')
        print(f'{app} Homepage URL: {driver.current_url}, Homepage title: {driver.title}')
        sleep(0.25)
    else:
        print(f'{app} did not launch. check your code or application')
        print(f'Current URL: {driver.current_url}, Page title: {driver.title}')



def teardown():
    if driver is not None:
        print('---------------***----------------')
        print(f'The test is completed at: {datetime.datetime.now()}')
        sleep(0.5)
        driver.close()
        driver.quit()


def register():
    if driver.current_url == home_page_url:
        driver.find_element(By.LINK_TEXT, 'Register').click()
        sleep(0.5)
        if register_page_url in driver.current_url and driver.title == register_page_title:
            print(f'{app} Register page is displayed! Continue to register...')
            sleep(0.25)
            assert driver.find_element(By.XPATH, '//h1[contains(text(),"Signing up is easy!")]').is_displayed()
            sleep(0.25)
            for i in range(len(list_id)):
                fid, val = list_id[i], list_val[i]
                driver.find_element(By.ID, fid).send_keys(val)
                sleep(0.25)
            ######################################
            # press register button to complete registration
            driver.find_element(By.XPATH, '//input[@value = "Register"]').click()
            sleep(0.25)
            teststr = "Welcome"+" "+f'{username}'
            sleep(0.25)

            text1 = driver.find_element(By.XPATH, f'//h1[contains(text(),"Welcome")]').text
            sleep(0.25)

            if f'{username}' in text1:
                print(f'{username} is in the title ')
            sleep(0.25)

            assert driver.find_element(By.XPATH, f'//p[contains(text(),"{fullname}")]').is_displayed()
            assert driver.find_element(By.XPATH, f'//h1[text()="{teststr}"]').is_displayed()
            sleep(0.25)
            print(f'--- User {fullname} is registered successfully ----')


def log_in():
    if home_page_url in driver.current_url: # check we are on the home page

        driver.find_element(By.XPATH, '//input[@name="username"]').send_keys(username)
        sleep(0.25)
        driver.find_element(By.XPATH, '//input[@name="password"]').send_keys(password)
        sleep(0.25)
        driver.find_element(By.XPATH, '//input[@value="Log In"]').click()
        sleep(0.5)
        try:
            assert driver.find_element(By.XPATH, f'//p[contains(.,"{fullname}")]').is_displayed()
            sleep(0.5)
            print(f'--- User {fullname} logged in successfully ----')
        except NoSuchElementException as nse:
            print('Element is not found')


def log_out():
    driver.find_element(By.LINK_TEXT, 'Log Out').click()
    assert driver.find_element(By.XPATH, '//h2[contains(., "Customer Login")]').is_displayed()
    print(f'user {fullname} log out successfully!')



# setup()
# register()
# log_out()
# log_in()
# log_out()
# teardown()