# Smart Planter

There are already a lot of open-source projects controlling plant growing conditions. This one is not special, but it is mine. Since I am doing the work anyway, I figured I might as well share it with anybody interested. My goal was to learn 3D printing, electronics design, micropython,  and GitHub, so to some this planter might appear way over-engineered. I am also doing this in my free time (i.e., nights and weekends), so progress is slow. For anyone interested in following what I have done, I will post step-by-step instructions here and upload any relevant files you might need to replicate my results. 


## Printing Parts:

The stl folder has all of the 3D models required for this setup. Here is the description of each:

- planter: This is the main planter container to which other accessories will be attached
- light_arm_anchor: This is the anchor that attaches to the planter. It is designed to hold the arm pieces in place while providing small space for the cables to go inside
- light_arm_straight: This is a straight piece of the light arm designed to interface with the light_arm_anchor, and either another light_arm_straight piece or light_arm_turn piece. Because it is hallow, it allows internal cable to power the grow light



## Micropython code:

I used a Raspberry Pi Pico W for this project, which can run micropython code. The folder [micropython](https://github.com/jakupsko/plant_house/tree/main/micropython) has files I individually designed to be self-contained (i.e., can be used for other projects). 
