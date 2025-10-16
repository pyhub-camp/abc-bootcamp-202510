from __future__ import annotations

import json
import math
import random
import socket
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

try:
    import pygame
except ModuleNotFoundError as exc:
    raise SystemExit("pygame 모듈이 설치되어 있지 않습니다. 'pip install pygame'을 먼저 실행해주세요.") from exc


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
MESSAGE_DURATION = 0.9
FEEDBACK_DURATION = 0.45

ROLE_HOST = "host"
ROLE_GUEST = "guest"


@dataclass
class GameConfig:
    width: int = 960
    height: int = 720
    fps: int = 60
    padding: int = 32
    spawn_y: float = 120.0
    input_height: int = 110
    input_margin: int = 28
    ground_line_offset: int = 18
    max_active_words: int = MAX_ACTIVE_WORDS
    max_buffer_chars: int = 24
    word_speed_range: Tuple[float, float] = (120.0, 220.0)
    font_name: Optional[str] = None
    font_candidates: List[str] = field(
        default_factory=lambda: [
            "Apple SD Gothic Neo",
            "AppleSDGothicNeo",
            "Malgun Gothic",
            "MalgunGothic",
            "NanumGothic",
            "Nanum Gothic",
            "Noto Sans CJK KR",
            "Noto Sans KR",
            "Arial Unicode MS",
            "Segoe UI",
        ]
    )
    word_font_size: int = 52
    message_font_size: int = 36
    ui_font_size: int = 30
    small_font_size: int = 22
    background_top_color: Tuple[int, int, int] = (18, 23, 52)
    background_bottom_color: Tuple[int, int, int] = (48, 20, 65)
    base_overlay_color: Tuple[int, int, int] = (80, 45, 120)
    ground_fill_color: Tuple[int, int, int] = (36, 40, 70)
    ground_line_color: Tuple[int, int, int] = (140, 150, 200)
    title_color: Tuple[int, int, int] = (140, 205, 255)
    text_color: Tuple[int, int, int] = (230, 235, 255)
    status_color: Tuple[int, int, int] = (190, 195, 220)
    progress_bg_color: Tuple[int, int, int] = (60, 70, 110)
    progress_color: Tuple[int, int, int] = (90, 200, 140)
    buffer_bg_color: Tuple[int, int, int, int] = (12, 12, 30, 180)
    buffer_border_color: Tuple[int, int, int] = (90, 95, 160)
    buffer_text_color: Tuple[int, int, int] = (235, 236, 255)
    buffer_placeholder_color: Tuple[int, int, int] = (140, 145, 180)
    caret_color: Tuple[int, int, int] = (255, 255, 255)
    word_shadow_offset: int = 4
    menu_selected_color: Tuple[int, int, int] = (255, 255, 255)
    menu_idle_color: Tuple[int, int, int] = (190, 195, 220)
    menu_hint_color: Tuple[int, int, int] = (150, 160, 210)
    menu_box_color: Tuple[int, int, int] = (40, 48, 90)
    error_color: Tuple[int, int, int] = (255, 140, 160)
    word_palette: List[Tuple[int, int, int]] = field(
        default_factory=lambda: [
            (255, 140, 105),
            (255, 200, 120),
            (120, 215, 200),
            (140, 180, 255),
            (220, 150, 240),
            (255, 110, 160),
            (170, 255, 140),
        ]
    )
    overlay_colors: Dict[str, Tuple[int, int, int]] = field(
        default_factory=lambda: {
            "success": (90, 190, 120),
            "warning": (200, 80, 90),
            "failure": (200, 80, 90),
            "info": (80, 140, 220),
            "neutral": (0, 0, 0),
        }
    )
    message_colors: Dict[str, Tuple[int, int, int]] = field(
        default_factory=lambda: {
            "success": (140, 235, 170),
            "warning": (255, 140, 160),
            "failure": (255, 140, 160),
            "info": (170, 200, 255),
            "neutral": (220, 225, 245),
        }
    )


@dataclass
class WordSurface:
    surface: "pygame.Surface"
    shadow: "pygame.Surface"
    width: int
    height: int


@dataclass
class FallingWord:
    text: str
    x: float
    y: float
    speed: float
    color: Tuple[int, int, int]
    display: WordSurface

    def step(self, delta: float) -> None:
        self.y += self.speed * delta

    @property
    def bottom(self) -> float:
        return self.y + self.display.height

    def to_payload(self) -> Dict[str, float]:
        return {
            "text": self.text,
            "x": self.x,
            "y": self.y,
            "color": list(self.color),
        }


@dataclass
class PlayerStats:
    correct: int = 0
    attempts: int = 0


@dataclass
class MessageState:
    text: str = ""
    seq: int = 0
    until: float = 0.0
    style: str = "neutral"

    def set(self, text: str, now: float, style: str = "neutral") -> None:
        self.text = text
        self.seq += 1
        self.until = now + MESSAGE_DURATION
        self.style = style


@dataclass
class FeedbackPulse:
    kind: str = "neutral"
    until: float = 0.0
    duration: float = FEEDBACK_DURATION

    def trigger(self, kind: str, now: float, duration: float = FEEDBACK_DURATION) -> None:
        self.kind = kind
        self.duration = duration
        self.until = now + duration

    def value(self, now: float) -> Tuple[str, float]:
        if now >= self.until:
            return ("neutral", 0.0)
        remaining = self.until - now
        if self.duration <= 0:
            return (self.kind, 0.0)
        strength = max(0.0, min(1.0, remaining / self.duration))
        return (self.kind, strength)


