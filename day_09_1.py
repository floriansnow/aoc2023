# Solution for Advent of Code day 9
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


class History:
    def __init__(self, line):
        self.history = [[int(num) for num in line.split()]]
        self._next_sequence_possible = True
        self._extrapolate()

    def _next_sequence(self):
        next_sequence = []
        self._next_sequence_possible = False
        for index in range(0, len(self.history[-1]) - 1):
            next_num = self.history[-1][index + 1] - self.history[-1][index]
            if next_num != 0:
                self._next_sequence_possible = True
            next_sequence.append(next_num)
        self.history.append(next_sequence)

    def _extrapolate(self):
        while self._next_sequence_possible:
            self._next_sequence()
        self._expand_forward()
        self._expand_backwards()

    def _expand_forward(self):
        self.history[-1].append(0)
        for index, sequence in list(enumerate(self.history))[-2::-1]:
            sequence.append(sequence[-1] + self.history[index + 1][-1])

    def _expand_backwards(self):
        self.history[-1].append(0)
        for index, sequence in list(enumerate(self.history))[-2::-1]:
            sequence.insert(0, sequence[0] - self.history[index + 1][0])


puzzle = Puzzle(year=2023, day=9)
data = puzzle.input_data.splitlines()
report = []
for line in data:
    report.append(History(line))

puzzle.answer_a = sum([history.history[0][-1] for history in report])
puzzle.answer_b = sum([history.history[0][0] for history in report])
print(puzzle.answer_a, puzzle.answer_b)
