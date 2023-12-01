# Solution for Advent of Code day 1
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
import re


def get_number(line, spelled_out=False):
    digits = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9'
    }
    if spelled_out:
        regex = '|'.join([str(value) for value in digits.values()] + list(digits.keys()))
    else:
        regex = '|'.join([str(value) for value in digits.values()])
    regex = '(' + regex + ')'

    num_string = ''
    first_digit = re.search(regex, line).group(1)
    num_string += digits.get(first_digit, first_digit)
    last_digit = re.search('.*' + regex, line).group(1)
    num_string += digits.get(last_digit, last_digit)
    return int(num_string)


puzzle = Puzzle(year=2023, day=1)
data = puzzle.input_data.splitlines()

calibration_data_part_a = []
calibration_data_part_b = []
for line in data:
    calibration_data_part_a.append(get_number(line))
    calibration_data_part_b.append(get_number(line, spelled_out=True))

puzzle.answer_a = sum(calibration_data_part_a)
puzzle.answer_b = sum(calibration_data_part_b)
print(puzzle.answer_a, puzzle.answer_b)
