# Solution for Advent of Code day 5
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


class Almanac:
    def __init__(self, data):
        self.seeds = [int(seed) for seed in data[0].split(':')[1].split()]
        self._set_translation_maps(data[1:])
        self._set_seed_ranges()
        self._seed_locations = {}

    def _set_translation_maps(self, data):
        self._translation_maps = {}
        self._translation_maps_order = []
        source = ''
        destination = ''
        for line in data:
            if 'map' in line:
                source, unused, destination = line.split()[0].split('-')
                self._translation_maps[(source, destination)] = []
                self._translation_maps_order.append((source, destination))
            elif line:
                dest_start, source_start, length = (int(num) for num in line.split())
                self._translation_maps[(source, destination)].append((range(source_start, source_start + length), dest_start))

    def _set_seed_ranges(self):
        self.seed_ranges = []
        for index in range(0, len(self.seeds), 2):
            self.seed_ranges.append(range(self.seeds[index], self.seeds[index] + self.seeds[index + 1]))

    def _offset_range(self, r, offset):
        return range(r.start + offset, r.stop + offset)

    def _is_overlapping(self, range1, range2):
        overlap_start = max(range1.start, range2.start)
        overlap_stop = min(range1.stop, range2.stop)
        if overlap_start <= overlap_stop:
            return range(overlap_start, overlap_stop)
        return False

    def _split_range(self, r, overlap):
        parts = []
        if r.start < overlap.start:
            parts.append(range(r.start, overlap.start - 1))
        if r.stop > overlap.stop:
            parts.append(range(overlap.stop + 1, r.stop))
        return parts

    def get_locations(self):
        return [self.get_location_for_seed(seed) for seed in self.seeds]

    def get_location_for_seed(self, seed):
        initial_seed = seed
        if seed in self._seed_locations:
            return self._seed_locations[seed]
        for translation_map in self._translation_maps_order:
            for translation_range in self._translation_maps[translation_map]:
                try:
                    index = translation_range[0].index(seed)
                    seed = translation_range[1] + index
                    break
                except ValueError:
                    pass
        self._seed_locations[initial_seed] = seed
        return seed

    def get_min_location_for_seed_ranges(self):
        ranges = self.seed_ranges.copy()
        for translation_map in self._translation_maps_order:
            offset_ranges = []
            for translation_range in self._translation_maps[translation_map]:
                for seed_range in ranges.copy():
                    overlap = self._is_overlapping(seed_range, translation_range[0])
                    if overlap:
                        ranges.remove(seed_range)
                        ranges += self._split_range(seed_range, overlap)
                        offset_ranges.append(self._offset_range(overlap, translation_range[1] - translation_range[0].start))
            ranges += offset_ranges
        return [location_range.start for location_range in ranges]

puzzle = Puzzle(year=2023, day=5)
data = puzzle.input_data.splitlines()
almanac = Almanac(data)

puzzle.answer_a = min(almanac.get_locations())
puzzle.answer_b = min(almanac.get_min_location_for_seed_ranges())
print(puzzle.answer_a, puzzle.answer_b)