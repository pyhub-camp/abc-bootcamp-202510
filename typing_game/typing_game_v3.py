import curses
import json
import random
import socket
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


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
FRAME_DELAY = 0.05  # seconds
MIN_SPEED = 2.0
MAX_SPEED = 4.5
MESSAGE_DURATION = 0.8

ROLE_HOST = "host"
ROLE_GUEST = "guest"


@dataclass
class FallingWord:
    text: str
    x: int
    y: float
    speed: float

    def step(self, delta: float) -> None:
        self.y += self.speed * delta

    @property
    def row(self) -> int:
        return int(self.y)

    def to_payload(self) -> Dict[str, float]:
        return {"text": self.text, "x": self.x, "y": self.y}


@dataclass
class PlayerStats:
    correct: int = 0
    attempts: int = 0


@dataclass
class MessageState:
    text: str = ""
    seq: int = 0
    until: float = 0.0

    def set(self, text: str, now: float) -> None:
        self.text = text
        self.seq += 1
        self.until = now + MESSAGE_DURATION


class JsonConnection:
    def __init__(self, sock: socket.socket) -> None:
        self.sock = sock
        self.sock.setblocking(False)
        self.buffer = ""
        self.closed = False

    def send(self, payload: Dict) -> bool:
        if self.closed:
            return False
        try:
            data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8") + b"\n"
            self.sock.sendall(data)
            return True
        except (BrokenPipeError, ConnectionResetError, OSError):
            self.closed = True
            return False

    def recv(self) -> List[Dict]:
        messages: List[Dict] = []
        if self.closed:
            return messages
        while True:
            try:
                chunk = self.sock.recv(4096)
                if not chunk:
                    self.closed = True
                    break
                self.buffer += chunk.decode("utf-8")
            except BlockingIOError:
                break
            except ConnectionResetError:
                self.closed = True
                break
        while True:
            newline_index = self.buffer.find("\n")
            if newline_index == -1:
                break
            line = self.buffer[:newline_index]
            self.buffer = self.buffer[newline_index + 1 :]
            if not line.strip():
                continue
            try:
                messages.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return messages


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


def collect_input(
    keys: List[str],
    buffer: str,
    max_length: int,
) -> Tuple[str, List[str], bool]:
    submissions: List[str] = []
    exit_requested = False
    for key in keys:
        if key in ("\n", "\r"):
            normalized = buffer.strip().lower()
            if normalized:
                submissions.append(normalized)
            buffer = ""
        elif key in ("\b", "\x7f") or (isinstance(key, int) and key == curses.KEY_BACKSPACE):
            buffer = buffer[:-1]
        elif key == "\x1b":
            exit_requested = True
            break
        elif isinstance(key, str) and key.isprintable():
            if len(buffer) < max_length:
                buffer += key.lower()
    return buffer, submissions, exit_requested


def draw_game_ui(
    window: "curses._CursesWindow",
    view_words: List[Dict[str, int]],
    buffer: str,
    me_stats: PlayerStats,
    other_stats: PlayerStats,
    message_text: str,
    now: float,
    total_words: int,
    status_text: Optional[str] = None,
) -> None:
    window.erase()
    height, width = window.getmaxyx()
    input_row = max(2, height - 2)
    ground_row = input_row - 1

    cleared = me_stats.correct + other_stats.correct
    safe_addstr(window, 0, 0, "Typing Game v3 - 1:1 대전")
    safe_addstr(window, 1, 0, f"진행 {cleared}/{total_words}   Me {me_stats.correct}  Other {other_stats.correct}")

    for word in view_words:
        row = min(word["row"], ground_row - 1)
        safe_addstr(window, row, word["x"], word["text"])

    safe_addstr(window, ground_row, 0, "-" * width)

    try:
        window.move(input_row, 0)
        window.clrtoeol()
    except curses.error:
        pass
    safe_addstr(window, input_row, 0, f"> {buffer}")

    if message_text:
        safe_addstr(window, input_row - 1, 0, message_text)

    if status_text:
        safe_addstr(window, height - 1, 0, status_text)
    else:
        safe_addstr(window, height - 1, 0, "Enter=입력  ESC=종료")

    window.refresh()


