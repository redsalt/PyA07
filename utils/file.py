def save_to_csv(filename, jobs):

  file = open(f"job/{filename}.csv", "w")
  file.write("Position,Company,Location,Salary,Type,URL\n")

  for job in jobs:
    file.write(
      f"{job['position']},{job['company']},{job['location']},{job['salary']},{job['type']},{job['link']}\n"
    )

  file.close()


def save_to_file(filename="noname", content=""):

  file = open(f"data/{filename}", "w")
  file.write(content)
  file.close()


def get_from_file(filename="noname"):

  file = open(f"data/{filename}", "r")
  content = file.read()
  file.close()

  return content
