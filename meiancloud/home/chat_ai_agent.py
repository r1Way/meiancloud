__all__ = ["process_ai_message"]

import sseclient
import requests
import json
import uuid


bot_app_key = "CKYuxNxnwIdoawZYszTUSPaMzObOwYFiKijlZBmfrCcCBOCWgSwfNwIFjnpErNgqpZuEbSSkONIwbtszYZxnKoaEYMFEfUJtkTAZKdcXPcWBZAgzjkFzxwWoejhTrRoj"  # 机器人密钥，不是BotBizId (从运营接口人处获取)
# 基于本机生成唯一的访客 ID（每次启动保持一致）
visitor_biz_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, "meiancloud.localhost"))
streaming_throttle = 1  # 节流控制


def sse_client(message: str, sid: str) -> str:
    req_data = {
        "content": "",
        "bot_app_key": bot_app_key,
        "visitor_biz_id": visitor_biz_id,
        "session_id": sid,
        "streaming_throttle": streaming_throttle,
    }
    try:
        content = message
        req_data["content"] = content
        resp = requests.post(
            "https://wss.lke.cloud.tencent.com/v1/qbot/chat/sse",
            data=json.dumps(req_data),
            stream=True,
            headers={"Accept": "text/event-stream"},
        )
        client = sseclient.SSEClient(resp)
        for ev in client.events():
            data = json.loads(ev.data)
            if ev.event == "reply":
                if data["payload"]["is_from_self"]:
                    pass
                elif data["payload"]["is_final"]:
                    reply = data["payload"]["content"]
                    return reply
            #     if data["payload"]["is_from_self"]:  # 自己发出的包
            #         # print(
            #         #     f'is_from_self, event:{ev.event}, "content:"{data["payload"]["content"]}'
            #         # )
            #         pass
            #     elif data["payload"][
            #         "is_final"
            #     ]:  # is_final=true，表示服务端reply事件的最后一条回复消息
            #         print(
            #             f'is_final, event:{ev.event}, "content:"{data["payload"]["content"]}'
            #         )
            #         # print(
            #         #     f'is_final，数据接收完成, event:{ev.event}, "data:"{data}'
            #         # )
            #     else:
            #         # print(f'event:{ev.event}, "data:"{data}')
            #         pass
            # else:
            #     # print(f'event:{ev.event}, "data:"{ev.data}')
            #     pass
        return "获取失败"
    except Exception as e:
        print(e)


def process_ai_message(message: str, session_id: str) -> str:
    """处理AI消息的核心函数"""
    print(f"message:{message}")
    try:
        assert isinstance(message, str)
        assert isinstance(session_id, str)
        message_lower = message.lower()
        reply = sse_client(message_lower, session_id)
        print(f"reply:{reply}")
        return reply
    except Exception as e:
        print(e)


if __name__ == "__main__":
    process_ai_message("你是谁")
