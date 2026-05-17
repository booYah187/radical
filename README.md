Radical Ed python screensaver
![Alt text](https://github.com/booYah187/radical/blob/main/radical.gif?raw=true)

open radical.py, adjust WIDTH, HEIGHT = to your resolution, may need to adjust x = and y = under WARNING POPUP to recenter. 

any custom terminal output text can be added under SMALL_TEXT and LARGE_TEXT. size of faces can be adjusted using size = int(160 * scale) and  img = pygame.transform.scale(img, (160, 160)) under FACES. swordfish appearance frequency can be adjusted at SWORDFISH_SPAWN_CHANCE = 0.0003. 
everything can be adjusted. mess around. get weird with it. send any cool configs back.

can be set as screensaver however you want. i use xidlehook: 
xidlehook --not-when-fullscreen --timer 300 "$HOME/radical/radical-idle.sh && xflock4" ""