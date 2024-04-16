#include <bits/stdc++.h>

using uint32_t = unsigned int;

const char* get_var_int32_ptr_fallback(const char* p, const char* limit,
                                       uint32_t* value) {
  uint32_t result = 0;
  for (uint32_t shift = 0; shift <= 28 && p < limit; shift += 7) {
    uint32_t byte = *(reinterpret_cast<const unsigned char*>(p));
    p++;
    if (byte & 128) {
      // More bytes are present
      result |= ((byte & 127) << shift);
    } else {
      result |= (byte << shift);
      *value = result;
      return reinterpret_cast<const char*>(p);
    }
  }
  return NULL;
}

const char* calc_var_int32_ptr(const char* p, const char* limit,
                               uint32_t* value) {
  if (p < limit) {
    uint32_t result = *(reinterpret_cast<const unsigned char*>(p));
    if ((result & 0x80) == 0) {
      *value = result;
      return p + 1;
    }
  }
  return get_var_int32_ptr_fallback(p, limit, value);
}

int main(int argc, char const* argv[]) {
  const char* data =
      "\x90\x02R\xc2\x01\n$\x08 \x12 "
      "\x1b\xf5\x13\x05v6\x9b\xbc\xae\x8f)I\x13\xb0\xb2\x13\x90bP\x06&"
      "\x81uq\xcc\x9d\xb0."
      "\xf4\xa4\xbeJ\x12\x99\x01\x08\x93\x01\x12\x93\x01\x08\x90N\x12\x87\x01"
      "\xb4I\xe4|\x87\xa8]\xd1\xaf\x89}b\xb8\xd4I\t\xcb@\xe4H\xdd\xac[\x13|n&"
      "\x05C\x0b\rd\x9e\x92\x8b\x8c\xc6w\x0b9\x82\xfd\x86\x80("
      "\x893ms\x9a\xc2\xdc\xd3,\xa5(8\xfc\xe8V\xcf\x95\x1e<#\xfe\xbc\xaf\x00 "
      "j\xd1\x03\x15\x14Ez\xe1\xfc\xde\xee>\xfa\xc3c\xe6{"
      "6\x9c\xb1\xe4\x07\x19k\xa9\x85\x98\xd0\xf7\x05l\x8cEi\x93\x10J\x88\x9e7"
      "\x93pL\xe3\xd5\xa9\xc0`\xc73\xe0\xad\x02\xc0\xcb\t)\x97s\x08;"
      "\xaf\x03ow\x18\xe4\xf4\x87\xb1\r\n\x13wxid_r3f5pgkxrmf312\x12\x0e+"
      "8618376440480\x1a\x06\xe5\xa5\xbd\xe5\xa5\x87 "
      "\xef\xa0\x87\xd3\x03(\x020\x02:\x0e+8618376440480H\x00`\x00";
  int len = 274;
  uint32_t user_buffer_len = 0;
  const char* p = calc_var_int32_ptr(data, data + len, &user_buffer_len);
  std::cout << (p - data) << " " << user_buffer_len << std::endl;
  return 0;
}
