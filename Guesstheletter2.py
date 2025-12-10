import tkinter as tk
from tkinter import messagebox
import random
import os
from datetime import datetime
from PIL import Image, ImageTk
import pygame
from dictionary import EASY_WORDS, MEDIUM_WORDS, HARD_WORDS, LETTER_EMOJI_MAP, FALLBACK_EMOJI, WORD_IMAGES

# ---------------------------
# CONFIG & DATA
# ---------------------------
LEADERBOARD_FILE = "leaderboard.txt"
MAX_LEADERBOARD = 1000
LIVES_PER_WORD = 3
LETTER_TIME_LIMIT = 30  # seconds per letter for medium/hard
PASTEL_BG = "#fff8f0"
SOFT_TEXT = "#3b3b3b"
BUTTON_COLORS = ["#ffb3ba", "#ffdfba", "#ffffba", "#baffc9", "#bae1ff"]
BUTTON_WIDTH = 20
CORRECT_SOUND = "correct.mp3"
WRONG_SOUND = "wrong.mp3"
BG_MUSIC = "background.mp3"

# ---------------------------
# Leaderboard helpers
# ---------------------------
def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return {"Easy": [], "Medium": [], "Hard": []}
    leaderboards = {"Easy": [], "Medium": [], "Hard": []}
    with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(" | ")
            if len(parts) >= 3:
                name, score, mode = parts[:3]
                ts = parts[3] if len(parts) > 3 else ""
                leaderboards[mode].append((name, int(score), mode, ts))
    for mode in leaderboards:
        leaderboards[mode].sort(key=lambda x: x[1], reverse=True)
    return leaderboards

def save_to_leaderboard(name, score, mode):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(LEADERBOARD_FILE, "a", encoding="utf-8") as f:
        f.write(f"{name} | {score} | {mode} | {ts}\n")

# ---------------------------
# SOUND HELPER
# ---------------------------
def play_sound(file):
    try:
        sound = pygame.mixer.Sound(file)
        sound.play()
    except:
        print(f"Cannot play sound: {file}")

