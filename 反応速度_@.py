import tkinter as tk
import random
import time

class ReactionTimeApp:
    def __init__(self, master):
        self.master = master
        self.master.title("反応速度テスト")
        self.master.attributes('-fullscreen', True)

        self.clicks = 0
        self.times = []
        self.rankings = []

        self.start_button = tk.Button(self.master, text="スタート", font=("Helvetica", 24), command=self.start_test)
        self.start_button.place(relx=0.5, rely=0.5, anchor="center")

    def start_test(self):
        self.start_button.destroy()
        self.targets_left = 10
        self.start_time = None
        self.display_target()

    def display_target(self):
        if self.targets_left > 0:
            self.targets_left -= 1

            # ランダムな位置に＠ボタンを表示
            x = random.randint(100, self.master.winfo_screenwidth() - 100)
            y = random.randint(100, self.master.winfo_screenheight() - 100)
            self.target_label = tk.Label(self.master, text="@ ", font=("Helvetica", 18))
            self.target_label.place(x=x, y=y)
            self.target_label.bind("<Button-1>", self.end_test)  # ＠ボタンにクリックイベントをバインド

            self.start_time = time.time()
        else:
            self.show_results()

    def end_test(self, event=None):
        if event and self.start_time is not None:
            end_time = time.time()
            reaction_time = end_time - self.start_time
            self.times.append(reaction_time)
            self.target_label.destroy()

            if self.targets_left == 0:  # 最後の＠ボタンをクリックした場合
                self.show_results()  # 結果を表示する
            else:
                self.display_target()  # 次の＠ボタンを表示する

    def show_results(self):
        avg_reaction_time = sum(self.times) / len(self.times)
        self.rankings.append(avg_reaction_time)
        self.rankings.sort()

        result_text = f"今回のチャレンジのタイム: {avg_reaction_time:.3f}秒\n\nランキング:\n"
        for i, time in enumerate(self.rankings):
            result_text += f"{i + 1}: {time:.3f}秒\n"

        if len(self.rankings) > 1 and avg_reaction_time == self.rankings[0]:
            result_text += "\n記録更新！"

        restart_button = tk.Button(self.master, text="リスタート", font=("Helvetica", 24), command=self.restart)
        restart_button.place(relx=0.5, rely=0.9, anchor="center")
        self.show_game_end_button()

        result_label = tk.Label(self.master, text=result_text, font=("Helvetica", 18), justify="left")
        result_label.place(relx=0.5, rely=0.5, anchor="center")

    def show_game_end_button(self):
        game_end_button = tk.Button(self.master, text="ゲーム終了", font=("Helvetica", 24), command=self.game_end)
        game_end_button.place(relx=0.5, rely=0.95, anchor="center")

    def restart(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.start_test()

    def game_end(self):
        self.master.destroy()

def main():
    root = tk.Tk()
    app = ReactionTimeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
