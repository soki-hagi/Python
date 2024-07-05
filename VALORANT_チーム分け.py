import tkinter as tk
from tkinter import messagebox
import random

# ランクと対応する記号の辞書
RANK_SYMBOLS = {
    "アイアン": "IA",
    "ブロンズ": "B",
    "シルバー": "S",
    "ゴールド": "G",
    "プラチナ": "P",
    "ダイヤ": "D",
    "アセンダント": "A",
    "イモータル": "I",
    "レディアント": "☆"
}

# ランクごとのポイント
RANK_POINTS = {
    "IA3": 1, "IA2": 2, "IA1": 3,
    "B3": 5, "B2": 6, "B1": 7,
    "S3": 9, "S2": 10, "S1": 11,
    "G3": 13, "G2": 14, "G1": 15,
    "P3": 17, "P2": 18, "P1": 19,
    "D3": 21, "D2": 22, "D1": 23,
    "A3": 25, "A2": 26, "A1": 27,
    "I3": 29, "I2": 30, "I1": 31,
    "☆": 35
}

class TeamDividerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("チーム分けアプリ")

        self.player_names = []
        self.player_points = []
        self.team1_names = []
        self.team2_names = []

        self.player_label = tk.Label(master, text="プレイヤー名:")
        self.player_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.player_entry = tk.Entry(master)
        self.player_entry.grid(row=0, column=1, padx=10, pady=10)

        # ランク選択のチェックリスト
        self.rank_frame = tk.Frame(master)
        self.rank_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.ranks = {}
        for rank in RANK_SYMBOLS:
            var = tk.IntVar()
            self.ranks[rank] = var
            checkbox = tk.Checkbutton(self.rank_frame, text=rank, variable=var)
            checkbox.pack(anchor="w")

        # ランクの数字選択のチェックリスト
        self.rank_number_frame = tk.Frame(master)
        self.rank_number_frame.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.rank_numbers = {}
        for number in range(3, 0, -1):
            var = tk.IntVar()
            self.rank_numbers[number] = var
            checkbox = tk.Checkbutton(self.rank_number_frame, text=str(number), variable=var)
            checkbox.pack(anchor="w")

        # プレイヤー登録ボタン
        self.register_button = tk.Button(master, text="登録", command=self.register_player)
        self.register_button.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

        # シャッフルボタン
        self.shuffle_button = tk.Button(master, text="シャッフル", command=self.shuffle_teams)
        self.shuffle_button.grid(row=3, column=0, padx=10, pady=10, columnspan=2)

        self.team1_label = tk.Label(master, text="チーム1:")
        self.team1_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")

        self.team1_display = tk.Label(master, text="")
        self.team1_display.grid(row=4, column=1, padx=10, pady=10)

        self.team2_label = tk.Label(master, text="チーム2:")
        self.team2_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")

        self.team2_display = tk.Label(master, text="")
        self.team2_display.grid(row=5, column=1, padx=10, pady=10)

    def register_player(self):
        player_name = self.player_entry.get().strip()
        if player_name:
            if player_name not in self.player_names:
                # チェックされたランクと対応する数字を取得
                selected_ranks = [rank for rank, var in self.ranks.items() if var.get()]
                selected_numbers = [number for number, var in self.rank_numbers.items() if var.get()]

                # ランクが複数選択された場合はエラーメッセージを表示
                if len(selected_ranks) > 1:
                    messagebox.showerror("エラー", "複数のランクを選択できません。")
                    return

                # ランクが選択されていない場合はデフォルトの☆を設定
                rank_symbol = RANK_SYMBOLS[selected_ranks[0]] if selected_ranks else "☆"

                # レディアントが選択された場合は数字をチェックしていなくても35点
                if "レディアント" in selected_ranks:
                    player_points = 35
                    player_name += " (☆)"
                # ランクが選択されている場合は対応するポイントを計算
                elif selected_ranks:
                    rank_key = f"{rank_symbol}{selected_numbers[0]}"
                    player_points = RANK_POINTS[rank_key]
                    player_name += " ({}{})".format(rank_symbol, selected_numbers[0])
                else:
                    player_points = 0  # ランクが設定されていない場合はポイントを0とする

                self.player_names.append(player_name)
                self.player_points.append(player_points)
                self.player_entry.delete(0, tk.END)

                # ランクと数字のチェックを外す
                for var in self.ranks.values():
                    var.set(0)
                for var in self.rank_numbers.values():
                    var.set(0)

                self.divide_teams()
            else:
                messagebox.showerror("エラー", "この名前は既に登録されています。")
        else:
            messagebox.showerror("エラー", "プレイヤー名を入力してください。")

    def divide_teams(self):
        if not self.player_names:
            return

        # プレイヤーをポイント順に並び替えてから振り分ける
        players = list(zip(self.player_names, self.player_points))
        players.sort(key=lambda x: x[1], reverse=True)

        team1, team2 = [], []
        total1, total2 = 0, 0

        # 10人の場合は各チーム5人に分けるが、スコアが近くなるように分ける
        if len(players) == 10:
            sorted_players = sorted(players, key=lambda x: x[1], reverse=True)
            team1 = [name for name, _ in sorted_players[:5]]
            team2 = [name for name, _ in sorted_players[5:]]
            total1 = sum(points for _, points in sorted_players[:5])
            total2 = sum(points for _, points in sorted_players[5:])
            
            # チームのスコアをなるべく近づけるための最適化
            for i in range(5):
                for j in range(5):
                    new_total1 = total1 - sorted_players[i][1] + sorted_players[5 + j][1]
                    new_total2 = total2 - sorted_players[5 + j][1] + sorted_players[i][1]
                    if abs(new_total1 - new_total2) < abs(total1 - total2):
                        # スコアが改善される場合はメンバーを交換
                        team1[i], team2[j] = team2[j], team1[i]
                        total1, total2 = new_total1, new_total2

        else:
            # ポイントの合計が最も近くなるように振り分け
            for name, points in players:
                if total1 <= total2:
                    team1.append(name)
                    total1 += points
                else:
                    team2.append(name)
                    total2 += points

        self.team1_names = team1
        self.team2_names = team2
        self.display_teams()

    def display_teams(self):
        team1_text = "\n".join(self.team1_names)
        team2_text = "\n".join(self.team2_names)
        self.team1_display.config(text=team1_text)
        self.team2_display.config(text=team2_text)

    def shuffle_teams(self):
        random.shuffle(self.player_names)
        self.divide_teams()

def main():
    root = tk.Tk()
    app = TeamDividerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
