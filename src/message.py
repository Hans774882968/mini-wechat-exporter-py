from utils import get_format_date_by_timestamp
from friend import Friend
from typing import List

MSGTYPE_IMAGE = 3
MSGTYPE_VOICE = 34
MSGTYPE_VIDEO = 43
MSGTYPE_MICROVIDEO = 62


class WechatMessage:
    def __init__(self, chat_record, user_id_hash: str) -> None:
        self.create_timestamp = chat_record[0]
        self.create_time = get_format_date_by_timestamp(self.create_timestamp)
        self.message = chat_record[1]
        self.des = chat_record[2]
        self.type = chat_record[3]
        # 记录 mes_local_id 的其中一个原因是，查找语音消息对应的 .aud 文件需要
        self.mes_local_id = chat_record[4]

        self.user_id_hash = user_id_hash

        self.is_audio_message = self.type == MSGTYPE_VOICE
        self.audio_path = self.get_audio_path_substr()

        self.is_img_message = self.type == MSGTYPE_IMAGE
        self.img_paths = self.get_img_paths_substr()

        self.is_video_message = self.type == MSGTYPE_VIDEO or self.type == MSGTYPE_MICROVIDEO
        self.video_path, self.video_thumb_path = self.get_video_relevant_paths_substr()

    def __str__(self) -> str:
        return f'WechatMessage(\n  create_time={self.create_time},\n  message={self.message},\n  mes_local_id={self.mes_local_id}\n)'

    def get_audio_path_substr(self):
        return f'Audio/{self.user_id_hash}/{self.mes_local_id}.aud' if self.is_audio_message else ''

    def get_img_paths_substr(self):
        if not self.is_img_message:
            return []
        common = f'Img/{self.user_id_hash}/{self.mes_local_id}'
        return [
            f'{common}.pic_thum',
            f'{common}.pic',
        ]

    def get_video_relevant_paths_substr(self):
        if not self.is_video_message:
            return ['', '']
        common = f'Video/{self.user_id_hash}/{self.mes_local_id}'
        return [
            f'{common}.mp4',
            f'{common}.video_thum',
        ]


class Session:
    def __init__(self, messages: List[WechatMessage], friend: Friend) -> None:
        self.messages = messages
        self.friend = friend
