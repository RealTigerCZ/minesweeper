## Known bugs (many):
- in corners grid lines sometimes are not rendered to the absolute end
- grid lines are not positioned perfectly -> tiles are not rendered in
the middle
- smile button is not always best size and in the correct position 
    - y_padding its sometimes also incorrect

## Features:
- **Click highlighting:**
    - if you press covered tile -> texture will change
    - if you press uncovered tile -> texture of covered neighbours will change

- **Click cancelling:**
    - when you press one tile and slide to another
    - when you left click on tile with flag
    - when game is won or lost 

- **Advanced clicking controls:**
    - left clicking on uncovered tile with number, uncoveres all their neighbours if you mark same number of bombs as are on number
    - right clicking on uncovered tile with number, flags all their neighbours if the all must be bomb (all covered neighbours + all flaged neighbours are equal to the number)

- **Win and lose detection**
    - and some "graphic"

- **Reseting board** 
    - by pressing 'R'
    - by clicking on smile button

- **Smile button**
    - 4 game states -> 4 textures
    - board reseting

- it should work on Windows 10 64-bit with Python 3.9.5 (maybe i newer) and [requirements](https://github.com/RealTigerCZ/minesweeper/blob/master/requirements.txt)
- its somewhat resizable and should work with other resolutions



## Missing features:
- gameloop
- lots of other thing like settings, proper menu etc. see [Goals](https://github.com/RealTigerCZ/minesweeper/blob/master/readme.md#goals)