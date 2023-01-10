import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import json
import math

#### Local InsightIQ Server

IQServerURL = 'https://1.2.3.4' # enter the IP address of your Isilon here
IQLoginName = ''
IQLoginPass = ''

#### FUNCTIONS

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

def API_Request(session, lin, limit=25):
  # these must be correct, verify with the web inspector/console in a browser during an InsightIQ session
  param_cluster = "f8f21e1ecb0cd889965b4e26bff7a3cb63ec"
  param_dc = "1664799098438"
  param_rsid = "16643"
  param_sort = "log_size_sum"
  param_dir = "DESC"
  base_string = IQServerURL + "/api/fsa/dir?cluster=" + param_cluster + "&_dc=" + param_dc + "&sort=" + param_sort + "&dir=" + param_dir + "&rsid=" + param_rsid
  #print("URL: " + base_string + f"&lin={lin}&limit={limit}")
  r = session.get(base_string + f"&lin={lin}&limit={limit}" , verify=False)
  return json.loads(r.content)

#### END FUNCTIONS

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

session = requests.Session()

# Authenticate into InsightIQ
params = {'username': IQLoginName, 'password': IQLoginPass}
s = session.post(IQServerURL + "/security/login", data=params, verify=False)
print("Login returned: ", s.status_code)

print("\n")

# Get the home folders
homes_lin = '4323475492' # ID for homes directory
homes_count = 50         # number of dirs to return (sorted by size so top x largest)
homes_info = API_Request(session, homes_lin, homes_count)

# Cycle through each home folder to get sub-folders
for u in range(homes_count-1):
  print('\n', homes_info['usage_data'][u]['name'], "Total Folder Size:", convert_size(homes_info['usage_data'][u]['log_size_sum']))
  folder_limit = 20
  folder_info = API_Request(session, homes_info['usage_data'][u]['lin'], folder_limit)
  folder_count = len(folder_info['usage_data'])
  folder_count = folder_count if (folder_count < folder_limit) else folder_limit

  for f in range(folder_count-1):
    print('\t', convert_size(folder_info['usage_data'][f]['log_size_sum']), folder_info['usage_data'][f]['name'])