def show_final_result(
    window: "curses._CursesWindow",
    me_stats: PlayerStats,
    other_stats: PlayerStats,
    total_words: int,
    result: Dict,
    role_label: str,
) -> None:
    window.nodelay(False)
    window.clear()
    reason = result.get("reason", "unknown")
    winner = result.get("winner")
    if reason == "cleared":
        if winner == role_label:
            title = "승리!"
        elif winner is None:
            title = "무승부"
        else:
            title = "패배..."
    elif reason == "ground":
        title = "단어가 땅에 닿았습니다"
    elif reason in ("host_exit", "guest_exit"):
        title = "상대가 게임을 종료했습니다" if winner != role_label else "게임을 종료했습니다"
    elif reason == "disconnect":
        title = "상대 연결이 끊어졌습니다"
    else:
        title = "게임 종료"

    safe_addstr(window, 2, 2, title)
    safe_addstr(window, 4, 2, f"총 단어: {total_words}")
    safe_addstr(window, 5, 2, f"My 점수: {me_stats.correct}  시도: {me_stats.attempts}")
    safe_addstr(window, 6, 2, f"Other 점수: {other_stats.correct}  시도: {other_stats.attempts}")
    safe_addstr(window, 8, 2, "아무 키나 누르면 종료합니다.")
    window.refresh()
    window.getch()


def process_submission(
    player_id: str,
    word: str,
    active_words: List[FallingWord],
    stats: Dict[str, PlayerStats],
    messages: Dict[str, MessageState],
    now: float,
) -> None:
    stats[player_id].attempts += 1
    match_index = next((idx for idx, fw in enumerate(active_words) if fw.text == word), None)
    opponent = ROLE_HOST if player_id == ROLE_GUEST else ROLE_GUEST
    if match_index is not None:
        removed = active_words.pop(match_index)
        stats[player_id].correct += 1
        messages[player_id].set(f"정답! {removed.text}", now)
        messages[opponent].set(f"상대가 {removed.text} 획득!", now)
    else:
        messages[player_id].set("오답!", now)


def build_state_payload(
    active_words: List[FallingWord],
    stats: Dict[str, PlayerStats],
    messages: Dict[str, MessageState],
    total_words: int,
    status: str,
    result: Optional[Dict],
) -> Dict:
    return {
        "type": "state",
        "active": [word.to_payload() for word in active_words],
        "scores": {
            ROLE_HOST: {"correct": stats[ROLE_HOST].correct, "attempts": stats[ROLE_HOST].attempts},
            ROLE_GUEST: {"correct": stats[ROLE_GUEST].correct, "attempts": stats[ROLE_GUEST].attempts},
        },
        "messages": {
            ROLE_HOST: {"text": messages[ROLE_HOST].text, "seq": messages[ROLE_HOST].seq},
            ROLE_GUEST: {"text": messages[ROLE_GUEST].text, "seq": messages[ROLE_GUEST].seq},
        },
        "total": total_words,
        "status": status,
        "result": result,
    }


