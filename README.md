[TOC]

# WechatExporter源码解析，加极简python项目演示核心原理

## 引言

TODO

## 从iTunes备份中读取微信本地存储数据库文件

搜`Manifest.db`很容易定位到`WechatExporter\core\ITunesParser.cpp`的`bool ITunesDb::load(const std::string& domain, bool onlyFile)`

https://github1s.com/BlueMatthew/WechatExporter/blob/main/WechatExporter/core/ITunesParser.h

读取微信图片的SQL：

```sql
SELECT * FROM Files WHERE relativePath LIKE '%Img/315142b9d2ae5e8184da94f4c89902fe%';
```

## 读取用户备注、昵称和头像

`userName`是用户最初的微信号，而用户当前的微信号存储在`dbContactRemark`。读取用户当前微信号为`yina_not`的SQL：

```sql
SELECT certificationFlag, dbContactBrand, dbContactChatRoom, dbContactHeadImage, dbContactLocal, dbContactOpenIM, dbContactOther, dbContactProfile, dbContactRemark, dbContactSocial, encodeUserName, extFlag, imgStatus, openIMAppid, "type", userName, dbContactEncryptSecret, typeExt
FROM Friend
WHERE dbContactRemark like '%yina_not%';
```

参考`WechatExporter`相关代码：

```cpp
bool FriendsParser::parseRemark(const void *data, int length, Friend& f)
{
    RawMessage msg;
    if (!msg.merge(reinterpret_cast<const char *>(data), length))
    {
        return false;
    }
    
    std::string value;
    // Remark Name
    if (msg.parse("3", value))
    {
        f.setDisplayName(value);
    }
    if (f.isDisplayNameEmpty() && msg.parse("1", value))
    {
        f.setDisplayName(value);
    }
    
    /*
    if (msg.parse("6", value))
    {
    }
    */
    
    return true;
}

bool FriendsParser::parseAvatar(const void *data, int length, Friend& f)
{

    RawMessage msg;
    if (!msg.merge(reinterpret_cast<const char *>(data), length))
    {
        return false;
    }
    
    std::string value;
    if (msg.parse("2", value))
    {
        if (!Friend::isInvalidPortrait(value))
        {
            f.setPortrait(value);
        }
    }
    if (msg.parse("3", value))
    {
        if (!Friend::isInvalidPortrait(value))
        {
            f.setPortraitHD(value);
        }
    }

    return true;
}
```

可知`dbContactRemark`和`dbContactHeadImage`都是proto格式的数据。

提取dbeaver的BLOB类型数据：在数值查看器中选择保存至文件，然后用Notepad++的Hex-Editor插件打开，最后进行复制。但这里有一个问题，就是这个插件给到我的数据会自动把`0x00`转为`0x20`，原因未知。

写出代码：

```python
from google.protobuf.descriptor_pb2 import FileDescriptorProto
from google.protobuf.descriptor_pool import DescriptorPool
from google.protobuf.message_factory import GetMessageClass
from google.protobuf.unknown_fields import UnknownFieldSet


def get_fields_from_proto_data(data: bytes):
    # 模仿 WechatExporter\core\RawMessage.cpp bool RawMessage::merge(const char *data, int length)
    m_pool = DescriptorPool()
    file_name = 'empty_message.proto'
    file = FileDescriptorProto(name=file_name)
    message_type = file.message_type.add()
    MESSAGE_TYPE_NAME = 'EmptyMessage'
    message_type.name = MESSAGE_TYPE_NAME
    m_pool.Add(file)
    descriptor = m_pool.FindMessageTypeByName(MESSAGE_TYPE_NAME)
    message = GetMessageClass(descriptor)  # 已废弃的旧写法 m_factory = MessageFactory(m_pool); message = m_factory.GetPrototype(descriptor)

    m_message = message()  # 类似于 C++ 版 m_message = message->New();
    m_message.ParseFromString(data)
    ufs = UnknownFieldSet(m_message)
    return ufs
```

## silk → pcm → mp3

silk → pcm在python里有若干选项：

1. https://github.com/Coldison/silk2mp3
2. https://github.com/foyoux/pilk
3. https://github.com/synodriver/pysilk
4. https://github.com/DCZYewen/Python-Silk-Module

pilk用法：

```python
import pilk

pilk.decode(r'248.silk', '248.pcm')  # 生成248.pcm
```

`Python-Silk-Module`用法：

```python
PCM_SAMPLE_RATE = 24000


def silk2pcm2mp3(silk_data: bytes):
    pcm_data = pysilk.decode(silk_data, sample_rate=PCM_SAMPLE_RATE)
```

最终选择了`Python-Silk-Module`。

另外，调研的时候意外发现`https://github.com/foyoux/pilk/blob/main/src/silk/pilk_decode.c`和`WechatExporter\core\Utils_silk.cpp`的代码大部分都是别处抄来的。

cpp可以用`lame`来实现pcm → mp3，参考`WechatExporter\core\Utils_audio.cpp`：

```cpp
const int num_of_channels = 1;

lame_global_flags *gfp = NULL;
gfp = lame_init();
if (NULL == gfp)
{
    return false;
}

lame_set_in_samplerate(gfp, 24000); // 被输入编码器的原始数据的采样率为24000
lame_set_preset(gfp, 56);
lame_set_mode(gfp, MONO); // mp3编码输出的声道数也是1
// RG is enabled by default
lame_set_findReplayGain(gfp, 1);
// lame_set_quality(gfp, 7);
//Setting Channels
lame_set_num_channels(gfp, num_of_channels); // 原始数据单声道

// ...
lame_set_out_samplerate(gfp, 24000); // mp3编码输出的声音的采样率
```

而以开源社区繁荣而著称的`python`似乎没有很受欢迎的库来做pcm → mp3这件事。但注意到ffmpeg可以用以下命令实现（[https://blog.csdn.net/weixin_33890499/article/details/88708622](参考链接1)）：

```bash
ffmpeg -y -f s16be -ac 1 -ar 24000 -acodec pcm_s16le -i 248.pcm 248.mp3
```

所以我们只需要找到套壳ffmpeg的库。这里我选择了`pydub`。用法：

```python
PCM_SAMPLE_WIDTH = 2
PCM_SAMPLE_RATE = 24000
PCM_CHANNELS = 1
# 编码器是 pcm_s16le 故 sample_width=2 ；看 audio_segment.py 后猜测 frame_rate 就是 sample_rate ； channels 就是通道数
audio = AudioSegment(pcm_data, sample_width=PCM_SAMPLE_WIDTH, frame_rate=PCM_SAMPLE_RATE, channels=PCM_CHANNELS)
audio.export(mp3_file_path, format='mp3')
```

最后，因为`pcm`只是一个中介，所以我们不妨封装一个`silk2pcm2mp3`方法：

```python
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
```

https://blog.csdn.net/zhuxian2009/article/details/120363605

https://larsimmisch.github.io/pyalsaaudio/terminology.html

## 参考资料

1. ffmpeg处理pcm和mp3互转：https://blog.csdn.net/weixin_33890499/article/details/88708622
2. PCM 大端（S16BE）和小端（S16LE）分析，及转换：https://blog.csdn.net/zhuxian2009/article/details/120363605
3. https://larsimmisch.github.io/pyalsaaudio/terminology.html