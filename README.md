# Documentation

## Features
#### Disaster Prediction
The type of disaster in an area is identified by a unique model - by using the movement patterns of panic-struck people in a particular area.
#### Real-time Location Tracking
The app monitors your location at all times, so that if a disaster occurs, you are notified immediately.
#### Locating Panic Epicenters
Computational geometry algorithms are used to accurately determine the center of a disaster-stricken area, allowing us to notify nearby people about the same.
#### Android Interface
Our Android app monitors disaster events, even in the background, and then notifies users about the same. It also displays a handy map, allowing users to know their location and the center of the disaster zone.
#### Web Interface
The web interface allows people to see the current disaster areas over the globe. It also behaves as a registration portal.


## How it Works
The Android application constantly monitors the user's position in real time. When the user starts moving, the app sends this information to the server.

Once the server receives this data, it applies a computational geometry algorithm to determine the number of users moving about in that given area.

If this number of users exceeds a certain threshold, the algorithm regards this as an area of interest, and a neural network is used to determine whether it is actually a disaster, and what type of disaster it is.

If it is concluded that it is a disaster, the server sends a message to the app to notify the user about the current situation, and displays a map showing the affected areas.


## Open-Source Libraries and Datasets Used
Leaflet maps (<https://leafletjs.com/>) is used to generate the map for the web interface.

The dataset for training our predictive model is derived from Kaggle's dataset for Human Mobility during Natural Disasters (<https://www.kaggle.com/dryad/human-mobility-during-natural-disasters>).


## Further Enhancements
Due to lack of a GPU, we couldn't create a CNN for predicting disasters. We plan to retrain our model using a convolution architecture once we get access to a GPU.

We plan to add features to the map displayed in our Android interface to plot the route to the nearest safe location, based on the type of disaster. In particular, we plan to choose the route that has relatively high traffic on it, as opposed to the routes recommended by general map services. This is because during a disaster of large scale, it is very likely that roads that are not being used _cannot_, in fact, be used, and this reflects in the lack of any traffic on that route.

In addition, we plan to create an interface for rescue services to pinpoint and locate affected people using the location data from the app.




