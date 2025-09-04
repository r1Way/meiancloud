import uuid
import os


def get_session():
    # 生成一个 UUID
    new_uuid = uuid.uuid4()
    # 将 UUID 转换为字符串
    session_id = str(new_uuid)
    return session_id


def get_request_id():  # 生成的request_id有48位
    # 生成 24 个字节的随机数据
    random_bytes = os.urandom(24)

    # 将随机数据转换为十六进制字符串
    request_id = random_bytes.hex()
    return request_id


if __name__ == "__main__":
    sid = get_request_id()
    print(sid)
