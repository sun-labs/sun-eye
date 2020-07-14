# Sun Eye
Collection of Machine Learning algorithms and tools used for hyperlocal weather prediction

Each folder contains a different project

## How to use

- Install requirements.txt in each project before running with `pip install -r requirements.txt`

## :cloud: Feature Detection

![Preview of Feature Detection](docs/assets/feature-detection-preview.gif)

Analyze clouds and cloudiness from a stream of images or video.
 - Returns number of clouds and cloudiness factor in JSON format
 - Supports MP4 and static images (JPEG, PNG).
 - Hypnotizing visualizations during analysis

## :bento: Mosaic Generator

Convert a time lapsed image collection
![Preview of Feature Detection](docs/assets/mosaic-before.png)

Into a single image strip that contains the complete time lapse
![Preview of Feature Detection](docs/assets/mosaic-result.png)

 - Used for training Convolutional Neural Nets
 - Mesmerizing images, put it on your wall. wow.

## Algorithms

### Caclculate cloud height from relative humidity and temperature
```
T_x = Temperature of x
h_clouds = height of clouds
T_dp = dew point
RH = relative humidity
```
![eq-dewpoint](https://latex.codecogs.com/svg.latex?\Large&space;T_{dp}=T_{air}-\frac{100-RH}{5})

![eq-height](https://latex.codecogs.com/svg.latex?\Large&space;h_{clouds}=\frac{T_{air}-T_{dp}}{0.00802})


### Calculating width of viewport in meters
```
c = altitude of clouds (m)
z = width of viewport at clouds altitude (m)
alpha = focal view angle of camera (deg)
```

![eq-viewport-width](https://latex.codecogs.com/svg.latex?\Large&space;z=\frac{c*tan(\alpha)}{2})
