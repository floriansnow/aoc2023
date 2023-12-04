# Solution for Advent of Code day 4
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


class Card:
    def __init__(self, data):
        self.id = int(data.split(':')[0].split()[1])
        self.winning_numbers = [int(number) for number in data.split(':')[1].split('|')[0].split()]
        self.available_numbers = [int(number) for number in data.split(':')[1].split('|')[1].split()]
        self.wins = self._get_wins()
        self.points = self._get_points()

    def _get_wins(self):
        return len([number for number in self.available_numbers if number in self.winning_numbers])

    def _get_points(self):
        if self.wins < 1:
            return 0
        return 2 ** (self.wins - 1)

    
class Table(dict):
    def __init__(self, data):
        self._cards = [Card(line) for line in data] 
        self._card_counts = {i: 1 for i in range(len(data))}
        self._process()

    def _process(self):
        for index in self._card_counts:
            number = self._card_counts[index]
            card = self._cards[index]
            for i in range(1, card.wins + 1):
                self._card_counts[index + i] += number

    def get_points_total(self):
        return sum([card.points for card in self._cards])
        
    def get_cards_total(self):
        return sum(self._card_counts.values())


puzzle = Puzzle(year=2023, day=4)
data = puzzle.input_data.splitlines()
table = Table(data)

puzzle.answer_a = table.get_points_total()
puzzle.answer_b = table.get_cards_total()
print(puzzle.answer_a, puzzle.answer_b)
