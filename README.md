# FlameAcid
<img width="64" height="64" alt="acid_logo" src="https://github.com/user-attachments/assets/5ea80193-14a5-4e91-85fc-f3338ab674bd" />


#Acid sucks... so i copy pasted it until it doesn't

---

## How to install

first wait i ahve bullet points
1. download FlameAcid from source
2. unzip it and get the orignal copy
3. find site packages though ```pip show lib-you-have```
4. copy FLAMEACID and put it in site packages

---

## Libs to download so i don't get sued by numpy

numpy... for maths ig

pygame... for rendering

opengl... for more rendering

json wait why am i adding this

toml wait what

pillow... to sleep on

math... for elementary maths

---

## SETUP

```python
import FLAMEACID

screen = FLAMEACID.window((800, 600), "name", "pygame")
screen.init()

while screen.Bro_Running:
  screen.loop()
  screen.fill("black") #Holy shit it supports color names and rgb also holy shit
  #Drawing code here
  screen.update()
```

yeah thats literary it... change the pygame to opengl and boom you are good

## DRAWING SHIT

```python
#how the fuck did i forget how to use my own engine
#me remeber
#between fill and update there goes the drawing shapes thing idfk
#SHUT THE FUCKING YAP UP
#ok i will :(

while screen.Bro_Running:
  screen.loop()
  screen.fill("black") #Holy shit it supports color names and rgb also holy shit
  #Drawing code here
  screen.screen_make_rect(pos, size, color)
  screen.screen_draw_triangle(color, pos, points)
  screen.screen_make_circle(pos, radius, color)
  screen.screen_make_image(pos, size, angle, img_path)
  screen.screen_make_line(point1, point2, color) #oh fuck i opened minecraft accidently
  screen.screen_make_pixel(pos, color) #oh fuck i opened minecraft accidently
  #Drawing code not here
  screen.update()

```

--

## CREDITS

my mom... for making me
past me... so that present me could be alive
