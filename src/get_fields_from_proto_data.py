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


def main():
    # 直接打开文件，肉眼就能看到明文数据了，但正确地分割它们需要使用 protobuf 包
    db_contact_remark = b'\x0a\x06\xe9\x9d\x9e\xe9\x97\xa8\x12\x0a\x49\x6c\x79\x69\x6e\x61\x5f\x6e\x6f\x74\x1a\x0d\xe6\xa2\xa7\xe5\xb7\x9e\x2d\xe5\x90\xb4\xe9\x94\x8b\x22\x0c\x77\x75\x7a\x68\x6f\x75\x77\x75\x66\x65\x6e\x67\x2a\x04\x57\x5a\x57\x46\x32\x06\x66\x65\x69\x6d\x65\x6e\x3a\x00\x42\x00'
    db_contact_remark_ufs = get_fields_from_proto_data(db_contact_remark)
    for unknown_field in db_contact_remark_ufs:
        wire_type = unknown_field.wire_type
        field_number = unknown_field.field_number
        data = unknown_field.data
        print(wire_type, field_number, data)
        # 2 1 b'\xe9\x9d\x9e\xe9\x97\xa8'
        # 2 2 b'Ilyina_not'
        # 2 3 b'\xe6\xa2\xa7\xe5\xb7\x9e-\xe5\x90\xb4\xe9\x94\x8b'
        # 2 4 b'wuzhouwufeng'
        # 2 5 b'WZWF'
        # 2 6 b'feimen'
        # 2 7 b''
        # 2 8 b''
    print(str(db_contact_remark_ufs[2].data, encoding='utf-8'))
    print(str(db_contact_remark_ufs[0].data, encoding='utf-8'))

    db_contact_head_image = b'\x08\x03\x12\x93\x01\x68\x74\x74\x70\x73\x3a\x2f\x2f\x77\x78\x2e\x71\x6c\x6f\x67\x6f\x2e\x63\x6e\x2f\x6d\x6d\x68\x65\x61\x64\x2f\x76\x65\x72\x5f\x31\x2f\x68\x76\x71\x45\x67\x61\x39\x51\x70\x73\x6a\x49\x4d\x71\x61\x5a\x33\x46\x79\x36\x70\x70\x6d\x72\x36\x4b\x51\x47\x45\x31\x77\x54\x53\x4b\x63\x34\x6c\x79\x5a\x71\x6c\x55\x50\x4e\x4c\x71\x45\x7a\x35\x67\x35\x77\x35\x6d\x61\x35\x48\x4d\x53\x58\x35\x76\x6f\x6e\x70\x78\x78\x41\x4a\x6c\x73\x67\x76\x6b\x33\x57\x36\x68\x45\x69\x62\x51\x38\x6d\x57\x4f\x65\x73\x4c\x5a\x72\x76\x72\x6e\x39\x72\x6b\x4f\x73\x79\x69\x61\x32\x70\x41\x34\x69\x63\x37\x63\x2f\x31\x33\x32\x1a\x91\x01\x68\x74\x74\x70\x73\x3a\x2f\x2f\x77\x78\x2e\x71\x6c\x6f\x67\x6f\x2e\x63\x6e\x2f\x6d\x6d\x68\x65\x61\x64\x2f\x76\x65\x72\x5f\x31\x2f\x68\x76\x71\x45\x67\x61\x39\x51\x70\x73\x6a\x49\x4d\x71\x61\x5a\x33\x46\x79\x36\x70\x70\x6d\x72\x36\x4b\x51\x47\x45\x31\x77\x54\x53\x4b\x63\x34\x6c\x79\x5a\x71\x6c\x55\x50\x4e\x4c\x71\x45\x7a\x35\x67\x35\x77\x35\x6d\x61\x35\x48\x4d\x53\x58\x35\x76\x6f\x6e\x70\x78\x78\x41\x4a\x6c\x73\x67\x76\x6b\x33\x57\x36\x68\x45\x69\x62\x51\x38\x6d\x57\x4f\x65\x73\x4c\x5a\x72\x76\x72\x6e\x39\x72\x6b\x4f\x73\x79\x69\x61\x32\x70\x41\x34\x69\x63\x37\x63\x2f\x30\x22\x00'
    db_contact_head_image_ufs = get_fields_from_proto_data(db_contact_head_image)
    print(db_contact_head_image_ufs[0].data)  # 3
    small_avatar = str(db_contact_head_image_ufs[1].data, encoding='utf-8')
    print(small_avatar)  # https://wx.qlogo.cn/mmhead/ver_1/hvqEga9QpsjIMqaZ3Fy6ppmr6KQGE1wTSKc4lyZqlUPNLqEz5g5w5ma5HMSX5vonpxxAJlsgvk3W6hEibQ8mWOesLZrvrn9rkOsyia2pA4ic7c/132
    big_avatar = str(db_contact_head_image_ufs[2].data, encoding='utf-8')
    print(big_avatar)  # https://wx.qlogo.cn/mmhead/ver_1/hvqEga9QpsjIMqaZ3Fy6ppmr6KQGE1wTSKc4lyZqlUPNLqEz5g5w5ma5HMSX5vonpxxAJlsgvk3W6hEibQ8mWOesLZrvrn9rkOsyia2pA4ic7c/0
    print(db_contact_head_image_ufs[3].data)  # b''


if __name__ == '__main__':
    main()
