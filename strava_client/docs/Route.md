# Route

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**athlete** | [**SummaryAthlete**](SummaryAthlete.md) |  | [optional] 
**description** | **str** | The description of the route | [optional] 
**distance** | **float** | The route&#39;s distance, in meters | [optional] 
**elevation_gain** | **float** | The route&#39;s elevation gain. | [optional] 
**id** | **int** | The unique identifier of this route | [optional] 
**id_str** | **str** | The unique identifier of the route in string format | [optional] 
**map** | [**PolylineMap**](PolylineMap.md) |  | [optional] 
**name** | **str** | The name of this route | [optional] 
**private** | **bool** | Whether this route is private | [optional] 
**starred** | **bool** | Whether this route is starred by the logged-in athlete | [optional] 
**timestamp** | **int** | An epoch timestamp of when the route was created | [optional] 
**type** | **int** | This route&#39;s type (1 for ride, 2 for runs) | [optional] 
**sub_type** | **int** | This route&#39;s sub-type (1 for road, 2 for mountain bike, 3 for cross, 4 for trail, 5 for mixed) | [optional] 
**created_at** | **datetime** | The time at which the route was created | [optional] 
**updated_at** | **datetime** | The time at which the route was last updated | [optional] 
**estimated_moving_time** | **int** | Estimated time in seconds for the authenticated athlete to complete route | [optional] 
**segments** | [**list[SummarySegment]**](SummarySegment.md) | The segments traversed by this route | [optional] 
**waypoints** | [**list[Waypoint]**](Waypoint.md) | The custom waypoints along this route | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


