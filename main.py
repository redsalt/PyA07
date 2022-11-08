# from requests import get
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils.file import save_to_file
from utils.file import save_to_csv
# from utils.file import get_from_file
from utils.time import get_now


# get a page source from a web
def get_from_browser(search_address):

  options = Options()
  options.add_argument("--no-sandbox")
  options.add_argument("--disable-dev-shm-usage")

  browser = webdriver.Chrome(options=options)
  browser.get(search_address)

  return browser.page_source


# save the page source
def save_page_source(filename="", content=""):
  now = get_now()
  filename = f"{filename}-{now}"
  save_to_file(filename, content)


# save the job information
def save_job_list(
  filename="",
  joblist={
    'company': '',
    'position': '',
    'location': '',
    'salary': '',
    'type': '',
    'link': ''
  }):
  now = get_now()
  filename = f"{filename}-{now}"
  save_to_csv(filename, joblist)


# extract job information from remoteok.com
def extract_remoteok_jobs(keyword="python"):

  # replace an empty space of the keyword to '-'
  keyword = keyword.replace(" ", "-")

  # url address
  base_url = "https://remoteok.com"
  base_url_head = "/remote-"
  base_url_back = "-jobs"

  # final url address
  search_address = f"{base_url}{base_url_head}{keyword}{base_url_back}"

  # get a page source from the web
  page_source = get_from_browser(search_address)
  save_page_source(keyword, page_source)

  soup = BeautifulSoup(page_source, "html.parser")
  jobs_board = soup.find("table", id="jobsboard")
  jobs_body = jobs_board.find("tbody")
  jobs_tr = jobs_body.find_all("tr")

  # the job list to store
  results = []

  for job_tr in jobs_tr:

    job_td = job_tr.find("td", class_="company position company_and_position")

    if job_td != None:

      job_link = ''
      anchor = job_td.find('a', class_="preventLink")
      if anchor != None:
        job_link = f"{base_url}{anchor['href']}"

      job_title = job_td.find('h2')
      if job_title != None:
        job_title = job_title.string.replace('\n', '').replace(',', '')
      job_company = job_td.find('h3')
      if job_company != None:
        job_company = job_company.string.replace('\n',
                                                 '').replace(',',
                                                             '').rstrip(' ')
      job_locations = job_td.find_all("div", class_="location")

      job_location = ''
      job_salary = ''

      # sometimes there's a part time. if not '-'
      job_type = '-'

      if len(job_locations) > 0:

        for index, element in enumerate(job_locations):

          job_info = job_locations[index].string

          if job_info.find("$") > 0:
            job_salary = job_info.replace(',', '')
          elif job_info.find("Part") > 0:
            job_type = job_info.replace(',', '')
          else:
            # in case of more locations,
            if job_location != '':
              job_location = f"{job_location} and {job_info}".replace(',', '')
            else:
              job_location = job_info.replace(',', '')

        job_data = {
          'company': job_company,
          'position': job_title,
          'location': job_location,
          'type': job_type,
          'salary': job_salary,
          'link': job_link
        }

        # add the extracted item
        results.append(job_data)

  # save the job list
  save_job_list(f"joblist_{keyword}", results)


# start to extract a job list with keyword
extract_remoteok_jobs("python")
