#!/usr/bin/env python
# encoding: utf=8

'''File: jam_tune.py
- Combine tune_info with audio_analysis to create an object.
  -  get the head_in, head_out (1 chorus)
  -  get all of the solo choruses (but exclude the first chorus, which is likely
     to be a repeat of the head.
  -  get one of those solo choruses - specific or random
  -  get a solo bar from one of the solo choruses
  -  get a solo bar from a random solo chorus

- Finding the phrases:
  - Input the chord structure, and try to match that to audio by overlaying it by measures, and trying to coorelate with the tone-vector.

- Maybe use user 'hints' (harder with initial python version)

Notes
 - Beware intro, outro
 - Beware fancy break bt head in and solos.
 - Beware of drums-only (or maybe use late in the tune as trade 4s)
 - Do sliding full-chorus match all the way through.  Eg 16-bar match for Blue Bossa.
 "Glue Bossa"
 - Only use a 12-bar section that is a good match for the chords.
 - Need to match the tempos.
 - Need to map a chord symbol (eg Cm7) to a list of ints corresponding to the
   indices of the tone vector.
 - Need a distance function between our expected tone vector and the current
   analysis tone vector.

Usage: 
    python jam.py chord_file song1_filename [song2_filename, ...]

Example:
    python reverse.py beats YouCanCallMeAl.mp3 AlMeCallCanYou.mp3

History:
 jcd 2013/10/10   File created - started with 'reverse.py'

'''

import re
from optparse import OptionParser
import random
import math

import echonest.remix.audio as audio
from chord import ChordInfo
from chord import get_chord_info
from tune_info import TuneInfo
from audio_bars import AudioBars
from duration import DurationInfo

