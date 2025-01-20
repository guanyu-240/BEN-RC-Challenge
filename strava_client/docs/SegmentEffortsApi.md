# swagger_client.SegmentEffortsApi

All URIs are relative to *https://www.strava.com/api/v3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_efforts_by_segment_id**](SegmentEffortsApi.md#get_efforts_by_segment_id) | **GET** /segment_efforts | List Segment Efforts
[**get_segment_effort_by_id**](SegmentEffortsApi.md#get_segment_effort_by_id) | **GET** /segment_efforts/{id} | Get Segment Effort


# **get_efforts_by_segment_id**
> list[DetailedSegmentEffort] get_efforts_by_segment_id(segment_id, start_date_local=start_date_local, end_date_local=end_date_local, per_page=per_page)

List Segment Efforts

Returns a set of the authenticated athlete's segment efforts for a given segment.  Requires subscription.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: strava_oauth
configuration = swagger_client.Configuration()
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = swagger_client.SegmentEffortsApi(swagger_client.ApiClient(configuration))
segment_id = 56 # int | The identifier of the segment.
start_date_local = '2013-10-20T19:20:30+01:00' # datetime | ISO 8601 formatted date time. (optional)
end_date_local = '2013-10-20T19:20:30+01:00' # datetime | ISO 8601 formatted date time. (optional)
per_page = 30 # int | Number of items per page. Defaults to 30. (optional) (default to 30)

try:
    # List Segment Efforts
    api_response = api_instance.get_efforts_by_segment_id(segment_id, start_date_local=start_date_local, end_date_local=end_date_local, per_page=per_page)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SegmentEffortsApi->get_efforts_by_segment_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **segment_id** | **int**| The identifier of the segment. | 
 **start_date_local** | **datetime**| ISO 8601 formatted date time. | [optional] 
 **end_date_local** | **datetime**| ISO 8601 formatted date time. | [optional] 
 **per_page** | **int**| Number of items per page. Defaults to 30. | [optional] [default to 30]

### Return type

[**list[DetailedSegmentEffort]**](DetailedSegmentEffort.md)

### Authorization

[strava_oauth](../README.md#strava_oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_segment_effort_by_id**
> DetailedSegmentEffort get_segment_effort_by_id(id)

Get Segment Effort

Returns a segment effort from an activity that is owned by the authenticated athlete. Requires subscription.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: strava_oauth
configuration = swagger_client.Configuration()
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = swagger_client.SegmentEffortsApi(swagger_client.ApiClient(configuration))
id = 789 # int | The identifier of the segment effort.

try:
    # Get Segment Effort
    api_response = api_instance.get_segment_effort_by_id(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SegmentEffortsApi->get_segment_effort_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| The identifier of the segment effort. | 

### Return type

[**DetailedSegmentEffort**](DetailedSegmentEffort.md)

### Authorization

[strava_oauth](../README.md#strava_oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

