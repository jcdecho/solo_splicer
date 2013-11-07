"""File: chord.py
- Chord object

- chord  A short chord symbol string, such as Dm7b5
- ChordInfo: An object representing that chord, including all intervals,
  note ints (raw, and wrapped to 0-11), etc.

NOTE: ChordInfo objects behave like singletons - I guess they really are
singletons.  If you construct a ChordInfo with a short symbol we've already
seen, you'll get the object we constructed when we first saw it.  Chords
are immutable.

Note information is in here too.  Didn't see the point of creating a separate
note.py at this point.

"""

import re
from string import strip


class ChordParseException(Exception):
    pass


NOTE_C = 0
NOTE_C_SHARP = 1
NOTE_D_FLAT = 1
NOTE_D = 2
NOTE_E_FLAT = 3
NOTE_D_SHARP = 3
NOTE_E = 4
NOTE_F = 5
NOTE_F_SHARP = 6
NOTE_G_FLAT = 6
NOTE_G = 7
NOTE_G_SHARP = 8
NOTE_A_FLAT = 8
NOTE_A = 9
NOTE_A_SHARP = 10
NOTE_B_FLAT = 10
NOTE_B = 11

NOTES = range(12)

NOTE_TO_INT = { 'C': NOTE_C,
                'Db': NOTE_C_SHARP,
                'D': NOTE_D,
                'Eb': NOTE_E_FLAT,
                'E': NOTE_E,
                'F': NOTE_F,
                'F#': NOTE_F_SHARP,
                'G': NOTE_G,
                'Ab': NOTE_A_FLAT,
                'A': NOTE_A,
                'Bb': NOTE_B_FLAT,
                'B': NOTE_B,
                }
INT_TO_NOTE = dict([(NOTE_TO_INT[note], note) for note in NOTE_TO_INT.keys()])
print "INT_TO_NOTE: %s" % INT_TO_NOTE

def note_to_int(note):
    return(NOTE_TO_INT[note])

def note_int_to_note(note_int):
    return(INT_TO_NOTE(note_int))

# Map already seen chords to their full representation.
CHORD_TO_CHORD_INFO = {}

def remember_chord(chord, chord_info):
    if not chord in CHORD_TO_CHORD_INFO:
        CHORD_TO_CHORD_INFO[chord] = chord_info
        

def get_chord_info(chord):
    """If we have already parsed this chord, return a copy of the result.
    """
    chord = strip(chord)
    existing = CHORD_TO_CHORD_INFO.get(chord, None)
    return existing or ChordInfo(chord)

chord_regex = re.compile(r"""
   (?P<root>[a-gA-G](b)?)
   (?P<mode_char>[mM])?
   (?P<seventh>[7])?
   ((?P<alt_fifth>[b])5)?""",
 re.VERBOSE)

CHORD_TONE_CONST = 2
OTHER_TONE_CONST = 0.5

def mod_twelve(notes_raw):
    """Convert an array of raw notes to an array of note_ints.
    - ie each one mod 12.
    """
    return [note % 12 for note in notes_raw]


