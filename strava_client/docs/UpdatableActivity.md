# UpdatableActivity

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**commute** | **bool** | Whether this activity is a commute | [optional] 
**trainer** | **bool** | Whether this activity was recorded on a training machine | [optional] 
**hide_from_home** | **bool** | Whether this activity is muted | [optional] 
**description** | **str** | The description of the activity | [optional] 
**name** | **str** | The name of the activity | [optional] 
**type** | [**ActivityType**](ActivityType.md) | Deprecated. Prefer to use sport_type. In a request where both type and sport_type are present, this field will be ignored | [optional] 
**sport_type** | [**SportType**](SportType.md) |  | [optional] 
**gear_id** | **str** | Identifier for the gear associated with the activity. ‘none’ clears gear from activity | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