class WordSurfaceCache:
    def __init__(self, font: "pygame.font.Font") -> None:
        self.font = font
        self._cache: Dict[Tuple[str, Tuple[int, int, int]], WordSurface] = {}

    def get(self, text: str, color: Tuple[int, int, int]) -> WordSurface:
        key = (text, color)
        cached = self._cache.get(key)
        if cached is not None:
            return cached
        text_surface = self.font.render(text, True, color).convert_alpha()
        shadow_surface = self.font.render(text, True, (0, 0, 0)).convert_alpha()
        shadow_surface.set_alpha(140)
        cached = WordSurface(
            surface=text_surface,
            shadow=shadow_surface,
            width=text_surface.get_width(),
            height=text_surface.get_height(),
        )
        self._cache[key] = cached
        return cached


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

    def close(self) -> None:
        if self.closed:
            try:
                self.sock.close()
            except OSError:
                pass
            return
        self.closed = True
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        finally:
            try:
                self.sock.close()
            except OSError:
                pass


def random_stage_words() -> List[str]:
    if len(WORDS) < STAGE_WORD_COUNT:
        raise ValueError("Not enough words to build a stage.")
    return random.sample(WORDS, STAGE_WORD_COUNT)


def create_gradient_surface(
    width: int, height: int, top_color: Tuple[int, int, int], bottom_color: Tuple[int, int, int]
) -> "pygame.Surface":
    surface = pygame.Surface((width, height)).convert()
    if height <= 1:
        surface.fill(top_color)
        return surface
    for y in range(height):
        ratio = y / (height - 1)
        color = tuple(int(top_color[i] + (bottom_color[i] - top_color[i]) * ratio) for i in range(3))
        pygame.draw.line(surface, color, (0, y), (width, y))
    return surface


def ground_line_y(config: GameConfig) -> int:
    return config.height - config.input_margin - config.input_height - config.ground_line_offset


@dataclass
class PygameAssets:
    screen: "pygame.Surface"
    gradient_bg: "pygame.Surface"
    word_cache: WordSurfaceCache
    font_word: "pygame.font.Font"
    font_message: "pygame.font.Font"
    font_ui: "pygame.font.Font"
    font_small: "pygame.font.Font"
    pulse_overlay: "pygame.Surface"
    feedback_overlay: "pygame.Surface"
    input_surface: "pygame.Surface"


def _make_font(config: GameConfig, size: int) -> "pygame.font.Font":
    candidates = [name for name in config.font_candidates if name]
    matched: Optional[str] = None
    if candidates:
        matched = pygame.font.match_font(candidates)
    if matched:
        return pygame.font.Font(matched, size)
    if config.font_name:
        return pygame.font.SysFont(config.font_name, size)
    return pygame.font.SysFont(None, size)


def init_pygame(config: GameConfig) -> PygameAssets:
    screen = pygame.display.set_mode((config.width, config.height))
    pygame.display.set_caption("Typing Game v4 (Pygame)")
    word_font = _make_font(config, config.word_font_size)
    message_font = _make_font(config, config.message_font_size)
    ui_font = _make_font(config, config.ui_font_size)
    small_font = _make_font(config, config.small_font_size)
    gradient_bg = create_gradient_surface(
        config.width, config.height, config.background_top_color, config.background_bottom_color
    )
    word_cache = WordSurfaceCache(word_font)
    pulse_overlay = pygame.Surface((config.width, config.height), pygame.SRCALPHA)
    feedback_overlay = pygame.Surface((config.width, config.height), pygame.SRCALPHA)
    input_surface = pygame.Surface((config.width - config.padding * 2, config.input_height), pygame.SRCALPHA)
    return PygameAssets(
        screen=screen,
        gradient_bg=gradient_bg,
        word_cache=word_cache,
        font_word=word_font,
        font_message=message_font,
        font_ui=ui_font,
        font_small=small_font,
        pulse_overlay=pulse_overlay,
        feedback_overlay=feedback_overlay,
        input_surface=input_surface,
    )


RenderableWord = Tuple[WordSurface, float, float]