class ChordInfo(object):
    def __init__(self, chord):
        """Parse a chord symbol into a dict of 'root', 'mode', 'seventh', store in self.
        - root_letter: 'C', 'C-sharp', 'B-flat'
        - root_encoding: 0 (C), 1 (C#), 2 (D), 3 (E-flat), 4 (E), 5 (F), 6 (F-sharp)
        7 (G), 8 (G#), 9 (A), 10 (B-flat), 11 (B)
        - mode: 'major', 'minor', 'half-diminished', 'diminished'
        - third: 'major', 'minor'
        - fifth: 'normal', 'flat', 'sharp'
        - seventh: 'major', 'minor', 'diminished' (ie 6th)
        """
        self.chord = strip(chord)
        
        # Hope this does not get confusing.  Other modules use chord_info to
        # hold a ChordInfo object.  Then to get the dict results, you can
        # use chord_info.chord_info.
        self.chord_info = self.parse_chord(self.chord)

    @property
    def changes(self):
        return(self.chord_info.changes)

    @property
    def unique_chords(self):
        return(self.chord_info.unique_chords)

    @property
    def note_ints(self):
        return(self.chord_info['note_ints'])


    def parse_chord(self, chord):
        result = {}
        mode = None
        root = None
        root_offset = 0
        root_int = None

        third = None
        third_offset = None
        third_int_raw = None
        third_int = None

        fifth = None
        fifth_offset = None
        fifth_int_raw = None
        fifth_int = None

        seventh = None
        seventh_offset = None
        seventh_int_raw = None
        seventh_int = None
        alt_fifth = None

        match = chord_regex.match(chord)
        if match:
            chord = chord
            root = match.group('root')
            root_int = note_to_int(root)
            mode_char = match.group('mode_char')
            # Some values may be changed later in the parsing sequence.
            result['root_offset'] = 0
            # Major or Dominant.
            if mode_char == 'M':
                mode = 'major'
                third_offset = 4
                third = 'major'
                fifth_offset = 7
                fifth = 'normal'
            # Dominant
            elif mode_char == None:
                mode = 'dominant'
                third_offset = 4
                third = 'major'
                fifth_offset = 7
                fifth = 'normal'
            elif mode_char == 'm':
                mode = 'minor'
                third_offset = 3
                third = 'minor'
                fifth_offset = 7
                fifth = 'normal'
            elif mode_char == 'o':
                mode = 'diminished'
                third_offset = 3
                third = 'minor'
                fifth_offset = 6
                fifth = 'flat'
            else:
                raise ChordParseException(
                    "Invalid mode_char - expected 'M', 'm' or 'o' ")
            
            # Is the '7' present?
            seventh = match.group('seventh')
            if seventh == '7':
                if mode == 'major':
                    seventh = 'major'
                    seventh_offset = 11
                elif mode == 'dominant':
                    seventh = 'minor'
                    seventh_offset = 10
                elif mode == 'minor':
                    seventh = 'minor'
                    seventh_offset = 10
                elif mode == 'diminished':
                    seventh = 'diminished'
                    seventh_offset = 9
                else:
                    raise ChordParseException("Invalid mode - expected 'major', 'minor' or 'diminished' ")

            # Is b5 present (we don't support #5 yet)
            alt_fifth = match.group('alt_fifth')
            if alt_fifth == 'b':
                # Flat 5
                mode = 'diminished'
                fifth = 'flat'
                fifth_offset = 6
            elif alt_fifth == None:
                pass
            else:
                raise ChordParseException("Invalid alt_fifth - expected 'b' (flat) or None, got: %s" % alt_fifth)

            note_base_offsets = [root_offset, third_offset, fifth_offset]
            if seventh_offset:
                note_base_offsets.append(seventh_offset)

            # Preserve intervals, so can identify chord - go beyond 0-11.
            third_int_raw = root_int + third_offset
            fifth_int_raw = root_int + fifth_offset
            if seventh_offset != None:
                seventh_int_raw = root_int + seventh_offset

            OUT = """
            third_int = third_int_raw % 12
            fifth_int = fifth_int_raw % 12
            if seventh_int_raw != None:
                seventh_int = seventh_int_raw % 12
"""
            # Order is important for reconstructing chord from root_int and note_ints.
            note_ints_raw = [root_int, third_int_raw, fifth_int_raw]
            if seventh_int_raw != None:
                note_ints_raw.append(seventh_int_raw)

            note_ints = mod_twelve(note_ints_raw)
            OUT = """
            note_ints = [root_int, third_int, fifth_int]
            if seventh_int != None:
                note_ints.append(seventh_int)
"""
            anti_note_offsets = []
            if (third in ['major', 'minor'] and 
                mode != 'dominant' and
                fifth != 'flat'
                ):
                # b9 not good for major or minor seven.  OK for m7b5, Dominant
                anti_note_offsets.append(1)
            if third == 'major' and mode != 'dominant':
                # If major chord, minor third is anti_tone, except for dominant
                anti_note_offsets.append(3)
            # No major 3rd on a minor chord.
            if third == 'minor':
                anti_note_offsets.append(4)
            # If flat 7, major 7 is anti_tone
            if seventh == 'minor':
                anti_note_offsets.append(11)
            # If major 7, flat 7 is anti_tone.
            if seventh == 'major' or (mode == 'major' and seventh == None):
                anti_note_offsets.append(10)

            anti_note_ints_raw = [anti_offset + root_int for anti_offset in anti_note_offsets]
            anti_note_ints = mod_twelve(anti_note_ints_raw)

            result['chord'] = chord
            result['mode'] = mode
            result['root'] = root
            result['root_int'] = root_int
            result['third'] = third
            result['third_offset'] = third_offset
            result['third_int_raw'] = third_int_raw
            # result['third_int'] = third_int
            result['fifth'] = fifth
            result['fifth_offset'] = fifth_offset
            result['fifth_int_raw'] = fifth_int_raw
            # result['fifth_int'] = fifth_int
            result['seventh'] = seventh
            result['seventh_offset'] = seventh_offset
            result['seventh_int_raw'] = seventh_int_raw
            # result['seventh_int'] = seventh_int

            # 0-based, regardless of which chord.  Does not wrap, because we only go up to 7th.
            result['note_base_offsets'] = tuple(note_base_offsets)
            # Shifted from note_base_offsets based on Root value.  Can go above 11.
            result['note_ints_raw'] = tuple(note_ints_raw)
            # Wrapped version of the above - 0-11.
            result['note_ints'] = tuple(note_ints)
            
            result['anti_note_offsets'] = tuple(anti_note_offsets)
            result['anti_note_ints_raw'] = tuple(anti_note_ints_raw)
            result['anti_note_ints'] = tuple(anti_note_ints)
        else:
            raise ParseChordException("Failed to parse chord: %s" % chord)

        # Remember it
        remember_chord(chord, self)
        return result

    def indexes_of_top_two(self, tone_vector):
        """Return a list with highest, then 2nd highest tone_vector values.
        - todo: indexes_of_top_n(self, tone_vector, n)
        """
        indexes = []
        tone_vector_copy = tone_vector[:]
        # Get largest
        max_index = tone_vector_copy.index(max(tone_vector_copy))
        indexes.append(max_index)
        tone_vector_copy.pop(max_index)
        # Get 2nd largest
        next_largest_index = tone_vector_copy.index(max(tone_vector_copy))
        # Remember we popped one value, so account for that
        if next_largest_index >= max_index:
            # Use position before pop
            next_largest_index += 1
        indexes.append(next_largest_index)
        return(indexes)


    def indexes_of_max_n(self, tone_vector, count):
        """Return the ordered list of indexes of the strongest vector tones.
        """
        assert(len(tone_vector) == 12)
        assert(count < 12)
        indexes = []
        tone_vector_copy = tone_vector[:]
        for _ in xrange(count):
            # Get max
            max_index = tone_vector_copy.index(max(tone_vector_copy))
            indexes.append(max_index)
            # Don't want to pick this one again, but leave it there so offsets stay the same.
            tone_vector_copy[max_index] = -1000
        return indexes
        
    def indexes_of_min_n(self, tone_vector, count):
        """Return the ordered list of indexes of the strongest vector tones.
        """
        assert(len(tone_vector) == 12)
        assert(count < 12)
        indexes = []
        tone_vector_copy = tone_vector[:]
        # When we've used one, we'll set it to 1000, to never be picked again.
        assert max(tone_vector_copy) < 1000
        tone_vector_copy = tone_vector[:]
        for _ in xrange(count):
            # Get min
            min_index = tone_vector_copy.index(min(tone_vector_copy))
            indexes.append(min_index)
            tone_vector_copy[min_index] = 1000
        return indexes
        

    def index_of_highest(self, tone_vector):
        max_value = max(tone_vector)
        # assume that value only appears once
        return tone_vector.index(max_value)
        
    def index_is_in_chord(self, index):
        # This note (0-11) is a chord tone
        return index in self.note_ints

    def index_is_in(self, index, index_set):
        return index in index_set

    def highest_is_in_chord(self, tone_vector):
        highest_index = self.index_of_highest(tone_vector)
        return self.index_is_in_chord(highest_index)

    #################################
    # Matching of beats and bars
    #################################

    # Version 1
    # def match_analysis_tone_vector(self, analysis_tone_vector):
    def match_analysis_tone_vector(self, analysis_bar):
        """Score a closeness match between a given chord, and an analysis tone vector
        - If a chord tone is strong in the tone vector, + score
        - If a non-chord tone is strong in tone vector, - score
        """
        analysis_tone_vector = analysis_bar.mean_pitches()
        # Notes of the chord
        chord_set = set(self.chord_info['note_ints'])
        # Notes not in the chord
        other_set = set(range(12)) - chord_set
        tone_vector_average = sum(analysis_tone_vector) / len(analysis_tone_vector)
        score = 0.0
        for note_int in chord_set:
            if analysis_tone_vector[note_int] > tone_vector_average:
                score += ((analysis_tone_vector[note_int] - tone_vector_average) * 
                          CHORD_TONE_CONST)
            if analysis_tone_vector[note_int] < tone_vector_average:
                score -= ((tone_vector_average - analysis_tone_vector[note_int]) *
                          CHORD_TONE_CONST)

        # Demerits if non-chord-tones are strong.
        for note_int in other_set:
            if analysis_tone_vector[note_int] > tone_vector_average:
                score -= ((analysis_tone_vector[note_int] - tone_vector_average) * 
                          OTHER_TONE_CONST)

        # Normalize to number of notes in chord
        score /= len(chord_set)
        return(score)


    # Version 2
    def match_analysis_bar(self, analysis_bar):
        """Match - v2
        - Try using individual beats as well as measure
        - Use match analysis tone vector(), below to get one score
        - For measure, Is highest value in the tone_vector in our chord?
        - For each beat, it highest value from the tone vector in our chord?
          - add 1 for each time it is
        """
        bar_tone_vector = analysis_bar.mean_pitches()
        # Calculate a score based on how many of the highest pitches are chord tones
        # - average for measure
        # - each beat
        peak_tone_score = 0
        if self.highest_is_in_chord(bar_tone_vector):
            peak_tone_score += 1
        beats = analysis_bar.children()
        for beat in beats:
            if self.highest_is_in_chord(beat.mean_pitches()):
                peak_tone_score += 1
        return peak_tone_score

    # Version 3
    def match_beats_OLD(self, beats):
        """Score by the beat.  Score 2 if strongest pitch is in chord, 1 if 2nd strongest is in chord
        """
        score = 0
        for beat in beats:
            top_indexes = self.indexes_of_top_two(beat.mean_pitches())
            if self.index_is_in_chord(top_indexes[0]):
                score += 2
            if self.index_is_in_chord(top_indexes[1]):
                score += 1
        return score

    # Version 4
    def match_beats(self, beats):
        score = 0
        for beat in beats:
            tone_vector = beat.mean_pitches()
            score += self.match_tone_vector(tone_vector)
        return score


    def match_bar(self, bar):
        tone_vector = bar.mean_pitches()
        score = self.match_tone_vector(tone_vector)
        return(score)

    #################################
    # End matching of beats and bars
    #################################


    ###################################
    # Matching of chord to tone_vector
    # - NOT re specific beats or bars.
    ###################################


    # Version 4
    def match_tone_vector(self, tone_vector):
        """Combine all sub-scores into one final score for the tone_vector.
        """
        assert(len(self.note_ints) in [3, 4])
        OUT = """
        return (self.match_tone_vector_max_vector_tones(tone_vector, len(self.note_ints)) +
                self.match_tone_vector_min_vector_tones(tone_vector, 4) +
                self.match_tone_vector_delta_average(tone_vector))
"""
        # count = len(self.chord_info['note_ints'])
        count = 2
        total_score = 0
        score, raw_score = self.match_tone_vector_min_max_vector_tones_2(
            tone_vector=tone_vector, indexes=self.chord_info['note_ints'],
            min_max='max', in_is_good=True, count=2)
        total_score += score

        score, raw_score = self.match_tone_vector_min_max_vector_tones_2(
            tone_vector=tone_vector, indexes=self.chord_info['note_ints'],
            min_max='min', in_is_good=False, count=2)
        total_score += score

            # Anti-notes

        # count = len(self.chord_info['note_ints'])
        count = 2
        score, raw_score = self.match_tone_vector_min_max_vector_tones_2(
            tone_vector=tone_vector, indexes=self.chord_info['note_ints'],
            min_max='max', in_is_good=False, count=len(self.chord_info['anti_note_ints']))
        total_score += score

        score, raw_score = self.match_tone_vector_min_max_vector_tones_2(
            tone_vector=tone_vector, indexes=self.chord_info['note_ints'],
            min_max='max', in_is_good=True, count=len(self.chord_info['anti_note_ints']))
        total_score += score

            # multiply this?
        score, raw_score = self.match_tone_vector_delta_average(tone_vector)
        total_score += 2 * score
        return total_score



    # Match based on the max/min tone_vector tones.
    # - Good if MAX are IN chord, or MIN are NOT in chord.
    def match_tone_vector_max_vector_tones_OLD(self, tone_vector, count):
        """Identify the n max vector tones, and score plus for each one that matches this chord.
        - tone_vector: audio mean_pitches() at some level - beat or measure
        - count: number of max vector tones to examine
        - max vector tone is given most weight.
          - successive tones, less weight
        - return:
          - 0-1
            - also return unscaled score, for easier testing.
          - If they are all chord tones, should return 1
        """
        score = 0
        # Indexes of strongest tones - sorted descending.
        num_tried = 0
        cur_increment = 1
        raw_score = 0.0
        potential_score = 0.0
        max_indexes = self.indexes_of_max_n(tone_vector, count)
        print("max_indexes: %s" % max_indexes)
        for index in max_indexes:
            if self.index_is_in_chord(index):
                print "matched index: %s" % index
                raw_score += cur_increment
            potential_score += cur_increment
            # Next increment will be half as much
            cur_increment /= 2.0
        print ("raw_score: %s  potential_score: %s" % (raw_score, potential_score))
        
        score = raw_score / potential_score
        return (score, raw_score)


    def match_tone_vector_min_vector_tones_OLD(self, tone_vector, count):
        """Identify the n min vector tones, and relate them to this chord.
        - tone_vector: audio mean_pitches() at some level - beat or measure
        - count: number of min vector tones to examine
        - raw score is 0 - 1 + 0.5 + 0.25 + 0.125 ... (as many as 'count')
        - score is normalized to 0-1.
        """
        score = 0
        # Indexes of strongest tones - sorted descending.
        num_tried = 0
        cur_increment = 1
        raw_score = 0.0
        potential_score = 0.0
        min_indexes = self.indexes_of_min_n(tone_vector, count)
        print("min_indexes: %s" % min_indexes)
        for index in min_indexes:
            if not self.index_is_in_chord(index):
                print "did not match index: %s" % index
                raw_score += cur_increment
            potential_score += cur_increment
            # Next increment will be half as much
            cur_increment /= 2.0
        print ("raw_score: %s  potential_score: %s" % (raw_score, potential_score))

        score = raw_score / potential_score
        return (score, raw_score)




    # Match based on the max/min tone_vector tones.
    # - If in_is_good, Good if min/max are IN indexes, Bad if min/max are NOT in indexes
    # - If min_max == 'min', compare the smallest vector tones
    # - If min_max == 'max', compare the largest vector tones

    def match_tone_vector_min_max_vector_tones_2(self, tone_vector, indexes, min_max, in_is_good, count=None):
        """Identify the n max vector tones, and score plus for each one that matches this chord.
        - tone_vector: audio mean_pitches() at some level - beat or measure
        - count: number of max vector tones to examine
        - max vector tone is given most weight.
          - successive tones, less weight
        - return:
          - 0-1
            - also return unscaled score, for easier testing.
          - If they are all chord tones, should return 1
        """
        print "tone_vector: %s" % tone_vector
        if count == None:
            count = len(indexes)
        score = 0
        # Indexes of strongest tones - sorted descending.
        num_tried = 0
        cur_increment = 1
        raw_score = 0.0
        potential_score = 0.0
        if min_max == 'min':
            key_indexes = self.indexes_of_min_n(tone_vector, count)
        elif min_max == 'max':
            key_indexes = self.indexes_of_max_n(tone_vector, count)
        else:
            raise Exception("Bogus value for min_max: %s.  Expected 'min' or 'max' " %
                            min_max)
        print("key_indexes: %s" % key_indexes)
        for index in key_indexes:
            if self.index_is_in(index, indexes):
                print "matched index: %s" % index
                if in_is_good:
                    raw_score += cur_increment
            else:
                print "did not match index: %s" % index
                if not in_is_good:
                    raw_score += cur_increment
            potential_score += cur_increment
            # Next increment will be half as much
            cur_increment /= 2.0
        print ("raw_score: %s  potential_score: %s" % (raw_score, potential_score))
        
        if potential_score == 0:
            import pdb; pdb.set_trace()

        score = raw_score / potential_score
        return (score, raw_score)


    def delta_average_score(self, tone_vector_val, tone_vector_avg, in_chord):
        """How do we score an individual one?
        - could be delta * const
          - But how would we normalize?
        - could just be a constant for each one.
        """
        # return ((tone_vector_val - tone_vector_average) * 
        #        CHORD_TONE_CONST)
        if in_chord and (tone_vector_val > tone_vector_avg):
            return 1
        if (not in_chord) and (tone_vector_val < tone_vector_avg):
            return 1
        return 0
        

    # Match based on whether tone_vector tones are above or below the 
    #   average of the tone_vector.
    # - Each chord tone that is above average is good
    # - Each non-chord tone that is below average is good.
    def match_tone_vector_delta_average(self, tone_vector):
        """Compare each vector value with the average, score accordingly
        - Raw scores, per value:
          - If below average, and chord tone, 1                                                                    
          - If above average, and non-chord tone, 1                                                                
          - else 0                                                                                                 
        - Sum and divide by 12 for total score.                                                                    
        """

        # Notes of the chord
        chord_indexes = set(self.chord_info['note_ints'])
        # Notes not in the chord
        non_chord_indexes = set(range(12)) - chord_indexes

        chord_tone_values = [tone_vector[index] 
                             for index in chord_indexes]
        non_chord_tone_values = [tone_vector[index] 
                                 for index in non_chord_indexes]

        # ZZZ sum squares?
        tone_vector_avg = sum(tone_vector) / len(tone_vector)
        score = 0.0
        chord_scores = [self.delta_average_score(val, 
                                                 tone_vector_avg,
                                                 in_chord=True)
                        for val in chord_tone_values]
        non_chord_scores = [self.delta_average_score(val,
                                                     tone_vector_avg,
                                                     in_chord=False)
                            for val in non_chord_tone_values]

        potential_score = 12
        raw_score = sum(chord_scores) + sum(non_chord_scores)
        score = raw_score / potential_score
        return score, raw_score


