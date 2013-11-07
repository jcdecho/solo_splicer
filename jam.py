#!/usr/bin/env python
# encoding: utf=8

'''jam.py
Description: Combine jazz tunes with simple chord structures (eg blues, blue bossa)
 Splice them together by 4-bar phrases.

- Finding the phrases:
  - Input the chord structure, and try to match that to audio by overlaying it by measures, and trying to coorelate with the tone-vector.

- Maybe use user 'hints' (harder with initial python version)

Notes
 - Maybe prefer choruses in the middle
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

import sys
import re
from optparse import OptionParser
import random

import echonest.remix.audio as audio
from chord import ChordInfo
from chord import get_chord_info
from tune_info import TuneInfo
from jam_tune import JamTune

CHUNK_NUM_BARS = 4
CHUNK_NUM_BARS = 8

class Jammer(object):
    def __init__(self, tune_info_module_name, input_filenames, output_filename, num_choruses=3):
        # TuneInfo describes the changes, time signature etc.
        # Currently we assume 4/4 time.
        tune_info_module = __import__(tune_info_module_name)
        self.tune_info = TuneInfo(tune_info_module.tune_info)
        self.input_filenames = input_filenames
        self.output_filename = output_filename
        # Load and analyze audio files.
        self.jam_tunes = [JamTune(self.tune_info, input_filename)
                          for input_filename in self.input_filenames]


    # ZZZ ZZZ ZZZ
    # audio.getpieces takes audio_analysis as first arg.  How can this work
    # when combining two tunes?
    def save_result(self):
        # output_bars = self.generate_jam(num_choruses=3)
        # List of AudioBars objects
        all_output_audio_bars = self.generate_jam(num_choruses=3)
        # ZZZ
        # final_audio = audio.getpieces(self.audio_analysis, output_bars)
        # import pdb; pdb.set_trace()
        # Start with first ones - should be the head in
        first_audio_bars = all_output_audio_bars.pop(0)

        # Create an audioData object for the first bars, but it will end up including
        # everything, so call it all_pieces.
        all_pieces = first_audio_bars.get_pieces()
        # Add the rest of the pieces

        # Temporarily just the head in
        for audio_bars in all_output_audio_bars:
            # Create an audioData objects for the next few bars
            next_piece = audio_bars.get_pieces()
            # Join that into the first audioData object.
            all_pieces.append(next_piece)
        # final_audio = all_pieces.getpieces()
        all_pieces.encode(self.output_filename)


    def generate_jam(self, num_choruses):
        """Generate and return a full song, of AudioBars"""
        head = []
        head_out = []
        solo_choruses = []
        head_audio_bars = self.jam_tunes[0].head_audio_bars
        solo_choruses = self.generate_n_solo_choruses(num_choruses)
        # Head out from the last tune
        head_out_audio_bars = self.jam_tunes[-1].head_out_audio_bars
        return [head_audio_bars] + solo_choruses + [head_out_audio_bars]

    def generate_n_solo_choruses(self, num_choruses):
        """Return a list of AudioBars objects representing n solo choruses
        - Each AudioBars is not a full chorus, but some number of bars.
        """
        choruses = []
        for _ in xrange(num_choruses):
            choruses.extend(self.generate_solo_chorus(CHUNK_NUM_BARS))
        return choruses

    def generate_solo_chorus(self, chunk_num_bars):
        """Generate a solo chorus by taking chunks from the available solo choruses
        """
        chorus = []
        chunk_real_num_bars = chunk_num_bars
        if self.tune_info.tune_info['half_time']:
            chunk_real_num_bars = chunk_real_num_bars / 2
            

        for bar_index in xrange(0, self.tune_info.chorus_num_bars, chunk_real_num_bars):
            jam_tune = self.get_random_jam_tune()
            audio_bars = jam_tune.get_nth_audio_bar_of_random_solo_chorus(bar_index, chunk_real_num_bars)
            chorus.append(audio_bars)
        return chorus
            
    def get_random_jam_tune(self):
        """Randomly return one of the jam tunes"""
        return self.jam_tunes[random.randrange(len(self.jam_tunes))]


def main(tune_info_module_name, input_filenames, output_filename, num_choruses=4):
    jammer = Jammer(tune_info_module_name, input_filenames, output_filename, num_choruses=num_choruses)
    jam_tunes = jammer.jam_tunes
    jam_tune = jam_tunes[0]
    jammer.save_result()

    # import pdb; pdb.set_trace()
    x = 3

if __name__ == '__main__':
    try :
        parser = OptionParser()
        parser.add_option("-o", "--output_filename", dest="output_filename",
                          default="jam_outfile.wav",
                          help="Write output to FILE", metavar="FILE")
        parser.add_option("-t", "--tune_info", dest="tune_info",
                          default="tune_info",
                          help="Read tune_info from MODULE", metavar="MODULE")
        parser.add_option("-c", "--choruses", dest="num_choruses",
                          default=4,
                          help="Number of solo choruses")
        (options, args) = parser.parse_args()
        output_filename = options.output_filename
        # ZZZ strip .py if present
        tune_info_module = options.tune_info
        num_choruses = options.num_choruses
        input_filenames = args
    except :
        parser.print_help()
        sys.exit(-1)
    if args == []:
        parser.print_help()
        sys.exit(-1)
    main(tune_info_module, input_filenames, output_filename, num_choruses=num_choruses)

