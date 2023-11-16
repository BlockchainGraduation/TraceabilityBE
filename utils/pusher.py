import pusher
from utils.pattern.singleton import Singleton


class PusherClient(Singleton):
    def __init__(self):
        self.pusher_client = pusher.Pusher(
            app_id="1692922",
            key="354fc3379d3a11a73464",
            secret="fee5d265369e54bea4ea",
            cluster="ap1",
            ssl=True,
        )

    def push_notification(self, channel, event, data_push):
        try:
            print("PusherClient: push_notification called")
            self.pusher_client.trigger(channel, event, data_push)
            print("PusherClient: push_notification called successes")
        except Exception as error:
            print("PusherClient: push_notification error")
