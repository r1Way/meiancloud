import sseclient
import requests
import json
import session

bot_app_key = "dHKMoopXcBhIhWNEKNvzeHXkMaGOLvQeEFieLzzJfIgKXwVZFzMnKXzllwBbmdRrkmVorMJwsofdPgNhCfuNwAXkPPagzlDYEaCOVlzeBrimJBNPbwngqQlDYEIwseEp"  # 机器人密钥，不是BotBizId (从运营接口人处获取)
visitor_biz_id = (
    "202403130001"  # 访客 ID（外部系统提供，需确认不同的访客使用不同的 ID）
)
streaming_throttle = 1  # 节流控制


def sse_client(sid: str):
    req_data = {
        "content": "",
        "bot_app_key": bot_app_key,
        "visitor_biz_id": visitor_biz_id,
        "session_id": sid,
        "streaming_throttle": streaming_throttle,
    }
    try:
        while True:
            content = "你是"
            if content == "exit":
                exit(0)
            req_data["content"] = content
            # print(f'req_data:{req_data}')
            resp = requests.post(
                "https://wss.lke.cloud.tencent.com/v1/qbot/chat/sse",
                data=json.dumps(req_data),
                stream=True,
                headers={"Accept": "text/event-stream"},
            )
            # print(f"resp:{resp.text}")
            client = sseclient.SSEClient(resp)
            for ev in client.events():
                # print(f'event:{ev.event}, "data:"{ev.data}')
                data = json.loads(ev.data)
                if ev.event == "reply":
                    if data["payload"]["is_from_self"]:  # 自己发出的包
                        # print(
                        #     f'is_from_self, event:{ev.event}, "content:"{data["payload"]["content"]}'
                        # )
                        pass
                    elif data["payload"][
                        "is_final"
                    ]:  # is_final=true，表示服务端reply事件的最后一条回复消息
                        # print(
                        #     f'is_final, event:{ev.event}, "content:"{data["payload"]["content"]}'
                        # )
                        print(data)
                        # print(
                        #     f'is_final，数据接收完成, event:{ev.event}, "data:"{data}'
                        # )
                    else:
                        # print(f'event:{ev.event}, "data:"{data}')
                        pass
                else:
                    # print(f'event:{ev.event}, "data:"{ev.data}')
                    pass
    except Exception as e:
        print(e)


if __name__ == "__main__":
    session_id = session.get_session()
    sse_client(session_id)
