## Known bugs (many):
- in corners grid lines sometimes are not rendered to the absolute end
- grid lines are not positioned perfectly -> tiles are not rendered in
the middle
- it ignores the flag -> its only visual indicator

- bad naming of uncovered and covered (sometimes switch up)

## Features:
- **Click highlighting and canceling:**
    - if you press covered tile -> texture will change
    - if you press uncovered tile -> texture of covered neighbours will change
    - if you press one tile and slide to another -> click will be canceled

- **Advanced clicking controls:**
    - left clicking on uncovered tile with number, uncoveres all their neighbours if you mark same number of bombs as are on number
    - right clicking on uncovered tile with number, flags all their neighbours if the all must be bomb (all covered neighbours + all flaged neighbours are equal to the number)

- it should work on Windows 10 64-bit with Python 3.9.5 (maybe i newer) and [requirements](https://github.com/RealTigerCZ/minesweeper/blob/master/requirements.txt)
- its somewhat resizable and should work with other resolutions
- you can edit constants in code (in data classes and main loop)


## Missing features:
- gameplay (yea it does not have any gameplay, you cant win or lose, you can only run it, click on tiles ale restart it)
- lots of other thing like settings, proper menu etc.