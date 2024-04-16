from google.protobuf.unknown_fields import UnknownFieldSet
from google.protobuf.internal import decoder


def get_str_from_unknown_field_set(ufs: UnknownFieldSet, idx: int):
    if len(ufs) < idx + 1:
        return ''
    return str(ufs[idx].data, encoding='utf-8')


def get_str_from_ufs_and_target_fn(ufs: UnknownFieldSet, target_field_number: int):
    data = find_unknown_field_by_number(ufs, target_field_number)
    return str(data, encoding='utf-8')


def decode_var_int32(data: bytes, pos: int):
    return decoder._DecodeVarint32(data, pos)


def find_unknown_field_by_number(ufs: UnknownFieldSet, target_field_number: int):
    for unknown_field in ufs:
        field_number = unknown_field.field_number
        data = unknown_field.data
        if field_number != target_field_number:
            continue
        return data
