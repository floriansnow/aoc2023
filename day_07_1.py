# Solution for Advent of Code day 7
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
from enum import Enum


class HandType(Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


class Hand:
    def __init__(self, raw_hand):
        cards, bid = raw_hand.split()
        self.cards = list(cards)
        self.bid = int(bid)
        self._card_types = '23456789TJQKA'
        self._card_count = self._get_card_count()
        self.type = self._get_type()

    def _get_card_count(self):
        # return [(card_type, self.cards.count(card_type)) for card_type in self._card_types]
        return {card_type: self.cards.count(card_type) for card_type in self._card_types}
        # return Counter(hand)

    def _get_type(self):
        highest = sorted(self._card_count.items(), key=lambda c: c[1], reverse=True)
        if highest[0][1] == 5:
            return HandType.FIVE_OF_A_KIND
        if highest[0][1] == 4:
            return HandType.FOUR_OF_A_KIND
        if highest[0][1] == 3 and highest[1][1] == 2:
            return HandType.FULL_HOUSE
        if highest[0][1] == 3:
            return HandType.THREE_OF_A_KIND
        if highest[0][1] == 2 and highest[1][1] == 2:
            return HandType.TWO_PAIR
        if highest[0][1] == 2:
            return HandType.ONE_PAIR
        return HandType.HIGH_CARD

    def __lt__(self, other):
        if self.__class__ is not other.__class__:
            return NotImplemented
        if self.type != other.type:
            return self.type < other.type
        for index, card in enumerate(self.cards):
            if self._card_types.index(card) != self._card_types.index(other.cards[index]):
                return self._card_types.index(card) < self._card_types.index(other.cards[index])
        return False

    def __repr__(self):
        return '(' + ''.join(self.cards) + ', ' + str(self.bid) + ')'


class HandWithJoker(Hand):
    def __init__(self, raw_hand):
        super().__init__(raw_hand)
        self._card_types = 'J23456789TQKA'

    def _get_type(self):
        if 'J' not in self.cards:
            return super()._get_type()
        if self._card_count['J'] == 1:
            return self._get_type_one_joker()
        if self._card_count['J'] == 2:
            return self._get_type_two_joker()
        if self._card_count['J'] == 3:
            return self._get_type_three_joker()
        return HandType.FIVE_OF_A_KIND

    def _get_type_one_joker(self):
        card_count_without_joker = {card: count for card, count in self._card_count.items() if card != 'J'}
        highest = sorted(card_count_without_joker.items(), key=lambda c: c[1], reverse=True)
        if highest[0][1] == 4:
            return HandType.FIVE_OF_A_KIND
        if highest[0][1] == 3:
            return HandType.FOUR_OF_A_KIND
        if (highest[0][1] == 2 and highest[1][1] == 2) or (highest[0][1] == 3 and highest[1][1] == 1):
            return HandType.FULL_HOUSE
        if highest[0][1] == 2:
            return HandType.THREE_OF_A_KIND
        if highest[0][1] == 2 and highest[1][1] == 1:
            return HandType.TWO_PAIR
        return HandType.ONE_PAIR

    def _get_type_two_joker(self):
        card_count_without_joker = {card: count for card, count in self._card_count.items() if card != 'J'}
        highest = sorted(card_count_without_joker.items(), key=lambda c: c[1], reverse=True)
        if highest[0][1] == 3:
            return HandType.FIVE_OF_A_KIND
        if highest[0][1] == 2:
            return HandType.FOUR_OF_A_KIND
        if highest[0][1] == 2 and highest[1][1] == 1:
            return HandType.FULL_HOUSE
        return HandType.THREE_OF_A_KIND

    def _get_type_three_joker(self):
        card_count_without_joker = {card: count for card, count in self._card_count.items() if card != 'J'}
        highest = sorted(card_count_without_joker.items(), key=lambda c: c[1], reverse=True)
        if highest[0][1] == 2:
            return HandType.FIVE_OF_A_KIND
        return HandType.FOUR_OF_A_KIND


puzzle = Puzzle(year=2023, day=7)
data = puzzle.input_data.splitlines()

hands = []
hands_with_joker = []
for line in data:
    hands.append(Hand(line))
    hands_with_joker.append(HandWithJoker(line))

hands.sort()
hands_with_joker.sort()

puzzle.answer_a = sum([hand.bid * (index + 1) for index, hand in enumerate(hands)])
puzzle.answer_b = sum([hand.bid * (index + 1) for index, hand in enumerate(hands_with_joker)])
print(puzzle.answer_a, puzzle.answer_b)
