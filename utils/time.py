import datetime

def get_now():
  
  now = datetime.datetime.now()

  year = now.strftime("%Y")
  month = now.strftime("%m")
  day = now.strftime("%d")
  weekday = now.strftime("%a")

  hour = now.strftime("%H")
  minute = now.strftime("%M")
  second = now.strftime("%S")
  
  file_now = f"{year}-{month}-{day}-{weekday}-{hour}{minute}{second}"

  return file_now
