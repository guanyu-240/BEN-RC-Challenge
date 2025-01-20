# ExplorerSegment

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | The unique identifier of this segment | [optional] 
**name** | **str** | The name of this segment | [optional] 
**climb_category** | **int** | The category of the climb [0, 5]. Higher is harder ie. 5 is Hors catégorie, 0 is uncategorized in climb_category. If climb_category &#x3D; 5, climb_category_desc &#x3D; HC. If climb_category &#x3D; 2, climb_category_desc &#x3D; 3. | [optional] 
**climb_category_desc** | **str** | The description for the category of the climb | [optional] 
**avg_grade** | **float** | The segment&#39;s average grade, in percents | [optional] 
**start_latlng** | [**LatLng**](LatLng.md) |  | [optional] 
**end_latlng** | [**LatLng**](LatLng.md) |  | [optional] 
**elev_difference** | **float** | The segments&#39;s evelation difference, in meters | [optional] 
**distance** | **float** | The segment&#39;s distance, in meters | [optional] 
**points** | **str** | The polyline of the segment | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


