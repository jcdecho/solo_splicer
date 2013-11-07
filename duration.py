# encoding: utf=8

'''File: dur.py
Description: Information about durations of beats and bars.

'''

import re
from optparse import OptionParser
import random

import echonest.remix.audio as audio
from chord import ChordInfo
from chord import get_chord_info
from tune_info import TuneInfo
from audio_bars import AudioBars


class Bin(object):
    """A collection of beats with roughly the same duration"""
    def __init__(self, tolerance=0.2):
        self.tolerance = tolerance
        self.durations = []
        self.average_duration = None


    def duration_belongs_in_bin(self, duration):
        if (self.durations == []
            or
            (abs(duration - self.average_duration) < 
             (self.tolerance * self.average_duration))):
            return True
        else:
            return False

    def add_duration(self, duration):
        """Add this duration if it belongs here, and return True, else False
        """
        if self.duration_belongs_in_bin(duration):
            self.durations.append(duration)
            self.average_duration = sum(self.durations) / float(len(self.durations))
            return True
        else:
            return False


class Bins(object):
    """Group beat durations into bins.
    - Normally expect 2 bins - target duration, and 1/2 that value or so.
    """
    def __init__(self, items, tolerance=0.2):
        self.tolerance = tolerance
        self.items = items
        self.bins = []
        all_durations = [item.duration for item in self.items]
        for duration in all_durations:
            self.add_duration(duration)
        self.primary_bin = self.get_primary_bin()
        self.average_duration = self.get_average_duration()


    def add_duration(self, duration):
        """Add a duration to one of the bins - creating one if necessary.
        - First see if we can add this duration to an existing bin.
          - If so, add it
        - Else, create a new bin and add it there.
        """
        added = False
        for bin in self.bins:
            if bin.add_duration(duration):
                added = True
                break
        if not added:
            new_bin = Bin(tolerance=self.tolerance)
            new_bin.add_duration(duration)
            self.bins.append(new_bin)
        return

    def get_bins(self):
        return self.bins

    def get_primary_bin(self):
        """Return the bin that has the most durations in it."""
        max_num_durations = 0
        primary_bin = None
        for bin in self.bins:
            if len(bin.durations) > max_num_durations:
                max_num_durations = len(bin.durations)
                primary_bin = bin
        return primary_bin


    def get_average_duration(self):
        """Find the bin with the most durations, and return its average
        """
        return self.get_primary_bin().average_duration
                    
            

class DurationInfo(object):
    """Information about beat and bar durations.
    """
    def __init__(self, beats, bars, tolerance=0.2):
        self.beat_bins = Bins(items=beats, tolerance=tolerance)
        self.bar_bins = Bins(items=bars, tolerance=tolerance)
    
        self.primary_beat_bin = self.beat_bins.get_primary_bin()
        self.average_beat_duration = self.beat_bins.get_average_duration()
        self.primary_bar_bin = self.bar_bins.get_primary_bin()
        self.average_bar_duration = self.bar_bins.get_average_duration()

