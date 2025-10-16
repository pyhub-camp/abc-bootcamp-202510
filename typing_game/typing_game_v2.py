import curses
import random
import time
from dataclasses import dataclass
from typing import List


WORDS: List[str] = """
ability adventure airport album almond anchor ancient answer apple arcade
artist aspect athlete atlas aurora autumn avenue bakery balance balloon
bamboo banner bargain beacon beauty because behave belief bicycle biology
blanket blossom border bottle bouquet bracket breeze bright brother bubble
bucket budget builder candle canvas canyon capital captain capture carbon
career carpet carrier castle cattle ceiling center century cereal chariot
cherish cherry chorus cinema circle citizen classic climate clover cluster
cobalt coffee comet comfort command common compass concept concert condor
coral corner cosmic cotton couple course cradle crater create cricket
crimson crystal culture custom dancer dawn decade defend degree deluxe
desert design detail device dialog diamond digital dinner doctor domain
dragon drawer drizzle dolphin eager early earth eclipse edge editor
effort elder elegant element eleven embark emerald emission empire empty
energy engine enjoy enough entire epic equal escape essay estate
event evolve exact exam exceed excel exchange excite exotic expand
expect expert express fabric factor falcon family famous fantasy farmer
fashion feather festive filter final finder finish flavor flight flower
forest fossil foster fountain fragile freedom frontier future galaxy garden
garlic gather gentle giant glacier glance global glory golden gossip
govern graceful granite graph gravity green guitar hammer harbor harmony
harvest hazelnut horizon hotel human humor hunter hybrid icicle icon
idea ignite image impact impulse index indoor infant inhale insect
inspire intact invite island ivory jacket jigsaw journey jewel justice
keeper kernel kingdom ladder lagoon lantern laser leader legend leisure
letter level liberty library lifeboat lightning linen liquid listen little
lively lizard logic lonely lotus lucky lunar luxury magnet maiden
manage marble margin marine market matrix meadow melody memory mentor
merit meteor method midnight mineral mirror mobile modern moment monkey
motion mountain museum muscle mystery nature nectar needle nephew neutral
noble nobody notion novel nurse oak object ocean office olive
""".split()

STAGE_WORD_COUNT = 10
MAX_ACTIVE_WORDS = 3
FRAME_DELAY = 0.05  # seconds between frames
MIN_SPEED = 2.0  # rows per second
MAX_SPEED = 4.5  # rows per second


@dataclass
class StageResult:
    cleared: bool
    correct: int
    attempts: int
    total: int

    @property
    def accuracy(self) -> float:
        if self.attempts == 0:
            return 0.0
        return (self.correct / self.attempts) * 100.0


class FallingWord:
    def __init__(self, text: str, x: int, speed: float) -> None:
        self.text = text
        self.x = x
        self.y = 1.0
        self.speed = speed

    def step(self, delta: float) -> None:
        self.y += self.speed * delta

    @property
    def row(self) -> int:
        return int(self.y)


def random_stage_words() -> List[str]:
    if len(WORDS) < STAGE_WORD_COUNT:
        raise ValueError("Not enough words to build a stage.")
    return random.sample(WORDS, STAGE_WORD_COUNT)


def safe_addstr(window: "curses._CursesWindow", y: int, x: int, text: str) -> None:
    height, width = window.getmaxyx()
    if y < 0 or y >= height or x >= width:
        return
    if x < 0:
        text = text[-x:]
        x = 0
    max_length = width - x
    if max_length <= 0:
        return
    try:
        window.addstr(y, x, text[:max_length])
    except curses.error:
        pass


def read_pending_keys(window: "curses._CursesWindow") -> List[str]:
    keys: List[str] = []
    while True:
        try:
            key = window.get_wch()
            keys.append(key)
        except curses.error:
            break
    return keys


def handle_input(
    keys: List[str],
    buffer: str,
    active_words: List[FallingWord],
    now: float,
    max_length: int,
) -> (str, int, int, bool, str, float):
    attempts = 0
    correct = 0
    message = ""
    message_until = 0.0
    exit_requested = False
    for key in keys:
        if key in ("\n", "\r"):
            normalized = buffer.strip().lower()
            if normalized:
                attempts += 1
                match_index = next(
                    (index for index, word in enumerate(active_words) if word.text == normalized),
                    None,
                )
                if match_index is not None:
                    del active_words[match_index]
                    correct += 1
                    message = "Nice!"
                else:
                    message = "Miss!"
                message_until = now + 0.8
            buffer = ""
        elif key in ("\b", "\x7f") or (isinstance(key, int) and key == curses.KEY_BACKSPACE):
            buffer = buffer[:-1]
        elif key == "\x1b":  # ESC
            exit_requested = True
            break
        elif isinstance(key, str) and key.isprintable():
            if len(buffer) < max_length:
                buffer += key.lower()
    return buffer, attempts, correct, exit_requested, message, message_until


