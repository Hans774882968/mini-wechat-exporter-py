import pysilk
from pydub import AudioSegment

PCM_SAMPLE_WIDTH = 2
PCM_SAMPLE_RATE = 24000
PCM_CHANNELS = 1


def silk2pcm2mp3(silk_data: bytes, mp3_file_path: str):
    pcm_data = pysilk.decode(silk_data, sample_rate=PCM_SAMPLE_RATE)
    # 编码器是 pcm_s16le 故 sample_width=2 ；看 audio_segment.py 后猜测 frame_rate 就是 sample_rate ； channels 就是通道数
    audio = AudioSegment(pcm_data, sample_width=PCM_SAMPLE_WIDTH, frame_rate=PCM_SAMPLE_RATE, channels=PCM_CHANNELS)
    audio.export(mp3_file_path, format='mp3')
