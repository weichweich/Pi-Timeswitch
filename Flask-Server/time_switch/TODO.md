# TODO for TimeSwitch
## Model.py

1. Cycle dependency between Pin and Schedule. When creating pins all schedules are created. When creating a schedule the corresponding pin is created... (at the moment schedules are created without pins)

2. Improve observer in SwitchManager (observer) and Model (should be observable). Currently the resources updates the SwitchManager...

## schema.py
1. AttributeError: 'pin.id' is not a valid attribute of <time_switch.model.Sequence> [bad marshmallow schema?]