def draw_interface(
    window: "curses._CursesWindow",
    active_words: List[FallingWord],
    buffer: str,
    message: str,
    message_until: float,
    now: float,
    correct: int,
    attempts: int,
    total: int,
) -> None:
    window.erase()
    height, width = window.getmaxyx()
    input_row = max(2, height - 2)
    ground_row = input_row - 1

    accuracy = (correct / attempts) * 100.0 if attempts else 0.0
    safe_addstr(window, 0, 0, "Typing Game v2 - Stage 1")
    safe_addstr(window, 1, 0, f"Cleared {correct}/{total}  Attempts {attempts}  Accuracy {accuracy:5.1f}%")

    for word in active_words:
        row = min(word.row, ground_row - 1)
        safe_addstr(window, row, word.x, word.text)

    safe_addstr(window, ground_row, 0, "-" * width)

    try:
        window.move(input_row, 0)
        window.clrtoeol()
    except curses.error:
        pass
    safe_addstr(window, input_row, 0, f"> {buffer}")

    if message and now <= message_until:
        safe_addstr(window, input_row - 1, 0, message)

    safe_addstr(window, height - 1, 0, "Enter=submit  ESC=quit")
    window.refresh()


def play_stage(window: "curses._CursesWindow", stage_words: List[str]) -> StageResult:
    curses.curs_set(0)
    window.nodelay(True)
    window.timeout(0)

    active_words: List[FallingWord] = []
    spawn_index = 0
    buffer = ""
    total_attempts = 0
    total_correct = 0
    message = ""
    message_until = 0.0

    last_time = time.monotonic()
    while True:
        now = time.monotonic()
        delta = now - last_time
        last_time = now

        height, width = window.getmaxyx()
        input_row = max(2, height - 2)
        ground_row = input_row - 1

        while len(active_words) < MAX_ACTIVE_WORDS and spawn_index < len(stage_words):
            word_text = stage_words[spawn_index]
            spawn_index += 1
            max_col = max(1, width - len(word_text) - 1)
            x = random.randint(1, max_col)
            speed = random.uniform(MIN_SPEED, MAX_SPEED)
            active_words.append(FallingWord(word_text, x, speed))

        keys = read_pending_keys(window)
        max_buffer = max(0, width - 4)
        if len(buffer) > max_buffer:
            buffer = buffer[:max_buffer]
        buffer, attempts, correct, exit_requested, new_message, new_until = handle_input(
            keys, buffer, active_words, now, max_buffer
        )
        total_attempts += attempts
        total_correct += correct
        if new_message:
            message = new_message
            message_until = new_until
        if exit_requested:
            return StageResult(False, total_correct, total_attempts, len(stage_words))

        for word in active_words:
            word.step(delta)

        if any(word.row >= ground_row for word in active_words):
            return StageResult(False, total_correct, total_attempts, len(stage_words))

        if total_correct >= len(stage_words):
            return StageResult(True, total_correct, total_attempts, len(stage_words))

        draw_interface(
            window,
            active_words,
            buffer,
            message,
            message_until,
            now,
            total_correct,
            total_attempts,
            len(stage_words),
        )
        time.sleep(FRAME_DELAY)


def show_result(window: "curses._CursesWindow", result: StageResult) -> None:
    window.nodelay(False)
    window.clear()
    outcome = "Stage Cleared!" if result.cleared else "Game Over"
    safe_addstr(window, 2, 2, outcome)
    safe_addstr(window, 4, 2, f"Words cleared: {result.correct}/{result.total}")
    safe_addstr(window, 5, 2, f"Attempts: {result.attempts}")
    safe_addstr(window, 6, 2, f"Accuracy: {result.accuracy:5.1f}%")
    safe_addstr(window, 8, 2, "Press any key to exit.")
    window.refresh()
    window.getch()


def main(stdscr: "curses._CursesWindow") -> None:
    stage_words = random_stage_words()
    stage_words = [word.lower() for word in stage_words]
    result = play_stage(stdscr, stage_words)
    show_result(stdscr, result)


if __name__ == "__main__":
    curses.wrapper(main)
