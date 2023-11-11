# SimCity 1989

This game, developed using PyGame and designed in Tiled, allows players to build and manage their own city as a mayor with wide powers.

## Table of Contents

- [About](#about)
- [How to Run](#how-to-run)
- [Team](#team)
- [License](#license)

## About <a name="about"></a>

In this 2D top-view game, players develop a city with various zones, service buildings, and connecting roads. The goal is to create a prosperous city with happy citizens and a balanced budget.

### Population

The player's task is to increase the city's population, positively influenced by factors like residents' satisfaction, available workplaces, and the absence of nearby industrial buildings. Maintaining a stable budget is crucial, with overspending leading to citizen dissatisfaction and potential game loss.

### Budget Management

Players earn income through annual fixed taxes on each zone, tied to the population. Expenses include one-time construction costs and maintenance fees. The game interface displays the budget.

### Satisfaction

Each citizen has a satisfaction indicator influenced by factors like low taxes, proximity of workplaces, and public safety. Negative influences include high taxes, industrial proximity, negative budgets, and unbalanced services.

## How to Run <a name="how-to-run"></a>

To play the game:

1. Clone the repository.
2. Navigate to the project directory.
3. Run the following command (You must have Python3 and Pip installed):

```bash
pip install -r requirements.txt
python GameEngine.py
```

Navigate through the menu and the game using the Arrow keys. 
Use the Right-Click button to cancel action or view an item and the Left-Click Mouse button to select or place items.

## Team <a name="team"></a>

- [Yousef Al-Akhali](https://github.com/Yousef-1022)
- [Abdullah Othman](https://github.com/OthmanAbdullah)
- Al-Baraa Al-Sharabi

Jira: [Project Board](https://blog-post.atlassian.net/jira/software/c/projects/BS/boards/4/roadmap) (Disabled)  
GitLab: [Repository](https://szofttech.inf.elte.hu/software-technology-2023/group-3/befk-squad.git) (Private)



## License <a name="license"></a>
MIT License

Copyright (c) 2023 Software technology 2023 / Group 3


Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS," WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
