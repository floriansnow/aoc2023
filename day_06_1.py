# Solution for Advent of Code day 6
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


def get_winning_possibilities(race):
    wins = []
    for t in range(race[0]):
        distance = t * (race[0] - t)
        if distance > race[1]:
            wins.append((t, distance))
    return wins

puzzle = Puzzle(year=2023, day=6)
data = puzzle.input_data.splitlines()

times = [int(t) for t in data[0].split()[1:]]
distances = [int(t) for t in data[1].split()[1:]]
races = zip(times, distances)

result = 1
for race in races:
    result *= len(get_winning_possibilities(race))

race2 = (int(''.join(data[0].split()[1:])), int(''.join(data[1].split()[1:])))

puzzle.answer_a = result
puzzle.answer_b = len(get_winning_possibilities(race2))
print(puzzle.answer_a, puzzle.answer_b)