def host_game(window: "curses._CursesWindow", connection: JsonConnection) -> None:
    curses.curs_set(0)
    window.nodelay(True)
    window.timeout(0)

    stats: Dict[str, PlayerStats] = {ROLE_HOST: PlayerStats(), ROLE_GUEST: PlayerStats()}
    messages: Dict[str, MessageState] = {ROLE_HOST: MessageState(), ROLE_GUEST: MessageState()}
    total_words = STAGE_WORD_COUNT
    stage_words = [word.lower() for word in random_stage_words()]
    active_words: List[FallingWord] = []
    spawn_index = 0
    buffer = ""
    last_time = time.monotonic()
    result: Optional[Dict] = None
    status = "running"

    connection.send({"type": "welcome", "player_id": ROLE_GUEST})

    while True:
        now = time.monotonic()
        delta = now - last_time
        last_time = now
        height, width = window.getmaxyx()
        input_row = max(2, height - 2)
        ground_row = input_row - 1
        max_buffer = max(0, width - 4)

        while len(active_words) < MAX_ACTIVE_WORDS and spawn_index < len(stage_words):
            word_text = stage_words[spawn_index]
            spawn_index += 1
            max_col = max(1, width - len(word_text) - 1)
            x = random.randint(1, max_col)
            speed = random.uniform(MIN_SPEED, MAX_SPEED)
            active_words.append(FallingWord(word_text, x, 1.0, speed))

        keys = read_pending_keys(window)
        buffer, submissions, exit_requested = collect_input(keys, buffer, max_buffer)

        for word in submissions:
            process_submission(ROLE_HOST, word, active_words, stats, messages, now)

        if exit_requested and status != "game_over":
            status = "game_over"
            result = {"winner": None, "reason": "host_exit"}

        for msg in connection.recv():
            if msg.get("type") == "submit":
                word = msg.get("word", "")
                if isinstance(word, str):
                    process_submission(ROLE_GUEST, word.lower(), active_words, stats, messages, now)
            elif msg.get("type") == "exit" and status != "game_over":
                status = "game_over"
                result = {"winner": ROLE_HOST, "reason": "guest_exit"}

        if connection.closed and status != "game_over":
            status = "game_over"
            result = {"winner": ROLE_HOST, "reason": "disconnect"}

        if status != "game_over":
            for word in active_words:
                word.step(delta)

            if any(word.row >= ground_row for word in active_words):
                status = "game_over"
                result = {"winner": None, "reason": "ground"}

            total_cleared = stats[ROLE_HOST].correct + stats[ROLE_GUEST].correct
            if total_cleared >= total_words and status != "game_over":
                if stats[ROLE_HOST].correct > stats[ROLE_GUEST].correct:
                    winner = ROLE_HOST
                elif stats[ROLE_HOST].correct < stats[ROLE_GUEST].correct:
                    winner = ROLE_GUEST
                else:
                    winner = None
                status = "game_over"
                result = {"winner": winner, "reason": "cleared"}

        payload = build_state_payload(active_words, stats, messages, total_words, status, result)
        connection.send(payload)

        host_message = messages[ROLE_HOST].text if now <= messages[ROLE_HOST].until else ""
        view_words = [{"text": w.text, "x": w.x, "row": min(w.row, ground_row - 1)} for w in active_words]
        status_text = "상대 연결 끊김" if connection.closed else None
        draw_game_ui(window, view_words, buffer, stats[ROLE_HOST], stats[ROLE_GUEST], host_message, now, total_words, status_text)

        if status == "game_over":
            break

        time.sleep(FRAME_DELAY)

    if result is None:
        result = {"winner": None, "reason": "unknown"}

    show_final_result(window, stats[ROLE_HOST], stats[ROLE_GUEST], total_words, result, ROLE_HOST)


