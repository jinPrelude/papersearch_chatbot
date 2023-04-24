from collections import deque


class HistoryHolder:
    def __init__(self, max_word_len: int = 512) -> None:
        self.history = deque()
        self.history.append("[user input, ai response]")
        self.history_len = deque()
        self.total_len = 0
        self.max_word_len = max_word_len

    def append(self, user: str, ai_response: str) -> None:

        dialog = f"[{user}, {ai_response}]"
        self.history.append(dialog)
        dialog_len = len(dialog.split())
        self.history_len.append(dialog_len)
        self.total_len += dialog_len
        while self.total_len > self.max_word_len:
            self.total_len -= self.history_len.popleft()
            self.history.popleft()

    def return_str(self) -> str:
        return "".join(self.history)
