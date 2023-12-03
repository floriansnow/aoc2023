# Solution for Advent of Code day 3
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


class Schematic:
    
    def __init__(self, data):
        self._schematic = {}
        for y, line in enumerate(data):
            for x, character in enumerate(line):
                if character == '.':
                    continue
                self._schematic[(x, y)] = character
        self._max_x = x
        self._max_y = y

    def _get_neighbors(self, point):
        for x_offset in range (-1, 2):
            for y_offset in range(-1, 2):
                x = point[0] + x_offset
                y = point[1] - y_offset
                if point != (x, y):
                    yield x, y

    def has_adjacent_symbol(self, point):
        for neighbor in self._get_neighbors(point):
            try:
                if not self._schematic[neighbor].isdigit():
                    return neighbor
            except KeyError:
                continue
        return False

    def get_numbers_adjacent_to_symbols(self):
        numbers = {}
        number = ''
        adjacent_to_symbol = False
        for y in range(self._max_y + 1):
            for x in range(self._max_x + 1):
                if ((x, y) not in self._schematic or not self._schematic[(x, y)].isdigit()) and number == '':
                    continue
                elif (x, y) not in self._schematic or not self._schematic[(x, y)].isdigit():
                    if adjacent_to_symbol:
                        if adjacent_to_symbol not in numbers:
                            numbers[adjacent_to_symbol] = []
                        numbers[adjacent_to_symbol].append(int(number))
                    number = ''
                    adjacent_to_symbol = False
                elif self._schematic[(x, y)].isdigit():
                    number += self._schematic[(x, y)]
                    if not adjacent_to_symbol:
                        adjacent_to_symbol = self.has_adjacent_symbol((x, y))
        return numbers

    def get_part_number_sum(self):
        return sum([sum(number) for number in schematic.get_numbers_adjacent_to_symbols().values()])

    def get_gear_ratio_sum(self):
        numbers_adjacent_to_symbols = self.get_numbers_adjacent_to_symbols()
        gear_part_numbers = {point: numbers_adjacent_to_symbols[point] for point in numbers_adjacent_to_symbols if self._schematic[point] == '*' and len(numbers_adjacent_to_symbols[point]) == 2}
        return sum([a * b for a, b in gear_part_numbers.values()])
                   
    def __repr__(self):
        repr = []
        for y in range(self._max_y + 1):
            line = []
            for x in range(self._max_x + 1):
                try:
                    line.append(self._schematic[(x, y)])
                except KeyError:
                    line.append('.')
            repr.append(''.join(line))
        return '\n'.join(repr)
    


puzzle = Puzzle(year=2023, day=3)
data = puzzle.input_data.splitlines()

schematic = Schematic(data)

puzzle.answer_a = schematic.get_part_number_sum()
puzzle.answer_b = schematic.get_gear_ratio_sum()
print(puzzle.answer_a, puzzle.answer_b)
