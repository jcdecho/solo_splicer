"""File: audio_bar.py
- Simple class to hold some bars and the audio_analysis that they came from, so
  that we can call get_pieces:
  audio.get_pieces(audio_analysis, bars_from_that_analysis)

- Maybe we can actually get up to the audio_analysis from a bar, but I didn't see
  how.

"""

import echonest.remix.audio as audio

class AudioBars(object):
    def __init__(self, audio_analysis, bars):
        self.audio_analysis = audio_analysis
        self.bars = bars
        

    def get_pieces(self):
        return(audio.getpieces(self.audio_analysis, self.bars))

