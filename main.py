import argparse
import struct
from pathlib import Path

import numpy as np
import soundfile as sf
from AccelBrainBeat.brainbeat.binaural_beat import BinauralBeat


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", default="cave_01.wav", type=str)
    parser.add_argument("-d", "--duration", default=60, type=int, help="play time[s]")

    return parser.parse_args()


class MyBinauralBeat(BinauralBeat):
    def __init__(self):
        super().__init__()

    def set_wave(self, frequencies: tuple):
        self.left_frequency, self.right_frequency = frequencies

    def set_roar_wave(self, base: float, diff: float):
        """うなりの周波数を差分でセットする

        Args:
            base (float): 基準の周波数[Hz]
            diff (float): 周波数の差分[Hz]
                -    ~  3 Hz: δ波（熟睡）
                -  4 ~  7 Hz: θ波（創造・直感・瞑想・浅眠）
                -  8 ~ 12 Hz: α波（リラックス）
                - 13 ~ 30 Hz: β波（日常・活動・思考・警戒）
                - 30 ~    Hz: γ波（情報処理・覚醒）
        """
        self.set_wave((base, base + diff))

    def set_ambient(self, sound: np.ndarray):
        self.ambient_volume = 1.0
        self.ambient_l = sound[:, 0]
        self.ambient_r = sound[:, 1]

    def play(self, play_time, sample_rate=44100, volume=0.01):
        frequencies = (self.left_frequency, self.right_frequency)
        self.play_beat(frequencies, play_time, sample_rate, volume)

    def save(self, output_file_name, play_time, sample_rate=44100, volume=0.01):
        frequencies = (self.left_frequency, self.right_frequency)
        self.save_beat(output_file_name, frequencies, play_time, sample_rate, volume)

    def write_stream(self, stream, beat_chunk_l, beat_chunk_r, beat_volume):
        assert len(beat_chunk_l) == len(beat_chunk_r), ValueError("Both of chunks (left, right) must be same length.")
        len_chunks = len(beat_chunk_l)

        ambient_l = np.tile(self.ambient_l, len_chunks // len(self.ambient_l) + 1)[:len_chunks]
        ambient_r = np.tile(self.ambient_r, len_chunks // len(self.ambient_r) + 1)[:len_chunks]

        chunk_l = ambient_l * self.ambient_volume + beat_chunk_l * beat_volume
        chunk_r = ambient_r * self.ambient_volume + beat_chunk_r * beat_volume

        for left, right in zip(chunk_l, chunk_r):
            data = struct.pack("2f", left, right)
            stream.write(data)


def main(wavf: Path, duration: int):
    sound, framerate = sf.read(wavf)

    brain_beat = MyBinauralBeat()
    brain_beat.set_ambient(sound)
    brain_beat.set_roar_wave(base=205, diff=6.3)
    try:
        print("▶ playing", end="\r")
        brain_beat.play(play_time=duration, volume=0.05)
    except KeyboardInterrupt:
        print("⏸ stopped")


if __name__ == "__main__":
    args = get_args()
    wavf = Path(".").joinpath(f"assets/{args.file}")
    if not wavf.exists():
        raise ValueError(f"'{wavf.name}' does not exist.")

    main(wavf, args.duration)
