# Binaural Beats

## Usage

### 環境構築

1. 仮想環境

    ```bash
    pyenv local 3.10.6
    python3 -m venv .venv

    source .venv/bin/activate
    python3 -m pip install --upgrade pip
    ```

2. ライブラリのインストール

    ref: [Coding Music: A project on Python’s Accel Brain Beat | Medium](https://medium.com/strategio/coding-music-a-project-on-pythons-accel-brain-beat-f1aab34b6876)

    ```bash
    brew install portaudio
    pip install AccelBrainBeat pyaudio soundfile
    pip install pydub  # for exp_cut_silence.py
    ```

3. 使用

    ```bash
    source .venv/bin/activate

    # do something

    deactivate
    ```
