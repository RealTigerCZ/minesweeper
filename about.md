## Known bugs (many):
- in corners grid lines sometimes are not rendered to the absolute end
- grid lines are not positioned perfectly -> tiles are not rendered in
the middle

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

- reset board by pressing 'R'

- it should work on Windows 10 64-bit with Python 3.9.5 (maybe i newer) and [requirements](https://github.com/RealTigerCZ/minesweeper/blob/master/requirements.txt)
- its somewhat resizable and should work with other resolutions



## Missing features:
- gameplay (yea it does not have any gameplay)
- lots of other thing like settings, proper menu etc.