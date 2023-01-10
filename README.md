# IsilonUsageReport
Gets directory sizes from a Dell EMC Isilon. Your FSA reports must be running for this to work.

This is simple Python code to retrieve the sizes of directories and files from an EMC Isilon device through the InsightIQ interface. Once you authenticate into the device you can use API calls to get JSON data.

The advantage of using this is that the data is retrieved immediately, calls to something like `du -h --max-depth=1` could take hours depending on how much data a directory contains.

To get your URL, log into the InsightIQ and click on a file path, the network tab will have the URL that is called.

![InsightIQ URL](https://user-images.githubusercontent.com/36523717/179535820-595c1598-9ba8-4d2d-a64a-722da2b34778.png)

It will look something like this:

    https://isilon01/api/fsa/dir?cluster=f8f212312312312313ec&_dc=2678678607&lin=458787485&sort=log_size_sum&dir=DESC&rsid=14866&limit=10000
  
From this you will want to replace the values `lin` and `limit`. `limit` is how many items are returned, and `lin` seems to be an ID for each file or directory. You will also need your `rsid` value.

`rsid` appears to be Result Set ID, you can grab it as follows:

```
# Get the date of the last FSA report

fsa_report_info = session.get(IQServerURL + "/api/clusters/" + param_cluster + "/fsa/resultsets/published?_dc=" + param_dc)
fsa_report_json = json.loads(fsa_report_info.content)
fsa_report_count = len(fsa_report_json['result_sets'])
fsa_report_date = int(fsa_report_json['result_sets'][fsa_report_count-1]['end_time'])
print("Report information from: " + datetime.utcfromtimestamp(fsa_report_date).strftime('%Y-%m-%d %H:%M'))

# Get the result set ID of the last FSA report
param_rsid = str(fsa_report_json['result_sets'][fsa_report_count-1]['id'])
```

The provided code goes through a `/homes/` directory and summarizes the storage for each user which are sub-folders.

Returned data will usually be in a format like:
```
        {
            "ads_cnt": 0,
            "dir_cnt": 1,
            "file_cnt": 0,
            "has_subdirs": false,
            "lin": 2323147949,
            "log_size_sum": 523310323423,
            "log_size_sum_overflow": 0,
            "name": "foobar_foldername",
            "other_cnt": 0,
            "parent": 2323475492,
            "phys_size_sum": 432358038233
        }
```