# ---------------------------
# GAME CLASS
# ---------------------------
class GuessTheLetterGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Guess The First Letter")
        self.geometry("760x700")
        self.configure(bg=PASTEL_BG)

        # Game state
        self.player_name = ""
        self.mode = "Medium"
        self.words_pool = []
        self.play_list = []
        self.current_word_index = 0
        self.current_letter_index = 0
        self.score = 0
        self.lives = LIVES_PER_WORD
        self.hints_left = 3
        self.word_start_time = None
        self.timer_label = None
        self.timer_job = None   # <-- track scheduled after job so we can cancel/reschedule

        # UI elements
        self.name_entry = None
        self.mode_var = tk.StringVar(value="Medium")
        self.header_frame = None
        self.info_label = None
        self.lives_frame = None
        self.game_frame = None
        self.word_label = None
        self.emoji_label = None
        self.hint_label = None   # <-- NEW: label for showing hint text (between emoji & choices)
        self.word_image_label = None
        self.buttons_frame = None
        self.next_button = None
        self.hint_button = None
        self.entry_field = None
        self.footer_frame = None

        # Images cache
        self.word_images = {}
        self.preload_word_images()

        # Initialize pygame
        pygame.mixer.init()
        try:
            pygame.mixer.music.load(BG_MUSIC)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
        except:
            print("Background music file not found or error.")

        self.setup_start_screen()

    # ---------------------------
    # Preload word images
    # ---------------------------
    def preload_word_images(self):
        for word, image_path in WORD_IMAGES.items():
            if os.path.exists(image_path):
                try:
                    img = Image.open(image_path)
                    self.word_images[word.lower()] = img
                except Exception as e:
                    print(f"Failed to load {image_path}: {e}")

    # ---------------------------
    # START SCREEN
    # ---------------------------
    def setup_start_screen(self):
        for w in self.winfo_children():
            w.destroy()
        box = tk.Frame(self, bg=PASTEL_BG)
        box.pack(pady=30)

        tk.Label(box, text="Guess The First Letter", font=("Montserrat", 28, "bold"), fg=SOFT_TEXT, bg=PASTEL_BG).pack(pady=(0, 10))
        tk.Label(box, text="Enter a nickname and choose a mode", font=("Helvetica", 12), fg=SOFT_TEXT, bg=PASTEL_BG).pack(pady=(0, 18))

        name_frame = tk.Frame(box, bg=PASTEL_BG)
        name_frame.pack(pady=8)
        tk.Label(name_frame, text="Nickname: ", bg=PASTEL_BG, fg=SOFT_TEXT, font=("Helvetica", 12)).pack(side="left")
        self.name_entry = tk.Entry(name_frame, font=("Helvetica", 12), width=20)
        self.name_entry.pack(side="left", padx=8)

        mode_frame = tk.Frame(box, bg=PASTEL_BG)
        mode_frame.pack(pady=12)
        tk.Label(mode_frame, text="Mode:", bg=PASTEL_BG, fg=SOFT_TEXT, font=("Helvetica", 12)).pack(side="left")
        for m in ("Easy", "Medium", "Hard"):
            rb = tk.Radiobutton(mode_frame, text=m, variable=self.mode_var, value=m, bg=PASTEL_BG, fg=SOFT_TEXT, selectcolor=PASTEL_BG, font=("Helvetica", 11))
            rb.pack(side="left", padx=6)

        # Buttons (uniform size)
        btn_font = ("Helvetica", 14, "bold")
        tk.Button(box, text="Start Game", command=self.start_game, font=btn_font, bg=BUTTON_COLORS[0], fg=SOFT_TEXT, width=BUTTON_WIDTH).pack(pady=6)
        tk.Button(box, text="Instructions", command=self.show_instructions, font=btn_font, bg=BUTTON_COLORS[1], fg=SOFT_TEXT, width=BUTTON_WIDTH).pack(pady=6)
        tk.Button(box, text="Show Leaderboard", command=self.show_leaderboard, font=btn_font, bg=BUTTON_COLORS[2], fg=SOFT_TEXT, width=BUTTON_WIDTH).pack(pady=6)
        tk.Button(box, text="Quit", command=self.destroy, font=btn_font, bg=BUTTON_COLORS[3], fg=SOFT_TEXT, width=BUTTON_WIDTH).pack(pady=6)

    # ---------------------------
    # START GAME
    # ---------------------------
    def start_game(self):
        name = self.name_entry.get().strip()
        if not name.isalpha():
            messagebox.showinfo("Invalid nickname", "Nickname must contain letters only!")
            return
        self.player_name = name
        self.mode = self.mode_var.get()
        if self.mode == "Easy":
            self.words_pool = EASY_WORDS.copy()
        elif self.mode == "Medium":
            self.words_pool = MEDIUM_WORDS.copy()
        else:
            self.words_pool = HARD_WORDS.copy()
        self.play_list = random.sample(self.words_pool, 10)  # Random 10 words
        self.current_word_index = 0
        self.current_letter_index = 0
        self.score = 0
        self.lives = LIVES_PER_WORD
        self.hints_left = 3
        self.timer_job = None
        self.setup_game_ui()

    # ---------------------------
    # GAME UI
    # ---------------------------
    def setup_game_ui(self):
        for w in self.winfo_children():
            w.destroy()

        self.header_frame = tk.Frame(self, bg=PASTEL_BG)
        self.header_frame.pack(fill="x", pady=10)
        self.info_label = tk.Label(self.header_frame, text=self._info_text(), bg=PASTEL_BG, fg=SOFT_TEXT, font=("Helvetica", 12))
        self.info_label.pack(side="left", padx=16)
        self.lives_frame = tk.Frame(self.header_frame, bg=PASTEL_BG)
        self.lives_frame.pack(side="right", padx=16)
        self.update_lives_display()

        if self.mode in ["Medium", "Hard"]:
            self.timer_label = tk.Label(self.header_frame, text="", bg=PASTEL_BG, fg="orange", font=("Helvetica", 14, "bold"))
            self.timer_label.pack(side="right", padx=(0, 16))

        self.game_frame = tk.Frame(self, bg=PASTEL_BG)
        self.game_frame.pack(pady=8, fill="both", expand=True)
        self.word_label = tk.Label(self.game_frame, text=self._word_display(), bg=PASTEL_BG, fg=SOFT_TEXT, font=("Montserrat", 32, "bold"))
        self.word_label.pack(pady=14)

        emoji_frame = tk.Frame(self.game_frame, bg="#ffffff", bd=2, relief="groove")
        emoji_frame.pack(pady=6)
        emoji_frame.configure(width=300, height=180)
        emoji_frame.pack_propagate(False)

        self.emoji_label = tk.Label(emoji_frame, text="", font=("Segoe UI Emoji", 64), bg="#ffffff")
        self.emoji_label.place(relx=0.5, rely=0.5, anchor="center")

        # NEW: hint label (between emoji and choices)
        self.hint_label = tk.Label(self.game_frame, text="", bg=PASTEL_BG, fg=SOFT_TEXT, font=("Helvetica", 12))
        self.hint_label.pack(pady=(6, 0))

        self.buttons_frame = tk.Frame(self.game_frame, bg=PASTEL_BG)
        self.buttons_frame.pack(pady=6)

        entry_frame = tk.Frame(self.game_frame, bg=PASTEL_BG)
        entry_frame.pack(pady=10)
        self.entry_field = tk.Entry(entry_frame, font=("Helvetica", 16), width=15, justify="center")
        self.entry_field.pack(pady=5)
        self.entry_field.bind("<Return>", lambda e: self.check_entry_guess())
        tk.Label(entry_frame, text="Type letter or full word", bg=PASTEL_BG, fg=SOFT_TEXT, font=("Helvetica", 10)).pack()

        hint_frame = tk.Frame(self.game_frame, bg=PASTEL_BG)
        hint_frame.pack(pady=5)
        self.hint_button = tk.Button(hint_frame, text=f"Hint ({self.hints_left} left)", command=self.use_hint, font=("Helvetica", 11), bg="#fff3cd", fg=SOFT_TEXT, width=12)
        self.hint_button.pack()

        self.next_button = tk.Button(self.game_frame, text="Skip", command=self.skip_word, font=("Helvetica", 12, "bold"), bg=BUTTON_COLORS[3], fg=SOFT_TEXT, width=12)
        self.next_button.pack(pady=10)

        self.footer_frame = tk.Frame(self, bg=PASTEL_BG)
        self.footer_frame.pack(side="bottom", pady=10)
        tk.Button(self.footer_frame, text="Quit to Menu", command=self.setup_start_screen, bg=BUTTON_COLORS[4], fg=SOFT_TEXT, width=BUTTON_WIDTH).pack(side="left", padx=8)
        tk.Button(self.footer_frame, text="Show Leaderboard", command=self.show_leaderboard, bg=BUTTON_COLORS[1], fg=SOFT_TEXT, width=BUTTON_WIDTH).pack(side="left", padx=8)

        self.load_round_ui()

    # ---------------------------
    # HELPERS
    # ---------------------------
    def _info_text(self):
        return f"Player: {self.player_name}   |   Score: {self.score}   |   Word: {self.current_word_index+1}/{len(self.play_list)}"

    def current_word(self):
        if 0 <= self.current_word_index < len(self.play_list):
            return self.play_list[self.current_word_index].upper()
        return None

    def _word_display(self):
        w = self.current_word()
        if not w:
            return ""
        displayed = [ch if i < self.current_letter_index else "_" for i, ch in enumerate(w)]
        return " ".join(displayed)

    def letter_for_current(self):
        w = self.current_word()
        if w and self.current_letter_index < len(w):
            return w[self.current_letter_index]
        return None

    def emoji_for_letter(self, letter):
        if not letter:
            return FALLBACK_EMOJI
        letter = letter.upper()
        return random.choice(LETTER_EMOJI_MAP.get(letter, [FALLBACK_EMOJI]))

    # ---------------------------
    # TIMER (with job management)
    # ---------------------------
    def cancel_timer_job(self):
        if self.timer_job is not None:
            try:
                self.after_cancel(self.timer_job)
            except Exception:
                pass
            self.timer_job = None

    def update_timer(self):
        # Called every second when active; stores job id in self.timer_job
        if not (self.mode in ["Medium", "Hard"] and self.word_start_time):
            return
        elapsed = (datetime.now() - self.word_start_time).total_seconds()
        remaining = max(0, LETTER_TIME_LIMIT - elapsed)
        mins, secs = divmod(int(remaining), 60)
        if self.timer_label:
            self.timer_label.config(text=f"⏰ {mins:01d}:{secs:02d}")

        if remaining <= 0:
            # time ran out for this letter -> penalize and advance
            self.lives -= 1
            self.update_lives_display()
            play_sound(WRONG_SOUND)
            if self.lives <= 0:
                self.cancel_timer_job()
                self.game_over()
                return
            # advance letter (skip this letter)
            self.current_letter_index += 1
            if self.current_letter_index >= len(self.current_word()):
                # completed by timeout -> go next word
                self.cancel_timer_job()
                self.after(300, self.next_word)
                return
            # else reset timer and refresh UI for new letter
            self.word_start_time = datetime.now()
            self.load_round_ui()  # load_round_ui will restart timer
            return

        # schedule next tick
        self.timer_job = self.after(1000, self.update_timer)

    # ---------------------------
    # ROUND LOGIC
    # ---------------------------
    def build_option_buttons(self, correct_letter):
        # build buttons for the current letter
        for w in self.buttons_frame.winfo_children():
            w.destroy()
        options = [correct_letter.upper()]
        while len(options) < 4:
            cand = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            if cand not in options:
                options.append(cand)
        random.shuffle(options)

        for idx, opt in enumerate(options):
            color = BUTTON_COLORS[idx % len(BUTTON_COLORS)]
            btn = tk.Button(self.buttons_frame, text=opt, width=6, height=2, font=("Helvetica", 16, "bold"),
                            bg=color, fg=SOFT_TEXT, command=lambda c=opt: self.check_guess(c))
            btn.pack(side="left", padx=8, pady=6)

    def update_lives_display(self):
        for w in self.lives_frame.winfo_children():
            w.destroy()
        for i in range(LIVES_PER_WORD):
            heart = "❤️" if i < self.lives else "💔"
            tk.Label(self.lives_frame, text=heart, font=("Helvetica", 24), bg=PASTEL_BG, fg="red").pack(side="left", padx=2)

    def load_round_ui(self):
        # cancel any existing timer job before loading new UI
        self.cancel_timer_job()

        if self.current_word_index >= len(self.play_list):
            self.game_over()
            return

        # reset hint label (do not overwrite player info)
        self.hint_label.config(text="")

        self.word_label.config(text=self._word_display())
        letter = self.letter_for_current()
        # update emoji to correspond to current letter
        self.emoji_label.config(text=self.emoji_for_letter(letter))
        # build option buttons for current letter
        self.build_option_buttons(letter if letter else "?")
        self.update_lives_display()
        self.info_label.config(text=self._info_text())

        # start / reset timer for the letter
        self.word_start_time = datetime.now()
        if self.mode in ["Medium", "Hard"]:
            # ensure timer job is started
            self.cancel_timer_job()
            self.update_timer()

        # hints reset per word (3 per word)
        self.hints_left = 3
        self.hint_button.config(text=f"Hint ({self.hints_left} left)")

    # ---------------------------
    # GUESS LOGIC
    # ---------------------------
    def _advance_after_correct(self):
        """Advance to next letter/word after a correct guess."""
        # cancel current timer job (we'll restart it if needed)
        self.cancel_timer_job()

        self.current_letter_index += 1
        self.score += 0  # score increment handled where necessary (your existing logic adds 1)
        if self.current_letter_index >= len(self.current_word()):
            # finished word -> go to next word automatically
            self.after(300, self.next_word)
            return
        # not finished -> update display for next letter
        self.word_label.config(text=self._word_display())
        # update emoji for the new current letter
        letter = self.letter_for_current()
        self.emoji_label.config(text=self.emoji_for_letter(letter))
        # rebuild choice buttons for new letter
        self.build_option_buttons(letter if letter else "?")
        # restart timer for new letter
        self.word_start_time = datetime.now()
        if self.mode in ["Medium", "Hard"]:
            self.cancel_timer_job()
            self.update_timer()

    def check_guess(self, choice_letter):
        correct = self.letter_for_current()
        if correct is None:
            return
        if choice_letter.upper() == correct.upper():
            play_sound(CORRECT_SOUND)
            # give score per correct letter (keeps your previous +1 behavior)
            self.score += 1
            # use helper to advance safely (updates emoji, buttons, timer)
            self._advance_after_correct()
            # update info text after scoring
            self.info_label.config(text=self._info_text())
        else:
            self.lives -= 1
            self.update_lives_display()
            play_sound(WRONG_SOUND)
            if self.lives <= 0:
                self.cancel_timer_job()
                self.game_over()

    def check_entry_guess(self):
        guess = self.entry_field.get().strip().upper()
        self.entry_field.delete(0, tk.END)
        if not guess.isalpha():
            return
        if len(guess) == 1:
            self.check_guess(guess)
            return
        # full word guess: calculate per-letter deduction as before
        word = self.current_word()
        # normalize both to upper
        word_u = word.upper()
        wrong_count = 0
        for i, ch in enumerate(word_u):
            if i >= len(guess) or guess[i] != ch:
                wrong_count += 1
        # deduct for wrong letters
        self.score = max(0, self.score - wrong_count)
        # if fully correct, award remaining letters
        if guess == word_u:
            # award letters not yet guessed
            gained = len(word_u) - self.current_letter_index
            if gained > 0:
                self.score += gained
            # mark as finished and go next
            self.cancel_timer_job()
            self.after(300, self.next_word)
            return
        else:
            # wrong full guess penalizes a life too
            self.lives -= 1
            self.update_lives_display()
            play_sound(WRONG_SOUND)
            if self.lives <= 0:
                self.cancel_timer_job()
                self.game_over()
                return
            # if still alive, continue on same letter (timer continues)
            # update info label but do NOT overwrite player name - place message in hint label
            self.hint_label.config(text=f"Wrong guess (-{wrong_count})")
            # no automatic advance here

    # ---------------------------
    # HINT
    # ---------------------------
    def use_hint(self):
        if self.hints_left <= 0:
            return
        self.hints_left -= 1
        letter = self.letter_for_current()
        # show hint between emoji and choices
        self.hint_label.config(text=f"Hint: {letter}")
        self.hint_button.config(text=f"Hint ({self.hints_left} left)")

    # ---------------------------
    # SKIP
    # ---------------------------
    def skip_word(self):
        # skipping simply advances to the next word (skipped words do not return)
        self.cancel_timer_job()
        self.after(200, self.next_word)

    def next_word(self):
        # move to next word; reset letter index and UI
        self.current_word_index += 1
        self.current_letter_index = 0
        # cancel any timer job before loading
        self.cancel_timer_job()
        self.load_round_ui()

    # ---------------------------
    # GAME OVER
    # ---------------------------
    def game_over(self):
        save_to_leaderboard(self.player_name, self.score, self.mode)
        lb = load_leaderboard()
        lb_mode = lb[self.mode][:5]
        lb_text = "\n".join([f"{i + 1}. {e[0]} - {e[1]}pts" for i, e in enumerate(lb_mode)]) if lb_mode else "No scores yet"
        messagebox.showinfo("Game Over", f"Player: {self.player_name}\nScore: {self.score}\nMode: {self.mode}\n\nTop Scores:\n{lb_text}")
        self.setup_start_screen()

    # ---------------------------
    # INSTRUCTIONS & LEADERBOARD
    # ---------------------------
    def show_instructions(self):
        instructions = """How to play:
• Guess FIRST LETTER of the word each emoji stands for.
• 4 letter options OR you can type full word.
• 3 hearts PER GAME.
• Medium/Hard: 30 sec per letter.
• 3 Hints per word available.
• Skip words (they won't return).
• Game over when 0 hearts."""
        messagebox.showinfo("Instructions", instructions)

    def show_leaderboard(self):
        lb = load_leaderboard()
        text = ""
        for mode in ["Easy", "Medium", "Hard"]:
            text += f"{mode} Top 5:\n"
            mode_lb = lb[mode][:5]
            if mode_lb:
                text += "\n".join([f"{i + 1}. {e[0]} - {e[1]}pts" for i, e in enumerate(mode_lb)])
            else:
                text += "No scores yet"
            text += "\n" + "="*30 + "\n"
        top = tk.Toplevel(self)
        top.title("Leaderboards")
        top.configure(bg=PASTEL_BG)
        top.geometry("500x600")
        tk.Label(top, text="All Mode Leaderboards", font=("Helvetica", 16, "bold"), bg=PASTEL_BG, fg=SOFT_TEXT).pack(pady=8)
        tk.Label(top, text=text, font=("Helvetica", 11), bg=PASTEL_BG, fg=SOFT_TEXT, justify="left").pack(padx=12, pady=8)
        tk.Button(top, text="Close", command=top.destroy, bg=BUTTON_COLORS[0], fg=SOFT_TEXT, width=BUTTON_WIDTH).pack(pady=8)


# ---------------------------
# RUN
# ---------------------------
if __name__ == "__main__":
    app = GuessTheLetterGame()
    app.mainloop()
