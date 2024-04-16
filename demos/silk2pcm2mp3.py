import pysilk
from pydub import AudioSegment
import os

# pysilk: https://github.com/DCZYewen/Python-Silk-Module

# 假定是在 VSCode 上运行的， os.getcwd() 是项目根目录
INPUT_DIR = os.path.join('demos', 'silk2pcm2mp3_inp')
PCM_SAMPLE_WIDTH = 2
PCM_SAMPLE_RATE = 24000
PCM_CHANNELS = 1


def main():
    silk_paths = [os.path.join(INPUT_DIR, p) for p in os.listdir(INPUT_DIR) if p.endswith('.silk')]
    for silk_path in silk_paths:
        mp3_file_path = os.path.splitext(silk_path)[0] + '.mp3'
        pcm_data = bytes()
        with open(silk_path, 'rb') as silk:
            silk_data = silk.read()
            pcm_data = pysilk.decode(silk_data, sample_rate=PCM_SAMPLE_RATE)
        # 编码器是 pcm_s16le 故 sample_width=2 ；看 audio_segment.py 后猜测 frame_rate 就是 sample_rate ； channels 就是通道数
        audio = AudioSegment(pcm_data, sample_width=PCM_SAMPLE_WIDTH, frame_rate=PCM_SAMPLE_RATE, channels=PCM_CHANNELS)
        audio.export(mp3_file_path, format='mp3')


if __name__ == '__main__':
    main()
