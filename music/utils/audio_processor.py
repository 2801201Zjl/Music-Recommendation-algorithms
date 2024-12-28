import torchaudio
import torch

def extract_features(songs):
    """
    提取音频特征，包括：
    - MEL频谱图
    - 音频波形
    - 节奏特征
    """
    features = []
    for song in songs:
        waveform, sample_rate = torchaudio.load(song.audio_file.path)
        mel_spectrogram = torchaudio.transforms.MelSpectrogram()(waveform)
        features.append({
            'song_id': song.id,
            'mel_spectrogram': mel_spectrogram,
            'waveform': waveform
        })
    return features 