# Solution for Advent of Code day 8
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
import math


def follow_path(instructions, nodes, start, stop):
    steps = 0
    position = start
    while not position.endswith(stop):
        instruction = instructions[steps % len(instructions)]
        if instruction == 'L':
            position = nodes[position][0]
        else:
            position = nodes[position][1]
        steps += 1
    return steps


puzzle = Puzzle(year=2023, day=8)
data = puzzle.input_data.splitlines()
instructions = data[0]

nodes = {}
for line in data[2:]:
    node, unused, left, right = (element.strip('(), ') for element in line.split())
    nodes[node] = (left, right)

steps = []
for node in nodes:
    if node.endswith('A'):
        steps.append(follow_path(instructions, nodes, node, 'Z'))

puzzle.answer_a = follow_path(instructions, nodes, 'AAA', 'ZZZ')
puzzle.answer_b = math.lcm(*steps)
print(puzzle.answer_a, puzzle.answer_b)
