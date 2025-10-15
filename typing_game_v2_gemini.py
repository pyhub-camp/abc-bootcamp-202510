import curses
import random
import time


# --- ��� ���� ---
WORDS = [
    "apple",
    "river",
    "candle",
    "mountain",
    "window",
    "guitar",
    "orange",
    "planet",
    "forest",
    "summer",
    "python",
    "coding",
]
STAGE_WORD_COUNT = 10  # ���������� �ܾ� ��


def main(stdscr):
    # --- curses �ʱ� ���� ---
    curses.curs_set(0)
    curses.noecho()
    stdscr.nodelay(True)

    # ȭ���� ���̿� �ʺ� ��������
    height, width = stdscr.getmaxyx()

    # --- ���� �� �ʱ�ȭ ---
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    # --- �� �κ� ���� ---
    play_height = max(1, height - 2)
    play_width = width
    status_win = curses.newwin(1, width, 0, 0)
    play_win = curses.newwin(play_height, play_width, 1, 0)
    input_win = curses.newwin(1, width, height - 1, 0)
    input_win.bkgd(" ", curses.A_REVERSE)

    # --- ���� ���� �ʱ�ȭ ---
    score = 0
    missed = 0
    words_spawned = 0
    active_words = []
    current_input = ""
    start_time = time.time()

    # --- ���� ���� ---
    while words_spawned < STAGE_WORD_COUNT or active_words:
        status_win.erase()
        play_win.erase()
        input_win.erase()
        input_win.bkgd(" ", curses.A_REVERSE)

        # --- �� �ܾ� ���� ---
        if (
            words_spawned < STAGE_WORD_COUNT
            and len(active_words) < 5
            and random.random() < 0.02
        ):
            text = random.choice(WORDS)
            max_x = max(0, play_width - len(text))
            x = random.randint(0, max_x) if max_x > 0 else 0
            speed = random.uniform(0.1, 0.3)
            active_words.append({"text": text, "x": x, "y": 0.0, "speed": speed})
            words_spawned += 1

        # --- ����� �Է� ó�� ---
        try:
            key = stdscr.getkey()
            if key == "\n":
                for word in active_words[:]:
                    if current_input == word["text"]:
                        active_words.remove(word)
                        score += 1
                        break
                current_input = ""
            elif key in ("\b", curses.KEY_BACKSPACE):
                current_input = current_input[:-1]
            elif len(key) == 1 and key.isprintable():
                current_input += key
        except curses.error:
            pass

        # --- �ܾ� ��ġ ������Ʈ �� �׸��� ---
        for word in active_words[:]:
            word["y"] += word["speed"]
            if word["y"] >= play_height - 1:
                active_words.remove(word)
                missed += 1
                continue

            row = int(word["y"])
            row = max(0, min(row, play_height - 1))
            play_win.addstr(row, word["x"], word["text"], curses.color_pair(1))

        # --- �ϴ� UI �׸��� ---
        status_text = (
            f"Score: {score} | Missed: {missed} | Stage Words: {words_spawned}/{STAGE_WORD_COUNT}"
        )
        status_win.addnstr(0, 0, status_text, width - 1)

        prompt = f">> {current_input}"
        input_win.addnstr(0, 0, prompt, width - 1, curses.A_REVERSE)

        # --- ȭ�� ���ΰ�ħ ---
        status_win.noutrefresh()
        play_win.noutrefresh()
        input_win.noutrefresh()
        curses.doupdate()

        # --- ���� ���� �ӵ� ���� ---
        time.sleep(0.1)

        if missed >= STAGE_WORD_COUNT:
            break

    # --- ���� ���� �� ��� ǥ�� ---
    elapsed_time = time.time() - start_time
    wpm = (score / elapsed_time * 60) if elapsed_time > 0 else 0

    stdscr.nodelay(False)
    stdscr.clear()
    result_text = "== Game Over ==" if missed >= STAGE_WORD_COUNT else "== Stage Clear!"
    score_text = f"Score: {score}"
    missed_text = f"Missed: {missed}"
    wpm_text = f"WPM: {wpm:.2f}"

    stdscr.addstr(height // 2 - 2, max(0, (width - len(result_text)) // 2), result_text)
    stdscr.addstr(height // 2 - 1, max(0, (width - len(score_text)) // 2), score_text)
    stdscr.addstr(height // 2, max(0, (width - len(missed_text)) // 2), missed_text)
    stdscr.addstr(height // 2 + 1, max(0, (width - len(wpm_text)) // 2), wpm_text)
    stdscr.addstr(height - 2, max(0, (width - 25) // 2), "Press any key to exit...")
    stdscr.refresh()
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)
