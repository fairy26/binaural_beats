from AccelBrainBeat.brainbeat.binaural_beat import BinauralBeat


class MyBinauralBeat(BinauralBeat):
    def set_wave(self, frequencies: tuple):
        self.left_frequency, self.right_frequency = frequencies

    def set_roar_wave(self, base: float, diff: float):
        """うなりの周波数を差分でセットする
            δ波:     ~ 4 Hz (熟睡)
            θ波:  4 ~  8 Hz (創造・直感・瞑想・浅眠)
            α波:  8 ~ 12 Hz (リラックス)
            β波: 13 ~ 30 Hz (日常・活動・思考・警戒)
            γ波: 30 ~    Hz (情報処理・覚醒)

        Args:
            base (float): 基準の周波数[Hz]
            diff (float): 周波数の差分[Hz]
        """
        self.set_wave((base, base + diff))

    def play(self, play_time, sample_rate=44100, volume=0.01):
        frequencies = (self.left_frequency, self.right_frequency)
        self.play_beat(frequencies, play_time, sample_rate, volume)

    def save(self, output_file_name, play_time, sample_rate=44100, volume=0.01):
        frequencies = (self.left_frequency, self.right_frequency)
        self.save_beat(output_file_name, frequencies, play_time, sample_rate, volume)


def main():
    brain_beat = MyBinauralBeat()
    brain_beat.set_roar_wave(base=205, diff=6.3)
    brain_beat.play(play_time=5, volume=0.05)


if __name__ == "__main__":
    main()