class JamTune(object):
    def __init__(self, tune_info, input_filename):
        self.tune_info = tune_info
        self.input_filename = input_filename
        self.audio_analysis = audio.LocalAudioFile(self.input_filename)
        self.best_global_offset = None
        # Do all matching calculations, building result data structures
        self.match_info = None
        self.match_all_changes()
        self.duration_info = DurationInfo(self.beats, self.bars)
        self._average_loudness = self.calc_average_loudness()
        assert(self.time_signature['value'] == 4)
        print "JamTune Summary"
        print "input_filename: %s" % input_filename
        print " tempo: %d  time_signature: %d" % (self.tempo['value'],
                                                  self.time_signature['value'])
        print ' average_beat_duration: %s' % self.average_beat_duration
        print ' average_loudness: %s' % self.average_loudness
        print ' average_bar_duration: %s' % self.average_bar_duration
        print ' chorus_num_bars: %s' % self.tune_info.chorus_num_bars
        # import pdb; pdb.set_trace()
        x = 10

    # TEMPO, TIME SIGNATURE
    @property
    def tempo(self):
        return(self.audio_analysis.analysis.tempo)

    @property
    def time_signature(self):
        return(self.audio_analysis.analysis.time_signature)

    @property
    def primary_beat_bin(self):
        """Return a bin representing the most often occurring beat duration"""
        return self.duration_info.primary_beat_bin

    @property
    def average_beat_duration(self):
        return self.duration_info.average_beat_duration

    @property
    def average_loudness(self):
        return self._average_loudness

    @property
    def primary_bar_bin(self):
        """Return a bin representing the most often occurring bar duration"""
        return self.duration_info.primary_bar_bin

    @property
    def average_bar_duration(self):
        return self.duration_info.average_bar_duration

    def beat_in_primary_bin(self, beat):
        return self.primary_beat_bin.duration_belongs_in_bin(beat.duration)

    def bar_in_primary_bin(self, bar):
        """Basically, return True if this bar has the correct duration"""
        return self.primary_bar_bin.duration_belongs_in_bin(bar.duration)


    # CHORUSES
    @property
    def total_num_choruses(self):
        num_choruses = (len(self.bars)
                        - self.best_global_offset) / self.tune_info.chorus_num_bars

        return num_choruses


    @property
    def num_solo_choruses(self):
        num_choruses = self.total_num_choruses
        # Don't count head in (2x) for solo changes.
        num_choruses -= 2
        # Don't use head out (probably should use 2)
        num_choruses -= 1
        return num_choruses




    # BARS, AUDIO BARS

    @property
    def beats(self):
        return self.audio_analysis.analysis.beats

    @property
    def bars(self):
        return self.audio_analysis.analysis.bars

    @property
    def audio_bars(self):
        return AudioBars(self.audio_analysis, self.bars)


    @property
    def valid_bars(self):
        return self.bars[
            self.best_global_offset :
                self.best_global_offset + 
            self.total_num_choruses * self.tune_info.chorus_num_bars]
        
    @property
    def valid_audio_bars(self):
        return AudioBars(self.audio_analysis, self.valid_bars)

    @property
    def head_bars(self):
        """One chorus of the head.
        """
        return self.valid_bars[ :self.tune_info.chorus_num_bars]

    @property
    def head_audio_bars(self):
        return AudioBars(self.audio_analysis, self.head_bars)


    @property
    def head_out_bars(self):
        """One chorus of the head out.
        """
        return self.valid_bars[-self.tune_info.chorus_num_bars:]

    @property
    def head_out_audio_bars(self):
        return AudioBars(self.audio_analysis, self.head_out_bars)


    @property
    def solo_bars(self):
        """Return bars after 2 head choruses, and not including 1 head out chorus
        """
        head_offset = self.tune_info.chorus_num_bars * 2
        return self.valid_bars[head_offset :
                                   head_offset +
                               self.tune_info.chorus_num_bars * self.num_solo_choruses]

    @property
    def solo_audio_bars(self):
        return AudioBars(self.audio_analysis, self.solo_bars)
    

    def get_nth_chorus_bars(self, index):
        """Return one chorus of bars, using the nth solo chorus.
        """
        chorus_offset = self.tune_info.chorus_num_bars * index
        return self.solo_bars[chorus_offset : 
                              chorus_offset + self.tune_info.chorus_num_bars]

    def get_nth_chorus_audio_bars(self, index):
        bars = self.get_nth_chorus_bars(index)
        return AudioBars(self.audio_analysis, bars)


    def get_random_chorus_bars(self):
        rand_index = random.randrange(self.num_solo_choruses)
        return self.get_nth_chorus_bars(rand_index)

    def get_random_chorus_audio_bars(self):
        """Get a full chorus of bars, and return an AudioBars made from that"""
        bars = self.get_random_chorus_bars()
        return AudioBars(self.audio_analysis, bars)


    def get_nth_bar(self, bars, index, num_bars=1):
        """Usually a bar from a solo chorus"""
        return bars[index:index+num_bars]

    def get_nth_audio_bar(self, bars, index, num_bars=1):
        bars = self.get_nth_bar(bars, index, num_bars=1)
        return AudioBars(self.audio_analysis, bars)
        

    def get_nth_bar_of_random_solo_chorus(self, index, num_bars):
        """Return the nth bar[s] from a random solo chorus
        - Chunk size is the number of bars to return
        """
        return self.get_nth_bar(self.get_random_chorus_bars(), index, num_bars)

    def get_nth_audio_bar_of_random_solo_chorus(self, index, num_bars):
        bars = self.get_nth_bar_of_random_solo_chorus(index, num_bars)
        return AudioBars(self.audio_analysis, bars)



    # MATCHING
    def match_bar(self, match_bar_fn, match_beats_fn, measure_chord_infos, bar):
        score = 0
        if len(measure_chord_infos) == 2:
            score += match_beats_fn(measure_chord_infos[0], bar.children()[:2])
            score += match_beats_fn(measure_chord_infos[1], bar.children()[2:])
        else:
            bar_score = match_bar_fn(measure_chord_infos[0], bar)
            beat_score = match_beats_fn(measure_chord_infos[0], bar.children()[:4])
            # Measure is 4 beats, but then scale so overall weight is the same as for when no bar
            score = (beat_score + 4 * bar_score) / 2.0
        return score

    def match_chorus(self, start_bar):
        """Match changes from tune_info to analyzer_tones for full length of tune.
        - start_measure: 0-based index of measure to start match on
        - result is a chorus_match dict
          {'start_bar': <n>,
           'bars': <analyzer_bars>
           'match_results': [{'chord_info': ChordInfo object
                             'analyzer_tones': z,
                             'score': z }
                             ...]  (for full length of chorus
        """
        result = {'start_bar': start_bar, }
        print "start bar: %s" % start_bar
        # Now this is a list of measures, not a list of chords.
        changes = self.tune_info.changes
        chorus_bars = self.bars[start_bar:start_bar + len(changes)]
        # chord_infos = [get_chord_info(chord) for chord in changes]
        # measure_chord_infos is one or two chord_infos in a list, for one measure.
        measure_chord_infos = [[get_chord_info(chord) 
                                for chord in measure]
                               for measure in changes]

        # assert(len(chorus_bars) == len(chord_infos))
        assert(len(chorus_bars) == len(measure_chord_infos))
        # bars_infos = zip(chord_infos, chorus_bars)
        bar_infos = zip(measure_chord_infos, chorus_bars)

        # match_fn = ChordInfo.match_analysis_tone_vector
        # match_fn = ChordInfo.match_analysis_bar
        match_beats_fn = ChordInfo.match_beats
        match_bar_fn = ChordInfo.match_bar
        # ZZZ Do it twice for now...DEBUG

        # import pdb; pdb.set_trace()
        match_scores = [
            self.match_bar(match_bar_fn, match_beats_fn, measure_chord_info, bar)
            for measure_chord_info, bar in bar_infos]

        print 'match_scores: ',
        for match_score in match_scores:
            print '%0.4f' % match_score,
        print '  sum: %0.4f' % sum(match_scores)
        print 'measure lengths:',
        for bar in chorus_bars:
            print '%0.4f' % bar.duration,
        print '\n'
        OUT = """
        for chord_info, bar in bars_infos:
            print('chord_info: %s  bar duration: %0.4f  mean_pitches:' %
                  (chord_info.chord_info, bar.duration), )
            for pitch in bar.mean_pitches():
                print '%0.4f ' % pitch,
            # score = chord_info.match_analysis_tone_vector(bar.mean_pitches())
            score = match_fn(chord_info, bar)
            print('score: %0.4f' % score)
        print '\n\n'
"""
        return sum(match_scores)

                        
    def readable_chorus_match(self, chorus_match):
        """Extract readable stuff from objects, for saving in file, for study/debug.
        """
        return([{'start_bar': chord_match['start_bar'],
                 'bar_tones': ['ZZZ'],
                 'etc': 'z'} for chord_match in chorus_match])

    def match_all_changes(self):
        """Match changes with analyzer_tones for *every* start_measure offset
        - start_measure: 0-based index of measure to start match on
        """
        # Score a full chorus at every measure offset that allows a full chorus.
        num_cycles = (len(self.audio_analysis.analysis.bars) - 
                      len(self.tune_info.changes))

        chorus_scores = []
        chorus_len = len(self.tune_info.changes)
        for start_offset in xrange(num_cycles):
            chorus_score = self.match_chorus(start_offset)
            chorus_scores.append(chorus_score)

        print 'chorus_scores: %s' % chorus_scores
        # Which global_offset gives the best total score over all choruses
        global_offset_max = -1000
        best_global_offset = None
        for global_offset in xrange(chorus_len):
            offset_scores = [chorus_scores[offset] for offset in xrange(num_cycles)
                             if offset % chorus_len == global_offset]
            sum_offset_scores = sum(offset_scores)
            print 'global_offset: %s' % global_offset
            print 'sum_offset_scores: %0.4f\n' % sum_offset_scores
            if sum_offset_scores > global_offset_max:
                global_offset_max = sum_offset_scores
                best_global_offset = global_offset
        self.best_global_offset = best_global_offset


    def calc_average_loudness(self):
        count = len(self.audio_analysis.analysis.bars)
        total_loudness = 0
        for bar in self.audio_analysis.analysis.bars:
            total_loudness += bar.mean_loudness()
        avg_loudness = total_loudness / float(count)
        return avg_loudness
