# sun-eye
Your everyday eye of the sun


## Caclculate cloud height from relative humidity and temperature
```
h_clouds = height of clouds
T_dp = dew point
RH = relative humidity
```
![eq-dewpoint](https://latex.codecogs.com/svg.latex?\Large&space;T_{dp}=T_{air}-\frac{100-RH}{5})

![eq-height](https://latex.codecogs.com/svg.latex?\Large&space;h_{clouds}=\frac{T_{air}-T_{dp}}{0.00802})


## Calculating width of viewport in meters
```
c = altitude of clouds (m)
z = width of viewport at clouds altitude (m)
alpha = focal view angle of camera (deg)
```

![eq-viewport-width](https://latex.codecogs.com/svg.latex?\Large&space;z=\frac{c*tan(\alpha)}{2})
