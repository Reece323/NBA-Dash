# nba_vis

This project is where I keep all my files that I use when I analyze all sorts of NBA data.

## Files in this repository

### Projects (.ipynb)

#### .ipynb

__*2020_mvp.ipynb*__ - analysis of the 2020 NBA MVP race between LeBron and Giannis (as of 5/30/20) [Here is my completed analysis.](https://tidbitstatistics.com/are-nba-teams-shooting-better-in-the-bubble/)

__*2020_mvp.ipynb*__ - analysis of the 2019-20 season that compared shooting number before and during the bubble. [Here is my completed analysis.](https://www.tidbitstatistics.com/nba-mvp/)

__*margin_of_victory.ipynb*__ - analysis that showed the '19 - '20 season is set to have the most 40-point blowouts of all time. (as of 12/26/19) [Here is my completed analysis.](https://www.tidbitstatistics.com/NBA-blowouts/)

### .py

__*nba_player.py*__ - contains NBA_Player() object

__*nba_team.py*__ - contains NBA_Team() object

__*nba_season.py*__ - contains NBA_Season() object

__*nba_methods.py*__ - contains various methods to support NBA-related objects I have built in other files

__*pps.ipynb*__ - points per shot analysis - work in progress

## TODO

- [ ] why are there so many blowouts this year? - create new .py file and dig in to it
- [ ] dig in to ppfta, ppfga, pp3pa on pps.ipynb
- [ ] add get_shot_chart() method to NBA_Player class
  - [x] pull data frames
  - [ ] create shot chart from data frames
    - [x] figure out fix, ax
    - [x] colors and background color
    - [x] limiters for the shots
    - [x] kwargs handling
    - [x] team_id df in \_\_init__ method
    - [x] add abbreviation functionality for get_shot_chart
    - [x] chart design
      - [x] add colorbar for hexbins
      - [x] hardwood floor? or other texture?
      - [x] legend as color scale
        - [x] move color ticks to percentile of cbar
    - [x] determine zones
    - [x] hex size as frequency
      - [x] fix hex size plot error
    - [x] fix team/date error (can pass in 0 for teamid)
    - [x] fix scale error in nba_methods
    - [x] add 2pt% and 3pt% on chart
      - [x] if hex kind then add above the legends
    - [x] fix error for make_shot_chart
    - [x] fix playoff data from nba_team.py
    - [ ] parameter for size on/off in hexbins
    - [ ] team logo on chart?
- [ ] add get_shot_dist() method to NBA_Player class
  - [x] histogram with shot dist and freq
  - [ ] brainstorm kinds of charts and figure out parameter control
    - [ ] add bar color - one val or the different shooting %ages
    - [ ] stacked histogram for makes and misses
- [ ] make method when given x players it will compare stats similar to MVP analysis blog post
