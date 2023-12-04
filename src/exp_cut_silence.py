import argparse
from pathlib import Path

from pydub import AudioSegment
from pydub.playback import play
from pydub.silence import split_on_silence

CWD = Path(".")


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", default="cave_01.wav")
    parser.add_argument("-e", "--experiment", default=False, action="store_true")

    return parser.parse_args()


def experiment(wavf: Path):
    sound = AudioSegment.from_wav(wavf)
    print(f"original: {sound.duration_seconds :.3f} [sec]")

    for silence_thresh in range(-40, -70, -5):
        chunks = split_on_silence(sound, min_silence_len=100, silence_thresh=silence_thresh, keep_silence=100)
        if not chunks:
            continue
        cutted_sound = sum(chunks)
        print(f"{silence_thresh = }; cutted {cutted_sound.duration_seconds :.3f} [sec]")
        print("\t▶ playing", end="\r")
        try:
            play(cutted_sound)
        except KeyboardInterrupt:
            print("\t⏸ skipped", end="\r")
            continue


def cut_silence(wavf: Path):
    sound = AudioSegment.from_wav(wavf)
    chunks = split_on_silence(sound, min_silence_len=100, silence_thresh=-55, keep_silence=100)
    sound = sum(chunks)

    dest_fname = wavf.stem + "_cut" + wavf.suffix
    dest = wavf.parent.joinpath(dest_fname)
    sound.export(dest, format="wav")


if __name__ == "__main__":
    args = get_args()

    asset_dir = CWD.parent.joinpath("assets")
    wavf = asset_dir.joinpath(args.file)

    if args.experiment:
        experiment(wavf)
        # >>> threash = -55 くらいがよさそう
    else:
        cut_silence(wavf)
