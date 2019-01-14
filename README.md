# sun-eye
Your everyday eye of the sun


## Caclculate cloud height from relative humidity and temperature
```
h_clouds = height of clouds
T_dp = dew point
```
![eq-dewpoint](http://www.sciweavers.org/tex2img.php?eq=T_{dp}=T-\frac{100-RH}{5}&bc=White&fc=Black&im=jpg)

![eq-heightclouds](http://www.sciweavers.org/tex2img.php?eq=h_{clouds}=\frac{T_{air}-T_{dp}}{0.00802}&bc=White&fc=Black&im=jpg)


## Calculating width of viewport in meters
```
c = altitude of clouds (m)
z = width of viewport at clouds altitude (m)
alpha = focal view angle of camera (deg)
```
![eq-viewport](http://www.sciweavers.org/tex2img.php?eq=z=\frac{c*tan(\alpha)}{2}&bc=White&fc=Black&im=jpg)
