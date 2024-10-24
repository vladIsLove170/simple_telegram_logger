#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests


class Logger:
    def __init__(self, token: str, chat_id: int, verbose=False) -> None:
        self.token = token
        self.chat_id = chat_id

        self.verbose = verbose

        self.MAX_LENGTH_MESSAGE = 4096

    def send_message(self, message: str) -> bool:
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"

        payload = {
            "chat_id": self.chat_id,
            "text": message
        }

        result = requests.post(url, data=payload).json()

        status = result["ok"]

        if self.verbose:
            if not status:
                print(f"[-] {result['error_code']} {result['description']}")
            else:
                print(f"[+] Sent to {self.chat_id}.")

        return status

    def send_long_message(self, long_message: str) -> bool:
        msgs = [long_message[i:i + self.MAX_LENGTH_MESSAGE] for i in range(0, len(long_message), self.MAX_LENGTH_MESSAGE)]

        results = []

        for msg in msgs:
            status = self.send_message(msg)

            results.append(status)

        return all(results)

    def log(self, message: str) -> bool:
        if len(message) > self.MAX_LENGTH_MESSAGE:
            return self.send_long_message(message)
        else:
            return self.send_message(message)


if __name__ == "__main__":
    logger = Logger(token="", chat_id=12345678)

    logger.log(message="This is a test")
