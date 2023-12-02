# Solution for Advent of Code day 2
# Copyright (C) 2023 Florian Snow <florian@familysnow.net>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-FileCopyrightText: 2023 Florian Snow <florian@familysnow.net>
# SPDX-License-Identifier: AGPL-3.0-or-later

from aocd.models import Puzzle
from collections import defaultdict

def split_data(data):
    split_data = {}
    for line in data:
        game_id = int(line.split(':')[0].split()[1])
        raw_cube_sets = [cube_set.strip() for cube_set in line.split(':')[1].split(';')]
        cube_sets = []
        for cube_set in raw_cube_sets:
            cubes = defaultdict(int)
            parts = cube_set.split(', ')
            for part in parts:
                number, color = part.split()
                cubes[color] = int(number)
            cube_sets.append(cubes)
        split_data[game_id] = cube_sets
    return split_data


def is_game_possible(game):
    max_red = 12
    max_green = 13
    max_blue = 14
    for cube_set in game:
        if cube_set['red'] > max_red:
            return False
        if cube_set['green'] > max_green:
            return False
        if cube_set['blue'] > max_blue:
            return False
    return True


def get_min_numbers_possible(game):
    min_red = 0
    min_green = 0
    min_blue = 0
    for cube_set in game:
        min_red = max(min_red, cube_set['red'])
        min_green = max(min_green, cube_set['green'])
        min_blue = max(min_blue, cube_set['blue'])
    return {'red': min_red, 'green': min_green, 'blue': min_blue}


puzzle = Puzzle(year=2023, day=2)
data = split_data(puzzle.input_data.splitlines())

sum = 0
power = 0
for game_id, game in data.items():
    if is_game_possible(game):
        sum += game_id
    min_numbers_possible = get_min_numbers_possible(game)
    power += min_numbers_possible['red'] * min_numbers_possible['green'] * min_numbers_possible['blue']

puzzle.answer_a = sum
puzzle.answer_b = power
print(puzzle.answer_a, puzzle.answer_b)