def draw_gameplay_screen(
    assets: PygameAssets,
    config: GameConfig,
    words: List[RenderableWord],
    buffer: str,
    message: Tuple[str, str],
    status_text: Optional[str],
    total_words: int,
    me_stats: PlayerStats,
    other_stats: PlayerStats,
    role_label: str,
    opponent_label: str,
    overlay_info: Tuple[str, float],
    now: float,
) -> None:
    screen = assets.screen
    screen.blit(assets.gradient_bg, (0, 0))

    pulse_alpha = int(22 + 28 * ((math.sin(now * 0.9) + 1.0) * 0.5))
    if pulse_alpha > 0:
        assets.pulse_overlay.fill((*config.base_overlay_color, pulse_alpha))
        screen.blit(assets.pulse_overlay, (0, 0))

    overlay_kind, overlay_strength = overlay_info
    overlay_color = config.overlay_colors.get(overlay_kind)
    if overlay_color and overlay_strength > 0.0:
        alpha = int(160 * overlay_strength)
        if alpha > 0:
            assets.feedback_overlay.fill((*overlay_color, alpha))
            screen.blit(assets.feedback_overlay, (0, 0))

    padding = config.padding
    title_surface = assets.font_ui.render("Typing Game v4 - Pygame", True, config.title_color)
    screen.blit(title_surface, (padding, padding))

    cleared = me_stats.correct + other_stats.correct
    progress_rect = pygame.Rect(
        padding,
        padding + title_surface.get_height() + 12,
        config.width - padding * 2,
        18,
    )
    pygame.draw.rect(screen, config.progress_bg_color, progress_rect, border_radius=9)
    if total_words > 0:
        ratio = max(0.0, min(1.0, cleared / total_words))
        if ratio > 0.0:
            progress_inner = progress_rect.copy()
            progress_inner.width = max(1, int(progress_rect.width * ratio))
            pygame.draw.rect(screen, config.progress_color, progress_inner, border_radius=9)

    stats_y = progress_rect.bottom + 18
    me_text = assets.font_ui.render(
        f"{role_label} 점수 {me_stats.correct} / 시도 {me_stats.attempts}", True, config.text_color
    )
    other_text = assets.font_ui.render(
        f"{opponent_label} 점수 {other_stats.correct} / 시도 {other_stats.attempts}", True, config.text_color
    )
    screen.blit(me_text, (padding, stats_y))
    screen.blit(other_text, (config.width - padding - other_text.get_width(), stats_y))

    progress_label = assets.font_small.render(f"진행 {cleared}/{total_words}", True, config.status_color)
    screen.blit(progress_label, ((config.width - progress_label.get_width()) // 2, stats_y))

    message_text, message_style = message
    if message_text:
        message_color = config.message_colors.get(message_style, config.message_colors["neutral"])
        message_surface = assets.font_message.render(message_text, True, message_color)
        screen.blit(
            message_surface,
            ((config.width - message_surface.get_width()) // 2, stats_y + me_text.get_height() + 12),
        )

    g_line_y = ground_line_y(config)
    ground_rect = pygame.Rect(0, g_line_y, config.width, config.height - g_line_y)
    pygame.draw.rect(screen, config.ground_fill_color, ground_rect)
    pygame.draw.line(
        screen,
        config.ground_line_color,
        (padding, g_line_y),
        (config.width - padding, g_line_y),
        3,
    )

    shadow_offset = config.word_shadow_offset
    for display, x, y in words:
        int_x = int(x)
        int_y = int(y)
        screen.blit(display.shadow, (int_x + shadow_offset, int_y + shadow_offset))
        screen.blit(display.surface, (int_x, int_y))

    input_rect = pygame.Rect(
        padding,
        config.height - config.input_margin - config.input_height,
        config.width - padding * 2,
        config.input_height,
    )
    assets.input_surface.fill(config.buffer_bg_color)
    screen.blit(assets.input_surface, input_rect.topleft)
    pygame.draw.rect(screen, config.buffer_border_color, input_rect, width=2, border_radius=18)

    prompt_text = buffer if buffer else ""
    render_text = f"> {prompt_text}"
    text_color = config.buffer_text_color if buffer else config.buffer_placeholder_color
    buffer_surface = assets.font_ui.render(render_text, True, text_color)
    buffer_pos = (
        input_rect.left + 24,
        input_rect.top + (input_rect.height - buffer_surface.get_height()) // 2,
    )
    screen.blit(buffer_surface, buffer_pos)

    caret_visible = (int(now * 2) % 2) == 0
    if caret_visible:
        caret_x = buffer_pos[0] + buffer_surface.get_width() + 6
        caret_height = buffer_surface.get_height()
        caret_rect = pygame.Rect(caret_x, buffer_pos[1], 3, caret_height)
        pygame.draw.rect(screen, config.caret_color, caret_rect)

    if status_text:
        status_surface = assets.font_small.render(status_text, True, config.status_color)
    else:
        status_surface = assets.font_small.render("Enter=입력  ESC=종료", True, config.status_color)
    screen.blit(
        status_surface,
        (padding, config.height - status_surface.get_height() - config.input_margin // 2),
    )

    pygame.display.flip()


def resolve_message_for_display(message_state: MessageState, now: float) -> Tuple[str, str]:
    if now <= message_state.until:
        return (message_state.text, message_state.style)
    return ("", "neutral")


def process_submission(
    player_id: str,
    word: str,
    active_words: List[FallingWord],
    stats: Dict[str, PlayerStats],
    messages: Dict[str, MessageState],
    feedback: Dict[str, FeedbackPulse],
    now: float,
) -> None:
    stats[player_id].attempts += 1
    match_index = next((idx for idx, fw in enumerate(active_words) if fw.text == word), None)
    opponent = ROLE_HOST if player_id == ROLE_GUEST else ROLE_GUEST
    if match_index is not None:
        removed = active_words.pop(match_index)
        stats[player_id].correct += 1
        messages[player_id].set(f"정답! {removed.text}", now, style="success")
        if opponent in messages:
            messages[opponent].set(f"상대가 {removed.text} 획득!", now, style="info")
        feedback[player_id].trigger("success", now)
    else:
        messages[player_id].set("오답!", now, style="warning")
        feedback[player_id].trigger("warning", now)


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
            ROLE_HOST: {
                "text": messages[ROLE_HOST].text,
                "seq": messages[ROLE_HOST].seq,
                "style": messages[ROLE_HOST].style,
            },
            ROLE_GUEST: {
                "text": messages[ROLE_GUEST].text,
                "seq": messages[ROLE_GUEST].seq,
                "style": messages[ROLE_GUEST].style,
            },
        },
        "total": total_words,
        "status": status,
        "result": result,
    }


def spawn_word(word_text: str, config: GameConfig, assets: PygameAssets) -> FallingWord:
    color = random.choice(config.word_palette)
    display = assets.word_cache.get(word_text, color)
    max_x = config.width - config.padding - display.width
    if max_x <= config.padding:
        x = float(config.padding)
    else:
        x = random.uniform(config.padding, max_x)
    speed = random.uniform(*config.word_speed_range)
    return FallingWord(
        text=word_text,
        x=x,
        y=config.spawn_y,
        speed=speed,
        color=color,
        display=display,
    )


def words_to_renderable(words: List[FallingWord]) -> List[RenderableWord]:
    return [(word.display, word.x, word.y) for word in words]


def parse_color(value: object, fallback: Tuple[int, int, int]) -> Tuple[int, int, int]:
    if isinstance(value, (list, tuple)) and len(value) == 3:
        try:
            r, g, b = (int(max(0, min(255, int(float(v))))) for v in value)
            return (r, g, b)
        except (TypeError, ValueError):
            return fallback
    return fallback


def show_final_result(
    assets: PygameAssets,
    config: GameConfig,
    me_stats: PlayerStats,
    other_stats: PlayerStats,
    total_words: int,
    result: Optional[Dict],
    role_key: str,
    me_label: str,
    other_label: str,
) -> None:
    screen = assets.screen
    clock = pygame.time.Clock()
    pygame.key.stop_text_input()

    if result is None:
        result = {"winner": None, "reason": "unknown"}

    winner = result.get("winner")
    reason = result.get("reason", "unknown")
    if reason == "cleared":
        if winner == role_key:
            title = "승리!"
        elif winner is None:
            title = "무승부"
        else:
            title = "패배..."
    elif reason == "ground":
        title = "단어가 땅에 닿았습니다"
    elif reason == "host_exit":
        title = "게임을 종료했습니다"
    elif reason == "guest_exit":
        title = "상대가 게임을 종료했습니다" if winner != role_key else "게임을 종료했습니다"
    elif reason == "disconnect":
        title = "연결이 끊어졌습니다"
    else:
        title = "게임 종료"

    lines = [
        f"총 단어: {total_words}",
        f"{me_label} 점수: {me_stats.correct}  시도: {me_stats.attempts}",
        f"{other_label} 점수: {other_stats.correct}  시도: {other_stats.attempts}",
        "아무 키나 누르면 로비로 돌아갑니다.",
    ]

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                waiting = False
                break

        screen.blit(assets.gradient_bg, (0, 0))
        assets.pulse_overlay.fill((0, 0, 0, 180))
        screen.blit(assets.pulse_overlay, (0, 0))

        title_surface = assets.font_message.render(title, True, config.message_colors["info"])
        screen.blit(title_surface, ((config.width - title_surface.get_width()) // 2, config.height // 4))

        for idx, line in enumerate(lines):
            text_surface = assets.font_ui.render(line, True, config.text_color)
            screen.blit(
                text_surface,
                (
                    (config.width - text_surface.get_width()) // 2,
                    config.height // 4 + title_surface.get_height() + 30 + idx * (text_surface.get_height() + 12),
                ),
            )

        pygame.display.flip()
        clock.tick(30)


def solo_game(assets: PygameAssets, config: GameConfig) -> None:
    clock = pygame.time.Clock()
    pygame.key.start_text_input()

    stats: Dict[str, PlayerStats] = {ROLE_HOST: PlayerStats(), ROLE_GUEST: PlayerStats()}
    messages: Dict[str, MessageState] = {ROLE_HOST: MessageState(), ROLE_GUEST: MessageState()}
    feedback: Dict[str, FeedbackPulse] = {ROLE_HOST: FeedbackPulse()}

    total_words = STAGE_WORD_COUNT
    stage_words = [word.lower() for word in random_stage_words()]
    active_words: List[FallingWord] = []
    spawn_index = 0
    buffer = ""
    status = "running"
    result: Optional[Dict] = None

    try:
        running = True
        while running:
            dt = clock.tick(config.fps) / 1000.0
            now = time.monotonic()
            submissions: List[str] = []
            exit_requested = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_requested = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit_requested = True
                    elif event.key == pygame.K_BACKSPACE:
                        buffer = buffer[:-1]
                    elif event.key == pygame.K_RETURN:
                        normalized = buffer.strip().lower()
                        if normalized:
                            submissions.append(normalized)
                        buffer = ""
                elif event.type == pygame.TEXTINPUT:
                    if len(buffer) < config.max_buffer_chars:
                        buffer += event.text.lower()

            for word in submissions:
                process_submission(ROLE_HOST, word, active_words, stats, messages, feedback, now)

            if exit_requested and status != "game_over":
                status = "game_over"
                result = {"winner": ROLE_HOST, "reason": "host_exit"}

            if status != "game_over":
                while len(active_words) < config.max_active_words and spawn_index < len(stage_words):
                    word_text = stage_words[spawn_index]
                    spawn_index += 1
                    active_words.append(spawn_word(word_text, config, assets))

                for word in active_words:
                    word.step(dt)

                if any(word.bottom >= ground_line_y(config) for word in active_words):
                    status = "game_over"
                    result = {"winner": None, "reason": "ground"}

                cleared = stats[ROLE_HOST].correct
                if cleared >= total_words and status != "game_over":
                    status = "game_over"
                    result = {"winner": ROLE_HOST, "reason": "cleared"}

            host_message = resolve_message_for_display(messages[ROLE_HOST], now)
            overlay_info = feedback[ROLE_HOST].value(now)
            draw_gameplay_screen(
                assets,
                config,
                words_to_renderable(active_words),
                buffer,
                host_message,
                None,
                total_words,
                stats[ROLE_HOST],
                stats[ROLE_GUEST],
                "플레이어",
                "목표",
                overlay_info,
                now,
            )

            if status == "game_over":
                running = False

        if result is None:
            result = {"winner": None, "reason": "unknown"}

        show_final_result(assets, config, stats[ROLE_HOST], stats[ROLE_GUEST], total_words, result, ROLE_HOST, "플레이어", "목표")
    finally:
        pygame.key.stop_text_input()


def host_game(assets: PygameAssets, config: GameConfig, connection: JsonConnection) -> None:
    clock = pygame.time.Clock()
    pygame.key.start_text_input()

    stats: Dict[str, PlayerStats] = {ROLE_HOST: PlayerStats(), ROLE_GUEST: PlayerStats()}
    messages: Dict[str, MessageState] = {ROLE_HOST: MessageState(), ROLE_GUEST: MessageState()}
    feedback: Dict[str, FeedbackPulse] = {ROLE_HOST: FeedbackPulse(), ROLE_GUEST: FeedbackPulse()}

    total_words = STAGE_WORD_COUNT
    stage_words = [word.lower() for word in random_stage_words()]
    active_words: List[FallingWord] = []
    spawn_index = 0
    buffer = ""
    status = "running"
    result: Optional[Dict] = None
    connection.send({"type": "welcome", "player_id": ROLE_GUEST})

    try:
        running = True
        while running:
            dt = clock.tick(config.fps) / 1000.0
            now = time.monotonic()
            submissions: List[str] = []
            exit_requested = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_requested = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit_requested = True
                    elif event.key == pygame.K_BACKSPACE:
                        buffer = buffer[:-1]
                    elif event.key == pygame.K_RETURN:
                        normalized = buffer.strip().lower()
                        if normalized:
                            submissions.append(normalized)
                        buffer = ""
                elif event.type == pygame.TEXTINPUT:
                    if len(buffer) < config.max_buffer_chars:
                        buffer += event.text.lower()

            for word in submissions:
                process_submission(ROLE_HOST, word, active_words, stats, messages, feedback, now)

            if exit_requested and status != "game_over":
                status = "game_over"
                result = {"winner": None, "reason": "host_exit"}

            for msg in connection.recv():
                msg_type = msg.get("type")
                if msg_type == "submit":
                    word = msg.get("word", "")
                    if isinstance(word, str):
                        process_submission(ROLE_GUEST, word.lower(), active_words, stats, messages, feedback, now)
                elif msg_type == "exit" and status != "game_over":
                    status = "game_over"
                    result = {"winner": ROLE_HOST, "reason": "guest_exit"}

            if connection.closed and status != "game_over":
                status = "game_over"
                result = {"winner": ROLE_HOST, "reason": "disconnect"}

            if status != "game_over":
                while len(active_words) < config.max_active_words and spawn_index < len(stage_words):
                    word_text = stage_words[spawn_index]
                    spawn_index += 1
                    active_words.append(spawn_word(word_text, config, assets))

                for word in active_words:
                    word.step(dt)

                if any(word.bottom >= ground_line_y(config) for word in active_words):
                    status = "game_over"
                    result = {"winner": None, "reason": "ground"}

                cleared = stats[ROLE_HOST].correct + stats[ROLE_GUEST].correct
                if cleared >= total_words and status != "game_over":
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

            host_message = resolve_message_for_display(messages[ROLE_HOST], now)
            status_text = "상대 연결 끊김" if connection.closed else None
            overlay_info = feedback[ROLE_HOST].value(now)
            draw_gameplay_screen(
                assets,
                config,
                words_to_renderable(active_words),
                buffer,
                host_message,
                status_text,
                total_words,
                stats[ROLE_HOST],
                stats[ROLE_GUEST],
                "나",
                "상대",
                overlay_info,
                now,
            )

            if status == "game_over":
                running = False

        if result is None:
            result = {"winner": None, "reason": "unknown"}

        show_final_result(
            assets,
            config,
            stats[ROLE_HOST],
            stats[ROLE_GUEST],
            total_words,
            result,
            ROLE_HOST,
            "나",
            "상대",
        )
    finally:
        pygame.key.stop_text_input()


def client_game(assets: PygameAssets, config: GameConfig, connection: JsonConnection) -> None:
    clock = pygame.time.Clock()
    pygame.key.start_text_input()

    player_id = ROLE_GUEST
    other_role = ROLE_HOST
    buffer = ""
    total_words = STAGE_WORD_COUNT
    stats: Dict[str, PlayerStats] = {ROLE_HOST: PlayerStats(), ROLE_GUEST: PlayerStats()}
    view_words: List[RenderableWord] = []
    message_seq = -1
    message_text = ""
    message_style = "neutral"
    message_until = 0.0
    status = "waiting"
    result: Optional[Dict] = None
    feedback = FeedbackPulse()

    try:
        running = True
        while running:
            dt = clock.tick(config.fps) / 1000.0
            now = time.monotonic()
            submissions: List[str] = []
            exit_requested = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_requested = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit_requested = True
                    elif event.key == pygame.K_BACKSPACE:
                        buffer = buffer[:-1]
                    elif event.key == pygame.K_RETURN:
                        normalized = buffer.strip().lower()
                        if normalized:
                            submissions.append(normalized)
                        buffer = ""
                elif event.type == pygame.TEXTINPUT:
                    if len(buffer) < config.max_buffer_chars:
                        buffer += event.text.lower()

            for word in submissions:
                connection.send({"type": "submit", "word": word})

            if exit_requested:
                connection.send({"type": "exit"})
                if status != "game_over":
                    status = "game_over"
                    result = {"winner": ROLE_HOST, "reason": "guest_exit"}

            for msg in connection.recv():
                msg_type = msg.get("type")
                if msg_type == "welcome":
                    assigned = msg.get("player_id")
                    if assigned in (ROLE_HOST, ROLE_GUEST):
                        player_id = assigned
                        other_role = ROLE_HOST if player_id == ROLE_GUEST else ROLE_GUEST
                elif msg_type == "state":
                    total_words = msg.get("total", total_words)
                    scores = msg.get("scores", {})
                    for role in (ROLE_HOST, ROLE_GUEST):
                        role_score = scores.get(role, {})
                        stats[role].correct = int(role_score.get("correct", stats[role].correct))
                        stats[role].attempts = int(role_score.get("attempts", stats[role].attempts))

                    incoming_messages = msg.get("messages", {})
                    player_message = incoming_messages.get(player_id, {})
                    seq = player_message.get("seq", message_seq)
                    if isinstance(seq, int) and seq != message_seq:
                        message_seq = seq
                        message_text = str(player_message.get("text", ""))
                        message_style = str(player_message.get("style", "neutral"))
                        message_until = now + MESSAGE_DURATION
                        if message_style in ("success", "warning", "failure"):
                            feedback.trigger(message_style, now)
                        else:
                            feedback.trigger("neutral", now, duration=0.0)
                    elif now > message_until:
                        message_text = ""
                        message_style = "neutral"

                    active = msg.get("active", [])
                    new_views: List[RenderableWord] = []
                    for entry in active:
                        text_value = entry.get("text")
                        x_value = entry.get("x")
                        y_value = entry.get("y")
                        if not isinstance(text_value, str):
                            continue
                        try:
                            x = float(x_value)
                            y = float(y_value)
                        except (TypeError, ValueError):
                            continue
                        color = parse_color(entry.get("color"), random.choice(config.word_palette))
                        display = assets.word_cache.get(text_value, color)
                        new_views.append((display, x, y))
                    view_words = new_views

                    status = msg.get("status", status)
                    result = msg.get("result") or result

            if connection.closed and status != "game_over":
                status = "game_over"
                result = {"winner": ROLE_HOST, "reason": "disconnect"}

            message_tuple = (message_text, message_style) if now <= message_until else ("", "neutral")
            overlay_info = feedback.value(now)
            if status == "waiting":
                status_hint: Optional[str] = "서버 준비 대기중..."
            elif connection.closed:
                status_hint = "연결 끊김"
            else:
                status_hint = None

            draw_gameplay_screen(
                assets,
                config,
                view_words,
                buffer,
                message_tuple,
                status_hint,
                total_words,
                stats[player_id],
                stats[other_role],
                "나",
                "상대",
                overlay_info,
                now,
            )

            if status == "game_over":
                running = False

        if result is None:
            result = {"winner": None, "reason": "unknown"}

        show_final_result(
            assets,
            config,
            stats[player_id],
            stats[other_role],
            total_words,
            result,
            player_id,
            "나",
            "상대",
        )
    finally:
        pygame.key.stop_text_input()


def draw_menu_screen(
    assets: PygameAssets,
    config: GameConfig,
    title: str,
    options: List[str],
    selected_index: int,
    subtitle: Optional[str] = None,
    message: Optional[str] = None,
    message_color: Optional[Tuple[int, int, int]] = None,
    footer: Optional[str] = None,
) -> None:
    screen = assets.screen
    screen.blit(assets.gradient_bg, (0, 0))
    assets.pulse_overlay.fill((*config.base_overlay_color, 85))
    screen.blit(assets.pulse_overlay, (0, 0))

    title_surface = assets.font_message.render(title, True, config.title_color)
    screen.blit(title_surface, ((config.width - title_surface.get_width()) // 2, config.height // 6))

    if subtitle:
        subtitle_surface = assets.font_small.render(subtitle, True, config.menu_hint_color)
        screen.blit(subtitle_surface, ((config.width - subtitle_surface.get_width()) // 2, title_surface.get_rect().bottom + 12))

    option_spacing = 68
    start_y = config.height // 2 - option_spacing * len(options) // 2
    box_width = config.width // 2
    box_x = (config.width - box_width) // 2
    for idx, label in enumerate(options):
        rect = pygame.Rect(box_x, start_y + idx * option_spacing, box_width, 52)
        pygame.draw.rect(screen, config.menu_box_color, rect, border_radius=14)
        border_color = config.menu_selected_color if idx == selected_index else config.menu_hint_color
        pygame.draw.rect(screen, border_color, rect, width=3 if idx == selected_index else 1, border_radius=14)
        text_color = config.menu_selected_color if idx == selected_index else config.menu_idle_color
        option_surface = assets.font_ui.render(label, True, text_color)
        screen.blit(option_surface, (rect.centerx - option_surface.get_width() // 2, rect.centery - option_surface.get_height() // 2))

    if message:
        color = message_color or config.message_colors["info"]
        message_surface = assets.font_small.render(message, True, color)
        screen.blit(
            message_surface,
            ((config.width - message_surface.get_width()) // 2, config.height - config.padding * 2),
        )

    if footer:
        footer_surface = assets.font_small.render(footer, True, config.status_color)
        screen.blit(
            footer_surface,
            (config.padding, config.height - footer_surface.get_height() - config.padding // 2),
        )

    pygame.display.flip()


def lobby_loop(assets: PygameAssets, config: GameConfig, clock: "pygame.time.Clock") -> Optional[str]:
    options = ["솔로 모드", "1:1 모드", "게임 종료"]
    selected = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    selected = (selected - 1) % len(options)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    selected = (selected + 1) % len(options)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if selected == 0:
                        return "solo"
                    if selected == 1:
                        return "versus"
                    return "quit"
                elif event.key == pygame.K_ESCAPE:
                    return "quit"

        draw_menu_screen(
            assets,
            config,
            "Typing Game Lobby",
            options,
            selected,
            subtitle="화살표로 선택하고 Enter를 눌러주세요",
            footer="ESC=종료",
        )
        clock.tick(30)


def versus_mode_menu(assets: PygameAssets, config: GameConfig, clock: "pygame.time.Clock") -> Optional[str]:
    options = ["호스트 시작", "클라이언트 접속", "뒤로 가기"]
    selected = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    selected = (selected - 1) % len(options)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    selected = (selected + 1) % len(options)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if selected == 0:
                        return "host"
                    if selected == 1:
                        return "client"
                    return "back"
                elif event.key == pygame.K_ESCAPE:
                    return "back"

        draw_menu_screen(
            assets,
            config,
            "1:1 모드 선택",
            options,
            selected,
            subtitle="호스트는 방을 만들고 클라이언트는 접속합니다",
            footer="ESC=이전 화면",
        )
        clock.tick(30)


def draw_host_wait_screen(
    assets: PygameAssets,
    config: GameConfig,
    host_ip: str,
    port: int,
    message: str,
    highlight: bool,
) -> None:
    screen = assets.screen
    screen.blit(assets.gradient_bg, (0, 0))
    assets.pulse_overlay.fill((*config.base_overlay_color, 100))
    screen.blit(assets.pulse_overlay, (0, 0))

    title = assets.font_message.render("호스트 모드", True, config.title_color)
    screen.blit(title, ((config.width - title.get_width()) // 2, config.height // 6))

    info_lines = [
        f"IP 주소: {host_ip}",
        f"포트 번호: {port}",
    ]
    for idx, text in enumerate(info_lines):
        info_surface = assets.font_ui.render(text, True, config.menu_selected_color)
        screen.blit(
            info_surface,
            ((config.width - info_surface.get_width()) // 2, config.height // 2 - 40 + idx * 48),
        )

    message_color = config.message_colors["info"] if highlight else config.menu_hint_color
    message_surface = assets.font_small.render(message, True, message_color)
    screen.blit(
        message_surface,
        ((config.width - message_surface.get_width()) // 2, config.height // 2 + 80),
    )

    footer = assets.font_small.render("ESC=취소", True, config.status_color)
    screen.blit(footer, (config.padding, config.height - footer.get_height() - config.padding // 2))

    pygame.display.flip()


def host_wait_screen(assets: PygameAssets, config: GameConfig, clock: "pygame.time.Clock") -> Optional[JsonConnection]:
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(("0.0.0.0", 0))
    server_sock.listen(1)
    server_sock.setblocking(False)
    host, port = server_sock.getsockname()
    try:
        display_ip = "127.0.0.1"
        try:
            display_ip = socket.gethostbyname(socket.gethostname()) or display_ip
        except socket.gaierror:
            pass

        waiting = True
        highlight = False
        highlight_timer = 0.0
        while waiting:
            now = time.monotonic()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    server_sock.close()
                    return None
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    waiting = False
                    server_sock.close()
                    return None

            try:
                conn, addr = server_sock.accept()
            except BlockingIOError:
                conn = None

            if conn:
                server_sock.close()
                return JsonConnection(conn)

            if now - highlight_timer > 1.0:
                highlight = not highlight
                highlight_timer = now

            draw_host_wait_screen(
                assets,
                config,
                display_ip,
                port,
                "클라이언트 접속을 기다리는 중...",
                highlight,
            )
            clock.tick(30)
    finally:
        try:
            server_sock.close()
        except OSError:
            pass
    return None


def draw_client_connect_screen(
    assets: PygameAssets,
    config: GameConfig,
    ip_text: str,
    port_text: str,
    active_field: str,
    message: Optional[str],
    message_color: Optional[Tuple[int, int, int]],
) -> None:
    screen = assets.screen
    screen.blit(assets.gradient_bg, (0, 0))
    assets.pulse_overlay.fill((*config.base_overlay_color, 80))
    screen.blit(assets.pulse_overlay, (0, 0))

    title = assets.font_message.render("클라이언트 접속", True, config.title_color)
    screen.blit(title, ((config.width - title.get_width()) // 2, config.height // 6))

    instructions = assets.font_small.render("Tab으로 이동, Enter로 확정, ESC=취소", True, config.menu_hint_color)
    screen.blit(instructions, ((config.width - instructions.get_width()) // 2, title.get_rect().bottom + 12))

    box_width = config.width - config.padding * 2
    box_height = 64
    start_y = config.height // 2 - box_height - 20
    ip_rect = pygame.Rect(config.padding, start_y, box_width, box_height)
    port_rect = pygame.Rect(config.padding, start_y + box_height + 24, box_width, box_height)

    pygame.draw.rect(screen, config.menu_box_color, ip_rect, border_radius=14)
    pygame.draw.rect(screen, config.menu_box_color, port_rect, border_radius=14)

    ip_border_color = config.menu_selected_color if active_field == "ip" else config.menu_hint_color
    port_border_color = config.menu_selected_color if active_field == "port" else config.menu_hint_color
    pygame.draw.rect(screen, ip_border_color, ip_rect, width=3 if active_field == "ip" else 1, border_radius=14)
    pygame.draw.rect(screen, port_border_color, port_rect, width=3 if active_field == "port" else 1, border_radius=14)

    ip_label = assets.font_small.render("서버 IP", True, config.menu_idle_color)
    screen.blit(ip_label, (ip_rect.left + 12, ip_rect.top - ip_label.get_height() - 6))
    port_label = assets.font_small.render("포트 번호", True, config.menu_idle_color)
    screen.blit(port_label, (port_rect.left + 12, port_rect.top - port_label.get_height() - 6))

    ip_value = ip_text if ip_text else "예) 127.0.0.1"
    port_value = port_text if port_text else "예) 6000"
    ip_color = config.menu_selected_color if ip_text else config.menu_hint_color
    port_color = config.menu_selected_color if port_text else config.menu_hint_color

    ip_surface = assets.font_ui.render(ip_value, True, ip_color)
    port_surface = assets.font_ui.render(port_value, True, port_color)
    screen.blit(ip_surface, (ip_rect.left + 18, ip_rect.centery - ip_surface.get_height() // 2))
    screen.blit(port_surface, (port_rect.left + 18, port_rect.centery - port_surface.get_height() // 2))

    if message:
        color = message_color or config.message_colors["info"]
        message_surface = assets.font_small.render(message, True, color)
        screen.blit(
            message_surface,
            ((config.width - message_surface.get_width()) // 2, port_rect.bottom + 40),
        )

    pygame.display.flip()


def client_connect_flow(
    assets: PygameAssets, config: GameConfig, clock: "pygame.time.Clock"
) -> Optional[JsonConnection]:
    pygame.key.start_text_input()
    ip_text = "127.0.0.1"
    port_text = ""
    active_field = "ip"
    message: Optional[str] = None
    message_color: Optional[Tuple[int, int, int]] = None

    try:
        while True:
            connect_attempt = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None
                    if event.key in (pygame.K_TAB, pygame.K_DOWN, pygame.K_UP):
                        active_field = "port" if active_field == "ip" else "ip"
                    elif event.key == pygame.K_BACKSPACE:
                        if active_field == "ip":
                            ip_text = ip_text[:-1]
                        else:
                            port_text = port_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        if active_field == "ip":
                            if ip_text.strip():
                                active_field = "port"
                        else:
                            connect_attempt = True
                elif event.type == pygame.TEXTINPUT:
                    text = event.text
                    if active_field == "ip":
                        if len(ip_text) < 32 and all(ch.isalnum() or ch in (".", "-") for ch in text):
                            ip_text += text
                    else:
                        if len(port_text) < 5 and all(ch.isdigit() for ch in text):
                            port_text += text

            draw_client_connect_screen(assets, config, ip_text, port_text, active_field, message, message_color)
            clock.tick(30)

            if not connect_attempt:
                continue

            port_str = port_text.strip()
            ip_str = ip_text.strip()
            if not ip_str or not port_str:
                message = "IP와 포트를 모두 입력해주세요."
                message_color = config.error_color
                continue

            try:
                port_num = int(port_str)
                if port_num <= 0 or port_num > 65535:
                    raise ValueError
            except ValueError:
                message = "포트 번호가 올바르지 않습니다."
                message_color = config.error_color
                continue

            message = "연결 시도 중..."
            message_color = config.message_colors["info"]
            draw_client_connect_screen(assets, config, ip_text, port_text, active_field, message, message_color)
            pygame.display.flip()

            sock: Optional[socket.socket] = None
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5.0)
                sock.connect((ip_str, port_num))
                sock.settimeout(None)
                connection = JsonConnection(sock)
                sock = None
                return connection
            except OSError as exc:
                message = f"연결 실패: {exc}"
                message_color = config.error_color
            finally:
                if sock is not None:
                    try:
                        sock.close()
                    except Exception:
                        pass
    finally:
        pygame.key.stop_text_input()


def run_application() -> None:
    config = GameConfig()
    pygame.init()
    assets = init_pygame(config)
    clock = pygame.time.Clock()

    running = True
    while running:
        selection = lobby_loop(assets, config, clock)
        if selection in (None, "quit"):
            running = False
            break

        if selection == "solo":
            solo_game(assets, config)
            continue

        if selection == "versus":
            mode = versus_mode_menu(assets, config, clock)
            if mode is None:
                running = False
                break
            if mode == "back":
                continue
            if mode == "host":
                connection = host_wait_screen(assets, config, clock)
                if connection is None:
                    continue
                try:
                    host_game(assets, config, connection)
                finally:
                    connection.close()
                continue
            if mode == "client":
                connection = client_connect_flow(assets, config, clock)
                if connection is None:
                    continue
                try:
                    client_game(assets, config, connection)
                finally:
                    connection.close()
                continue

    pygame.quit()


def main() -> None:
    run_application()


if __name__ == "__main__":
    main()
