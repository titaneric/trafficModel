# Abstract
This is the traffic model built by Python.

The model is based on [Intelligent Driver Model](https://en.wikipedia.org/wiki/Intelligent_driver_model), and most of class design is referenced by volkhin's [RoadTrafficSimulator](https://github.com/volkhin/RoadTrafficSimulator).
# Operation
Double clicking on the grid can create intersection.

Press on the intersection and release on the non-intersection place can create the road.

Mouse wheel can zoom the area.

Mouse click and drag move the area.
# Known problem
The car may stop for unknown reason.

The intersection may "eat" the car for unknown reason.

The curve turning of the car will off the trajectory when the curve is on the intersection and then zooming.  
# Outlook
Will adjust the kernel of the trafficModel and add the signal control in the future.