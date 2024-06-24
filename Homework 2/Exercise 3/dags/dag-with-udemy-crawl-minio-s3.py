from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from minio import Minio
from minio.error import S3Error
from time import sleep
import pandas as pd

default_args = {
    'owner': 'chowsonice',
    'retries': 1,
    'retry_delay': timedelta(minutes=2)
}

##### Selenium scrap
options = webdriver.FirefoxOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--headless")

def scrap_courses():
    courses = []
    for page in range(1, 5):
        try:
            driver = webdriver.Remote(
                command_executor="http://selenium:4444/wd/hub",
                options=options
            )
            print("Connected to Selenium Grid Hub.")
            try:
                url = f"https://www.udemy.com/courses/search/?p={page}&q=web+development&src=ukw"
                driver.get(url)
                WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.XPATH, "//h1[contains(., 'results for')]")))
                course_elements = driver.find_elements(By.XPATH, "//div[starts-with(@class, 'course-card-module--container')]")
                for course_element in course_elements:
                    # Get general information on the course
                    img_element = course_element.find_element(By.XPATH, ".//img[starts-with(@class, 'course-card-image-module--image')]")
                    img_src = img_element.get_attribute('src')
                    title_element = course_element.find_element(By.XPATH, ".//h3[@data-purpose='course-title-url']//a")
                    title = title_element.text
                    course_url = title_element.get_attribute("href")
                    subtitle = course_element.find_element(By.XPATH, ".//p[contains(@class, 'course-card-module--course-headline')]").text
                    rating = course_element.find_element(By.XPATH, ".//span[@data-purpose='rating-number']").text
                    # price = course_element.find_element(By.XPATH, ".//span[@data-purpose='price-text-container']").text
                    courses.append({
                        'course_url': course_url,
                        'course_thumbnail_url': img_src,
                        'course_title': title,
                        'course_subtitle': subtitle,
                        'course_rating': rating
                    })
            except Exception as e:
                print(f"An error occurred: {e}")
                for entry in driver.get_log('browser'):
                    print(entry)
            finally:
                driver.quit()
                sleep(10)  
            print(courses)
            df = pd.DataFrame(courses)
            try:
                df.to_excel('courses.xlsx', index=False)
            except Exception as e:
                print(f"An error occurred: {e}") 
        except Exception as e:
            print(f"Failed to connect to Selenium Grid Hub: {e}")
#### Upload to Minio
def load_to_minio():
    client = Minio(
        "minio:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )
    try:
        if not client.bucket_exists("udemy"):
            client.make_bucket("udemy")
        client.fput_object(
            "udemy", "courses.xlsx", "courses.xlsx"
        )
    except S3Error as e:
        print(f"An error occurred: {e}")

with DAG(
    dag_id='dag_scrap_udemy_mini_v12',
    description='Scrap courses from Udemy, then upload to minio bucket',
    default_args=default_args,
    start_date=datetime(2024, 6, 8),
    schedule_interval='@daily'
) as dag:
    extract = PythonOperator(
        task_id="extract",
        python_callable=scrap_courses,
    )
    load = PythonOperator(
        task_id='load_to_minio',
        python_callable=load_to_minio,
    )
    extract >> load
