'''File: tune_info.py
- Parses and stores information about tune structure, especially changes

 - Notation:
   Cm7 Fm7 Dm7b5 G7 Cm7
   Ebm7 Ab7 DbM7
   Dm7b5 G7 Cm7
   - Encoding of symbols (Mapped according to the first letter - then stack
     intervals mod 12)
     CM   [0, 4, 7]
     CM7  [0, 7, 7, 11]
     Cm   [0, 3, 7]
     Cm7  [0, 3, 7, 10]
     Cm7b5 [0, 3, 6, 10]
     Co    [0, 3, 6, 9]
 - key.  Presumably audio analysis uses same numbers.
   (c, c-sharp, d, e-flat, e, f, f-sharp, g, a-flat, a, b-flat, b) 0 - 11
'''

from chord import ChordInfo
from chord import get_chord_info

class TuneInfo(object):
    def __init__(self, tune_info):
        # Read raw changes, etc from module
        self.tune_info = tune_info
        self.changes = None
        self.unique_chords = None
        self.parse_tune_info()

    @property
    def chorus_num_bars(self):
        return(len(self.changes))


    def parse_measure(self, measure):
        """Parse one measure of chords, and return a dict representation of that measure.
        - measure: list of chords for this measure.
          - Currently assume one chord per measure, SO RETURN A SINGLE CHORD OBJECT.
          - ZZZ return a measure, later.
        """
        # return ChordInfo(measure[0])
        return [ChordInfo(chord) for chord in measure]

    def parse_tune_info(self):
        """Parse tune_info, so we know something about our tune
        - tune_info is a dict.
          'changes': a list of lists, where each inner list represents the chords
          for one measure.
          - We assume exactly 1 chord per measure
          - We assume 4/4 time.

        """
        # Here, we cheat and represent a measure as a single chord.
        # changes is a list of chord symbols, change_infos is a list of
        # ChangeInfo objects.
        
        changes = []         # A list of chord symbols
        change_infos = []
        measure_list = self.tune_info['changes']
        for measure in measure_list:
            # We don't store this chord_info here - it stored
            # in chord.CHORD_TO_CHORD_INFO during parse_measure.
            # We always access them by chord symbols, using chord.get_chord_info()
            # chord_info = self.parse_measure(measure)
            measure_chord_info_list = self.parse_measure(measure)
            # Be sure we have clean changes with whitespace removed.
            # chord = chord_info.chord_info['chord']
            # List of chords for this measure
            chords = [chord_info.chord_info['chord'] 
                      for chord_info in measure_chord_info_list]
            # changes.append(chord)
            changes.append(chords)
        self.changes = changes
        # Unique chord symbols.  One thing we can do is match all unique chords
        # against current analyzer_tones, and choose the best alternative.
        # [The other thing we can do is match against the expected chord, and
        # just check whether it is above or below threshold].
        # all_chords = [measure[index] for index in xrange(len(measure))
        #               for measure in measure_list]
        all_chords = [measure[index] 
                      for measure in measure_list
                      for index in xrange(len(measure))]
        self.unique_chords = set(all_chords)
        # Don't store this.  Look up as necessary from chord.
        # self.available_chord_infos = [get_chord_info(chord) for chord in self.available_chords]

