#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
test jam app functions.

'''

__author__ = "James Dean (james@echonest.com)"
__date__   = "Thu Oct 10 16:00:00 2013"


import unittest2 as unittest

from jam import Jammer
from chord import ChordInfo
from chord import CHORD_TO_CHORD_INFO

class TestParseChord(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass

    def test_parse_chord_c_major(self):
        chord_info = ChordInfo("CM")
        expected = {
            'chord': 'CM',
            'mode': 'major',
            'root': 'C',
            'root_offset': 0,
            'root_int': 0,

            'third': 'major',
            'third_offset': 4,
            'third_int_raw': 4,
            # 'third_int': 4,

            'fifth': 'normal',
            'fifth_offset': 7,
            'fifth_int_raw': 7,
            # 'fifth_int': 7,

            'seventh': None,
            'seventh_offset': None,
            'seventh_int_raw': None,
            # 'seventh_int': None,
            # Order is important
            'note_base_offsets': (0, 4, 7, ),
            'note_ints_raw': (0, 4, 7, ),
            'note_ints': (0, 4, 7, ),

            'anti_note_offsets': (1, 3, 10),
            'anti_note_ints_raw': (1, 3, 10),
            'anti_note_ints': (1, 3, 10),
            }
        self.assertEqual(chord_info.chord_info, expected)


    def test_parse_chord_c_major_seven(self):
        chord_info = ChordInfo("CM7")
        expected = {
            'chord': 'CM7',
            'mode': 'major',
            'root': 'C',
            'root_offset': 0,
            'root_int': 0,

            'third': 'major',
            'third_offset': 4,
            'third_int_raw': 4,
            # 'third_int': 4,

            'fifth': 'normal',
            'fifth_offset': 7,
            'fifth_int_raw': 7,
            # 'fifth_int': 7,

            'seventh': 'major',
            'seventh_offset': 11,
            'seventh_int_raw': 11,
            # 'seventh_int': None,
            # Order is important
            'note_base_offsets': (0, 4, 7, 11),
            'note_ints_raw': (0, 4, 7, 11),
            'note_ints': (0, 4, 7, 11),

            'anti_note_offsets': (1, 3, 10),
            'anti_note_ints_raw': (1, 3, 10),
            'anti_note_ints': (1, 3, 10),
            }
        self.assertEqual(chord_info.chord_info, expected)


    def test_parse_chord_c_minor_seven(self):
        chord_info = ChordInfo("Cm7")
        expected = {
            'chord': 'Cm7',
            'mode': 'minor',
            'root': 'C',
            'root_offset': 0,
            'root_int': 0,

            'third': 'minor',
            'third_offset': 3,
            'third_int_raw': 3,
            # 'third_int': 3,

            'fifth': 'normal',
            'fifth_offset': 7,
            'fifth_int_raw': 7,
            # 'fifth_int': 7,

            'seventh': 'minor',
            'seventh_offset': 10,
            'seventh_int_raw': 10,
            # 'seventh_int': 10,
            # Order is important
            'note_base_offsets': (0, 3, 7, 10),
            'note_ints_raw': (0, 3, 7, 10),
            'note_ints': (0, 3, 7, 10),

            'anti_note_offsets': (1, 4, 11),
            'anti_note_ints_raw': (1, 4, 11),
            'anti_note_ints': (1, 4, 11),
            }
        self.assertEqual(chord_info.chord_info, expected)
        
    def test_parse_chord_d_minor_seven(self):
        chord_info = ChordInfo("Dm7")
        expected = {
            'chord': 'Dm7',
            'mode': 'minor',
            'root': 'D',
            'root_offset': 0,
            'root_int': 2,

            'third': 'minor',
            'third_offset': 3,
            'third_int_raw': 5,
            # 'third_int': 5,

            'fifth': 'normal',
            'fifth_offset': 7,
            'fifth_int_raw': 9,
            # 'fifth_int': 9,

            'seventh': 'minor',
            'seventh_offset': 10,
            'seventh_int_raw': 12,
            # 'seventh_int': 0,

            'note_base_offsets': (0, 3, 7, 10),
            'note_ints_raw': (2, 5, 9, 12, ),
            'note_ints': (2, 5, 9, 0, ),

            'anti_note_offsets': (1, 4, 11),
            'anti_note_ints_raw': (3, 6, 13),
            'anti_note_ints': (3, 6, 1),
            }
        self.assertEqual(chord_info.chord_info, expected)

        
    def test_parse_chord_e_flat_minor_seven(self):
        chord_info = ChordInfo("Ebm7")
        expected = {
            'chord': 'Ebm7',
            'mode': 'minor',
            'root': 'Eb',
            'root_offset': 0,
            'root_int': 3,

            'third': 'minor',
            'third_offset': 3,
            'third_int_raw': 6,
            # 'third_int': 5,

            'fifth': 'normal',
            'fifth_offset': 7,
            'fifth_int_raw': 10,
            # 'fifth_int': 9,

            'seventh': 'minor',
            'seventh_offset': 10,
            'seventh_int_raw': 13,
            # 'seventh_int': 0,

            'note_base_offsets': (0, 3, 7, 10),
            'note_ints_raw': (3, 6, 10, 13, ),
            'note_ints': (3, 6, 10, 1, ),

            'anti_note_offsets': (1, 4, 11),
            'anti_note_ints_raw': (4, 7, 14),
            'anti_note_ints': (4, 7, 2),
            }
        self.assertEqual(chord_info.chord_info, expected)

        
    def test_parse_chord_e_minor_seven_flat_five(self):
        chord_info = ChordInfo("Em7b5")
        expected = {
            'chord': 'Em7b5',
            'mode': 'diminished',

            'root': 'E',
            'root_offset': 0,
            'root_int': 4,

            'third': 'minor',
            'third_offset': 3,
            'third_int_raw': 7,
            # 'third_int': 7,

            'fifth': 'flat',
            'fifth_offset': 6,
            'fifth_int_raw': 10,
            # 'fifth_int': 10,

            'seventh': 'minor',
            'seventh_offset': 10,
            'seventh_int_raw': 14,
            # 'seventh_int': 2,

            'note_base_offsets': (0, 3, 6, 10),
            'note_ints_raw': (4, 7, 10, 14, ),
            'note_ints': (4, 7, 10, 2, ),

            'anti_note_offsets': (4, 11),
            'anti_note_ints_raw': (8, 15),
            'anti_note_ints': (8, 3),
            }
        self.assertEqual(chord_info.chord_info, expected)


    def test_parse_chord_f_minor_seven(self):
        chord_info = ChordInfo("Fm7")
        expected = {
            'chord': 'Fm7',
            'mode': 'minor',
            'root': 'F',
            'root_offset': 0,
            'root_int': 5,

            'third': 'minor',
            'third_offset': 3,
            'third_int_raw': 8,
            # 'third_int': 8,

            'fifth': 'normal',
            'fifth_offset': 7,
            'fifth_int_raw': 12,
            # 'fifth_int': 0,

            'seventh': 'minor',
            'seventh_offset': 10,
            'seventh_int_raw': 15,
            # 'seventh_int': 3,
            # Order is important
            'note_base_offsets': (0, 3, 7, 10),
            'note_ints_raw': (5, 8, 12, 15),
            'note_ints': (5, 8, 0, 3),

            'anti_note_offsets': (1, 4, 11),
            'anti_note_ints_raw': (6, 9, 16),
            'anti_note_ints': (6, 9, 4),
            }
        self.assertEqual(chord_info.chord_info, expected)


    def test_parse_chord_g_seven(self):
        chord_info = ChordInfo("G7")
        expected = {
            'chord': 'G7',
            'mode': 'dominant',
            'root': 'G',
            'root_offset': 0,
            'root_int': 7,

            'third': 'major',
            'third_offset': 4,
            'third_int_raw': 11,
            # 'third_int': 11,

            'fifth': 'normal',
            'fifth_offset': 7,
            'fifth_int_raw': 14,
            # 'fifth_int': 2,

            'seventh': 'minor',
            'seventh_offset': 10,
            'seventh_int_raw': 17,
            # 'seventh_int': 5,
            # Order is important
            'note_base_offsets': (0, 4, 7, 10),
            'note_ints_raw': (7, 11, 14, 17),
            'note_ints': (7, 11, 2, 5),

            'anti_note_offsets': (11, ),
            'anti_note_ints_raw': (18, ),
            'anti_note_ints': (6, ),
            }
        self.assertEqual(chord_info.chord_info, expected)



class TestMatchSupport(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass


    def test_indexes_of_max_n(self):
        chord_info = ChordInfo("CM7")
        res = chord_info.indexes_of_max_n(
            [4, 0, 0, 0, 8, 9, 0, 2, 0, 0, 0, 1], count=4)
        print "res: %s" % res
        self.assertEqual(res, [5, 4, 0, 7])


    def test_indexes_of_min_n(self):
        chord_info = ChordInfo("CM7")
        res = chord_info.indexes_of_min_n(
            [0.2, 0.3, 0.9, 0.9, 0.8, 0.9, 0.1, 0.2, 0.3, 5, 5, 1], count=4)
        print "res: %s" % res
        self.assertEqual(res, [6, 0, 7, 1])


    def test_max_vector_tones_match(self):
        """For 4 chord tones
        - match returns (score, raw_score)
        - raw_score is any combination of 1, 0.5, 0.25, 0.125
        """
        chord_info = ChordInfo("CM7")
        print chord_info.chord_info
        assert( chord_info.chord_info['note_base_offsets'] == (0, 4, 7, 11))
        assert( chord_info.chord_info['note_ints_raw'] == (0, 4, 7, 11))
        assert( chord_info.chord_info['note_ints'] == (0, 4, 7, 11))

        score0, _ = chord_info.match_tone_vector_max_vector_tones_OLD(
            [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1], count=4)
        print "score0: %s" % score0
        self.assertEqual(score0, 1)

        score1, _ = chord_info.match_tone_vector_max_vector_tones_OLD(
            [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1], count=4)

        score2, _ = chord_info.match_tone_vector_max_vector_tones_OLD(
            [0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1], count=4)

        score3, _ = chord_info.match_tone_vector_max_vector_tones_OLD(
            [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0], count=4)

        self.assertGreater(score0, score1)
        self.assertGreater(score1, score2)
        self.assertGreater(score2, score3)

    def test_min_vector_tones_match(self):
        chord_info = ChordInfo("CM7")
        print chord_info.chord_info
        assert( chord_info.chord_info['note_base_offsets'] == (0, 4, 7, 11))
        assert( chord_info.chord_info['note_ints_raw'] == (0, 4, 7, 11))
        assert( chord_info.chord_info['note_ints'] == (0, 4, 7, 11))
        
        tone_vector = [0.9] * 12
        tone_vector[1] = 0.6  # good
        tone_vector[5] = 0.5  # good
        tone_vector[8] = 0.4  # good
        tone_vector[10] = 0.3 # good
        (score0, raw_score0) = chord_info.match_tone_vector_min_vector_tones_OLD(
            tone_vector, count=4)
        print "score0: %s  raw_score0: %s" % (score0, raw_score0)
        self.assertEqual(raw_score0, 1.875)
        # 1.875 is potential raw score if all 4 tones are not in chord
        self.assertEqual(score0, 1)

        tone_vector = [0.9] * 12
        tone_vector[0] = 0.6  # bad
        tone_vector[4] = 0.5  # bad
        tone_vector[8] = 0.4  # good
        tone_vector[10] = 0.3 # good
        (score0, raw_score0) = chord_info.match_tone_vector_min_vector_tones_OLD(
            tone_vector, count=4)
        print "score0: %s  raw_score0: %s" % (score0, raw_score0)
        self.assertEqual(raw_score0, 1.5)
        # 1.875 is potential raw score if all 4 tones are not in chord
        self.assertEqual(score0, 1.5 / 1.875)


    # NEW VERSION
    def test_min_max_vector_tones_max_good(self):
        # indexes are max indexes
        # it's good if they match chord tones.
        # - returns (score, raw_score)
        # - score is normalized to 0-1.
        # - raw_score is any combination of 1, 0.5, 0.25, 0.125

        chord_info = ChordInfo("CM7")
        print chord_info.chord_info
        assert( chord_info.chord_info['note_base_offsets'] == (0, 4, 7, 11))
        assert( chord_info.chord_info['note_ints_raw'] == (0, 4, 7, 11))
        assert( chord_info.chord_info['note_ints'] == (0, 4, 7, 11))

        score0, _ = chord_info.match_tone_vector_min_max_vector_tones_2(
            tone_vector = [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
            indexes = chord_info.note_ints,
            min_max = 'max',
            in_is_good = True,
            count=len(chord_info.note_ints))

        score1, _ = chord_info.match_tone_vector_min_max_vector_tones_2(
            tone_vector = [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
            indexes = chord_info.note_ints,
            min_max = 'max',
            in_is_good = True,
            count=len(chord_info.note_ints))

        score2, _ = chord_info.match_tone_vector_min_max_vector_tones_2(
            tone_vector = [0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1],
            indexes = chord_info.note_ints,
            min_max = 'max',
            in_is_good = True,
            count=len(chord_info.note_ints))

        score3, _ = chord_info.match_tone_vector_min_max_vector_tones_2(
            tone_vector = [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
            indexes = chord_info.note_ints,
            min_max = 'max',
            in_is_good = True,
            count=len(chord_info.note_ints))

        self.assertGreater(score0, score1)
        self.assertGreater(score1, score2)
        self.assertGreater(score2, score3)


    def test_min_max_vector_tones_min_bad(self):
        # indexes are min indexes
        # it's bad if they match chord tones.
        # - returns (score, raw_score)
        # - score is normalized to 0-1.
        # - raw_score is any combination of 1, 0.5, 0.25, 0.125
        chord_info = ChordInfo("CM7")
        print chord_info.chord_info
        assert( chord_info.chord_info['note_base_offsets'] == (0, 4, 7, 11))
        assert( chord_info.chord_info['note_ints_raw'] == (0, 4, 7, 11))
        assert( chord_info.chord_info['note_ints'] == (0, 4, 7, 11))
        
        tone_vector = [0.9] * 12
        tone_vector[1] = 0.6  # good
        tone_vector[5] = 0.5  # good
        tone_vector[8] = 0.4  # good
        tone_vector[10] = 0.3 # good

        score, raw_score = chord_info.match_tone_vector_min_max_vector_tones_2(
            tone_vector = tone_vector,
            indexes = chord_info.note_ints,
            min_max = 'min',
            in_is_good = False,
            count=len(chord_info.note_ints))
        print "score: %s  raw_score: %s" % (score, raw_score)
        self.assertEqual(raw_score, 1.875)
        # 1.875 is potential raw score if all 4 tones are not in chord
        self.assertEqual(score, 1)


        tone_vector = [0.9] * 12
        tone_vector[0] = 0.6  # bad
        tone_vector[4] = 0.5  # bad
        tone_vector[8] = 0.4  # good
        tone_vector[10] = 0.3 # good

        score, raw_score = chord_info.match_tone_vector_min_max_vector_tones_2(
            tone_vector = tone_vector,
            indexes = chord_info.note_ints,
            min_max = 'min',
            in_is_good = False,
            count=len(chord_info.note_ints))

        print "score: %s  raw_score: %s" % (score, raw_score)
        self.assertEqual(raw_score, 1.5)
        # 1.875 is potential raw score if all 4 tones are not in chord
        self.assertEqual(score, 1.5 / 1.875)


    # NEW VERSION
    def test_min_max_vector_tones_max_bad_ZZZ(self):
        # indexes are max indexes
        # it's bad if they match chord anti-tones.
        # - returns (score, raw_score)
        # - score is normalized to 0-1.
        # - raw_score is any combination of 1, 0.5, 0.25
        # Here, scores should be getting increasingly good.

        chord_info = ChordInfo("CM7")
        print chord_info.chord_info
        assert( chord_info.chord_info['anti_note_offsets'] == (1, 3, 10))
        assert( chord_info.chord_info['anti_note_ints_raw'] == (1, 3, 10))
        assert( chord_info.chord_info['anti_note_ints'] == (1, 3, 10))

        # score0, _ = chord_info.match_tone_vector_max_vector_tones(
        #     [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1], count=4)
        score0, _ = chord_info.match_tone_vector_min_max_vector_tones_2(
            tone_vector = [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
            indexes = chord_info.chord_info['anti_note_ints'],
            min_max = 'max',
            in_is_good = False,
            count=len(chord_info.chord_info['anti_note_ints']))

        # score1, _ = chord_info.match_tone_vector_max_vector_tones(
        #     [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1], count=4)
        score1, _ = chord_info.match_tone_vector_min_max_vector_tones_2(
            tone_vector = [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
            indexes = chord_info.chord_info['anti_note_ints'],
            min_max = 'max',
            in_is_good = False,
            count=len(chord_info.chord_info['anti_note_ints']))

        # score2, _ = chord_info.match_tone_vector_max_vector_tones(
        #     [0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1], count=4)
        score2, _ = chord_info.match_tone_vector_min_max_vector_tones_2(
            tone_vector = [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
            indexes = chord_info.chord_info['anti_note_ints'],
            min_max = 'max',
            in_is_good = False,
            count=len(chord_info.chord_info['anti_note_ints']))

        self.assertLess(score0, score1)
        self.assertLess(score1, score2)


    def test_min_max_vector_tones_min_good_ZZZ(self):
        # indexes are min indexes
        # it's good if they match chord anti-tones.
        # - returns (score, raw_score)
        # - score is normalized to 0-1.
        # - raw_score is any combination of 1, 0.5, 0.25, 0.125
        chord_info = ChordInfo("CM7")
        print chord_info.chord_info
        assert( chord_info.chord_info['anti_note_offsets'] == (1, 3, 10))
        assert( chord_info.chord_info['anti_note_ints_raw'] == (1, 3, 10))
        assert( chord_info.chord_info['anti_note_ints'] == (1, 3, 10))
        
        tone_vector = [0.9] * 12
        tone_vector[1] = 0.5  # good
        tone_vector[3] = 0.4  # good
        tone_vector[10] = 0.3  # good

        score, raw_score = chord_info.match_tone_vector_min_max_vector_tones_2(
            tone_vector = tone_vector,
            indexes = chord_info.chord_info['anti_note_ints'],
            min_max = 'min',
            in_is_good = True,
            count=len(chord_info.chord_info['anti_note_ints']))
        print "score: %s  raw_score: %s" % (score, raw_score)
        self.assertEqual(raw_score, 1.75)
        # 1.75 is potential raw score if all 3 tones are in the anti-tones
        self.assertEqual(score, 1)


        tone_vector = [0.9] * 12
        tone_vector[0] = 0.2  # bad
        tone_vector[3] = 0.3  # good
        tone_vector[9] = 0.6  # bad
        # (score0, raw_score0) = chord_info.match_tone_vector_min_vector_tones(
        #     tone_vector, count=4)

        score, raw_score = chord_info.match_tone_vector_min_max_vector_tones_2(
            tone_vector = tone_vector,
            indexes = chord_info.chord_info['anti_note_ints'],
            min_max = 'min',
            in_is_good = True,
            count=len(chord_info.chord_info['anti_note_ints']))

        print "score: %s  raw_score: %s" % (score, raw_score)
        self.assertEqual(raw_score, 0.5)
        # 1.875 is potential raw score if all 4 tones are not in chord
        self.assertEqual(score, 0.5 / 1.75)


    # COMPARE WITH AVERAGE
    def test_match_tone_vector_delta_average(self):
        """Compare each vector value with the average, score accordingly
        - Raw scores, per value:
          - If below average, and chord tone, 1
          - If above average, and non-chord tone, 1
          - else 0
        - Sum and divide by 12 for total score.
        """
        chord_info = ChordInfo("CM7")
        print chord_info.chord_info
        assert( chord_info.chord_info['note_base_offsets'] == (0, 4, 7, 11))
        assert( chord_info.chord_info['note_ints_raw'] == (0, 4, 7, 11))
        assert( chord_info.chord_info['note_ints'] == (0, 4, 7, 11))

        # Average is 0.5
        tone_vector = [0.5] * 12
        tone_vector[0] = 0.6  # good
        tone_vector[4] = 0.8  # good
        tone_vector[7] = 0.9  # good
        tone_vector[11] = 0.55 # good
        tone_vector[1] = 0.4
        tone_vector[5] = 0.2
        tone_vector[8] = 0.15
        tone_vector[10] = 0.45

        (score0, raw_score0) = chord_info.match_tone_vector_delta_average(
            tone_vector)

        print "score0: %s  raw_score0: %s" % (score0, raw_score0)
        self.assertEqual(raw_score0, 12)
        # 1.875 is potential raw score if all 4 tones are not in chord
        self.assertEqual(score0, 1)



class TestMatchChord(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass

    def test_match_chord_c_major(self):
        chord_info = ChordInfo("CM")
        expected = {
            'chord': 'CM',
            'mode': 'major',
            'root': 'C',
            'root_offset': 0,
            'root_int': 0,

            'third': 'major',
            'third_offset': 4,
            'third_int_raw': 4,
            # 'third_int': 4,

            'fifth': 'normal',
            'fifth_offset': 7,
            'fifth_int_raw': 7,
            # 'fifth_int': 7,

            'seventh': None,
            'seventh_offset': None,
            'seventh_int_raw': None,
            # 'seventh_int': None,
            # Order is important
            'note_base_offsets': (0, 4, 7, ),
            'note_ints_raw': (0, 4, 7, ),
            'note_ints': (0, 4, 7, ),

            'anti_note_offsets': (1, 3, 10),
            'anti_note_ints_raw': (1, 3, 10),
            'anti_note_ints': (1, 3, 10),
            }
        self.assertEqual(chord_info.chord_info, expected)

    def test_match_chord_c_major_seven(self):
        chord_info = ChordInfo("CM7")
        expected = {
            'chord': 'CM7',
            'mode': 'major',
            'root': 'C',
            'root_offset': 0,
            'root_int': 0,

            'third': 'major',
            'third_offset': 4,
            'third_int_raw': 4,
            # 'third_int': 4,

            'fifth': 'normal',
            'fifth_offset': 7,
            'fifth_int_raw': 7,
            # 'fifth_int': 7,

            'seventh': 'major',
            'seventh_offset': 11,
            'seventh_int_raw': 11,
            # 'seventh_int': None,
            # Order is important
            'note_base_offsets': (0, 4, 7, 11),
            'note_ints_raw': (0, 4, 7, 11),
            'note_ints': (0, 4, 7, 11),

            'anti_note_offsets': (1, 3, 10),
            'anti_note_ints_raw': (1, 3, 10),
            'anti_note_ints': (1, 3, 10),
            }
        self.assertEqual(chord_info.chord_info, expected)

    def test_match_chord_c_minor_seven(self):
        chord_info = ChordInfo("Cm7")
        expected = {
            'chord': 'Cm7',
            'mode': 'minor',
            'root': 'C',
            'root_offset': 0,
            'root_int': 0,

            'third': 'minor',
            'third_offset': 3,
            'third_int_raw': 3,
            # 'third_int': 3,

            'fifth': 'normal',
            'fifth_offset': 7,
            'fifth_int_raw': 7,
            # 'fifth_int': 7,

            'seventh': 'minor',
            'seventh_offset': 10,
            'seventh_int_raw': 10,
            # 'seventh_int': 10,
            # Order is important
            'note_base_offsets': (0, 3, 7, 10),
            'note_ints_raw': (0, 3, 7, 10),
            'note_ints': (0, 3, 7, 10),

            'anti_note_offsets': (1, 4, 11),
            'anti_note_ints_raw': (1, 4, 11),
            'anti_note_ints': (1, 4, 11),
            }
        self.assertEqual(chord_info.chord_info, expected)
        
    def test_match_chord_d_minor_seven(self):
        chord_info = ChordInfo("Dm7")
        expected = {
            'chord': 'Dm7',
            'mode': 'minor',
            'root': 'D',
            'root_offset': 0,
            'root_int': 2,

            'third': 'minor',
            'third_offset': 3,
            'third_int_raw': 5,
            # 'third_int': 5,

            'fifth': 'normal',
            'fifth_offset': 7,
            'fifth_int_raw': 9,
            # 'fifth_int': 9,

            'seventh': 'minor',
            'seventh_offset': 10,
            'seventh_int_raw': 12,
            # 'seventh_int': 0,

            'note_base_offsets': (0, 3, 7, 10),
            'note_ints_raw': (2, 5, 9, 12, ),
            'note_ints': (2, 5, 9, 0, ),

            'anti_note_offsets': (1, 4, 11),
            'anti_note_ints_raw': (3, 6, 13),
            'anti_note_ints': (3, 6, 1),
            }
        self.assertEqual(chord_info.chord_info, expected)

        
    def test_match_chord_e_minor_seven_flat_five(self):
        chord_info = ChordInfo("Em7b5")
        expected = {
            'chord': 'Em7b5',
            'mode': 'diminished',

            'root': 'E',
            'root_offset': 0,
            'root_int': 4,

            'third': 'minor',
            'third_offset': 3,
            'third_int_raw': 7,
            # 'third_int': 7,

            'fifth': 'flat',
            'fifth_offset': 6,
            'fifth_int_raw': 10,
            # 'fifth_int': 10,

            'seventh': 'minor',
            'seventh_offset': 10,
            'seventh_int_raw': 14,
            # 'seventh_int': 2,

            'note_base_offsets': (0, 3, 6, 10),
            'note_ints_raw': (4, 7, 10, 14, ),
            'note_ints': (4, 7, 10, 2, ),

            'anti_note_offsets': (4, 11),
            'anti_note_ints_raw': (8, 15),
            'anti_note_ints': (8, 3),
            }
        self.assertEqual(chord_info.chord_info, expected)


    def test_match_chord_f_minor_seven(self):
        chord_info = ChordInfo("Fm7")
        expected = {
            'chord': 'Fm7',
            'mode': 'minor',
            'root': 'F',
            'root_offset': 0,
            'root_int': 5,

            'third': 'minor',
            'third_offset': 3,
            'third_int_raw': 8,
            # 'third_int': 8,

            'fifth': 'normal',
            'fifth_offset': 7,
            'fifth_int_raw': 12,
            # 'fifth_int': 0,

            'seventh': 'minor',
            'seventh_offset': 10,
            'seventh_int_raw': 15,
            # 'seventh_int': 3,
            # Order is important
            'note_base_offsets': (0, 3, 7, 10),
            'note_ints_raw': (5, 8, 12, 15),
            'note_ints': (5, 8, 0, 3),

            'anti_note_offsets': (1, 4, 11),
            'anti_note_ints_raw': (6, 9, 16),
            'anti_note_ints': (6, 9, 4),
            }
        self.assertEqual(chord_info.chord_info, expected)


    def test_match_chord_g_seven(self):
        chord_info = ChordInfo("G7")
        expected = {
            'chord': 'G7',
            'mode': 'dominant',
            'root': 'G',
            'root_offset': 0,
            'root_int': 7,

            'third': 'major',
            'third_offset': 4,
            'third_int_raw': 11,
            # 'third_int': 11,

            'fifth': 'normal',
            'fifth_offset': 7,
            'fifth_int_raw': 14,
            # 'fifth_int': 2,

            'seventh': 'minor',
            'seventh_offset': 10,
            'seventh_int_raw': 17,
            # 'seventh_int': 5,
            # Order is important
            'note_base_offsets': (0, 4, 7, 10),
            'note_ints_raw': (7, 11, 14, 17),
            'note_ints': (7, 11, 2, 5),

            'anti_note_offsets': (11, ),
            'anti_note_ints_raw': (18, ),
            'anti_note_ints': (6, ),
            }
        self.assertEqual(chord_info.chord_info, expected)



class TestJammerFullTime(unittest.TestCase):
    """Tests where tempo is correct.
    - eg Bob Mintzer
    """
    def setUp(self):
        print "Enter setUp"
        self.jammer = Jammer(
            tune_info_module_name='blue_bossa_info', 
            input_filenames=['data/blue_bossa_pat_martino.mp3'],
            output_filename='blue_bossa_jam_pat_martino_test.wav')
        print "Created Jammer"

    def test_load_jammer(self):
        # List of chord symbols, basically from input tune_info
        self.assertEqual(len(self.jammer.tune_info.changes), 16)
        jam_one = self.jammer.jam_tunes[0]
        self.assertEqual(jam_one.tune_info.chorus_num_bars, 16)
        self.assertEqual(len(self.jammer.tune_info.unique_chords), 7)
        self.assertEqual(len(jam_one.tune_info.unique_chords), 7)
        self.assertEqual(jam_one.time_signature['value'], 4)


OUT = """
class TestJammerHalfTime(unittest.TestCase):
    # Tests for a song that parses in half-time, ie analyzer tempo is half what it should be
    def setUp(self):
        jammer = Jammer(
            tune_info_module_name='blue_bossa_info_half_time', 
            input_filenames=['data/blue_bossa_art_pepper.mp3'],
            output_filename='blue_bossa_jam.wav')
        

    def test_load_jammer(self):
        # List of chord symbols, basically from input tune_info
        self.assertEqual(len(jammer.tune_info.changes), 8)
        self.assertEqual(jam_one.tune_info.num_bars, 8)
        self.assertEqual(len(jammer.tune_info.unique_chords), 7)
        jam_one = jammer.jam_tunes[0]
        self.assertEqual(jam_one.time_signature, 4)
"""

if __name__ == '__main__':
    unittest.main()