def client_game(window: "curses._CursesWindow", connection: JsonConnection) -> None:
    curses.curs_set(0)
    window.nodelay(True)
    window.timeout(0)

    player_id = ROLE_GUEST
    buffer = ""
    last_time = time.monotonic()
    total_words = STAGE_WORD_COUNT
    stats: Dict[str, PlayerStats] = {
        ROLE_HOST: PlayerStats(),
        ROLE_GUEST: PlayerStats(),
    }
    message_seq = -1
    message_text = ""
    message_until = 0.0
    view_words: List[Dict[str, int]] = []
    status = "waiting"
    result: Optional[Dict] = None

    while True:
        now = time.monotonic()
        _ = now - last_time  # Not used but kept for parity
        last_time = now
        height, width = window.getmaxyx()
        input_row = max(2, height - 2)
        ground_row = input_row - 1
        max_buffer = max(0, width - 4)

        for msg in connection.recv():
            msg_type = msg.get("type")
            if msg_type == "welcome":
                assigned_id = msg.get("player_id")
                if assigned_id in (ROLE_HOST, ROLE_GUEST):
                    player_id = assigned_id
            elif msg_type == "state":
                total_words = msg.get("total", total_words)
                scores = msg.get("scores", {})
                for role in (ROLE_HOST, ROLE_GUEST):
                    role_score = scores.get(role, {})
                    stats[role].correct = role_score.get("correct", stats[role].correct)
                    stats[role].attempts = role_score.get("attempts", stats[role].attempts)
                incoming_messages = msg.get("messages", {})
                player_message = incoming_messages.get(player_id, {})
                seq = player_message.get("seq", message_seq)
                text = player_message.get("text", "")
                if seq != message_seq:
                    message_seq = seq
                    message_text = text
                    message_until = now + MESSAGE_DURATION
                elif now > message_until:
                    message_text = ""
                active = msg.get("active", [])
                view_words = []
                for entry in active:
                    try:
                        word_text = str(entry.get("text", ""))
                        x = int(entry.get("x", 0))
                        y_float = float(entry.get("y", 1.0))
                        row = int(y_float)
                        view_words.append({"text": word_text, "x": x, "row": min(row, ground_row - 1)})
                    except (ValueError, TypeError):
                        continue
                status = msg.get("status", status)
                result = msg.get("result") or result

        if connection.closed and status != "game_over":
            status = "game_over"
            result = {"winner": ROLE_HOST, "reason": "disconnect"}

        keys = read_pending_keys(window)
        buffer, submissions, exit_requested = collect_input(keys, buffer, max_buffer)
        for word in submissions:
            connection.send({"type": "submit", "word": word})

        if exit_requested:
            connection.send({"type": "exit"})
            if status != "game_over":
                status = "game_over"
                result = {"winner": ROLE_HOST, "reason": "guest_exit"}

        display_message = message_text if now <= message_until else ""

        cleared = stats[player_id].correct + stats[ROLE_HOST if player_id == ROLE_GUEST else ROLE_GUEST].correct
        status_text = None
        if status == "waiting":
            status_text = "서버 준비 대기중..."
        elif connection.closed:
            status_text = "연결 끊김"

        draw_game_ui(
            window,
            view_words,
            buffer,
            stats[player_id],
            stats[ROLE_HOST if player_id == ROLE_GUEST else ROLE_GUEST],
            display_message,
            now,
            total_words,
            status_text,
        )

        if status == "game_over":
            break

        time.sleep(FRAME_DELAY)

    if result is None:
        result = {"winner": None, "reason": "unknown"}

    other_role = ROLE_HOST if player_id == ROLE_GUEST else ROLE_GUEST
    show_final_result(window, stats[player_id], stats[other_role], total_words, result, player_id)


def host_entry() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind(("0.0.0.0", 0))
        server_sock.listen(1)
        host, port = server_sock.getsockname()
        print(f"[HOST] 서버를 시작했습니다. 포트: {port}")
        print("클라이언트 접속을 기다리는 중...")
        conn, addr = server_sock.accept()
        print(f"클라이언트 접속: {addr}")
        with conn:
            connection = JsonConnection(conn)
            curses.wrapper(lambda win: host_game(win, connection))


def client_entry() -> None:
    server_ip = input("서버 IP를 입력하세요: ").strip()
    port_text = input("서버 포트를 입력하세요: ").strip()
    try:
        port = int(port_text)
    except ValueError:
        print("포트 번호가 올바르지 않습니다.")
        return
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((server_ip, port))
        except OSError as exc:
            print(f"서버에 연결할 수 없습니다: {exc}")
            return
        connection = JsonConnection(sock)
        curses.wrapper(lambda win: client_game(win, connection))


def main() -> None:
    mode = input("모드를 선택하세요 (host / client): ").strip().lower()
    if mode in ("host", "h"):
        host_entry()
    elif mode in ("client", "c"):
        client_entry()
    else:
        print("모드를 정확히 입력해주세요 (host 또는 client).")


if __name__ == "__main__":
    main()
