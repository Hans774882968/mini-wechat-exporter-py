import os
import shutil
from typing import List
from message import WechatMessage, Session
from ctx import context
from silk2pcm2mp3 import silk2pcm2mp3
from const import EXPORT_DIR_MOCK_NAME
from utils import check_or_mkdir


def write_messages(session: Session):
    check_or_mkdir(EXPORT_DIR_MOCK_NAME)
    write_messages_txt(session)
    write_messages_files(session)


def write_messages_txt(session: Session):
    messages_txt_path = os.path.join(EXPORT_DIR_MOCK_NAME, f'{session.friend.display_name}.txt')
    with open(messages_txt_path, 'w', encoding='utf-8') as f:
        messages_str = '\n'.join([str(m) for m in session.messages])
        f.write(messages_str)


def write_messages_files(session: Session):
    output_files_dir = os.path.join(EXPORT_DIR_MOCK_NAME, f'{session.friend.display_name}_files')
    if not os.path.exists(output_files_dir):
        os.mkdir(output_files_dir)

    def write_img_messages_files(img_messages: List[WechatMessage]):
        for message in img_messages:
            for img_path in message.img_paths:
                img_query_results = context.iTunes_bak_finder.find_file_bak_infos_by_relative_path(img_path, 'suf')
                # 比如 iTunes 备份到一半说失败了（原因可能是磁盘空间不足），就会出现文件找不到的情况，这里我的选择是静默失败
                if not img_query_results:
                    continue
                file_bak_path, _ = img_query_results[0]
                thumb_suffix = '_thumb' if img_path.endswith('pic_thum') else ''
                shutil.copy(file_bak_path, os.path.join(output_files_dir, f'{message.mes_local_id}{thumb_suffix}.jpg'))

    def write_audio_messages_files(audio_messages: List[WechatMessage]):
        for message in audio_messages:
            audio_query_results = context.iTunes_bak_finder.find_file_bak_infos_by_relative_path(message.audio_path, 'suf')
            if not audio_query_results:
                continue
            file_bak_path, _ = audio_query_results[0]
            mp3_file_path = os.path.join(output_files_dir, f'{message.mes_local_id}.mp3')
            with open(file_bak_path, 'rb') as silk:
                silk_data = silk.read()
                silk2pcm2mp3(silk_data, mp3_file_path)

    def write_video_messages_files(video_messages: List[WechatMessage]):
        for message in video_messages:
            video_query_results = context.iTunes_bak_finder.find_file_bak_infos_by_relative_path(message.video_path, 'suf')
            if video_query_results:
                video_file_bak_path, _ = video_query_results[0]
                video_file_output_path = os.path.join(output_files_dir, f'{message.mes_local_id}.mp4')
                shutil.copy(video_file_bak_path, video_file_output_path)

            video_thumb_query_results = context.iTunes_bak_finder.find_file_bak_infos_by_relative_path(message.video_thumb_path, 'suf')
            if video_thumb_query_results:
                video_thumb_file_bak_path, _ = video_thumb_query_results[0]
                video_thumb_file_output_path = os.path.join(output_files_dir, f'{message.mes_local_id}_video_thumb.jpg')
                shutil.copy(video_thumb_file_bak_path, video_thumb_file_output_path)

    audio_messages = [message for message in session.messages if message.is_audio_message]
    img_messages = [message for message in session.messages if message.is_img_message]
    video_messages = [message for message in session.messages if message.is_video_message]
    write_img_messages_files(img_messages)
    write_audio_messages_files(audio_messages)
    write_video_messages_files(video_messages)
