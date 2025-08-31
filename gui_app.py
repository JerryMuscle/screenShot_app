import os
from datetime import datetime as dt
import tkinter as tk
import threading
from tkinter import messagebox, filedialog
from service.capture import capture_start

save_dir = None  # 保存先ディレクトリをグローバルで保持

def select_directory():
    global save_dir
    dir_selected = filedialog.askdirectory()
    if dir_selected:
        save_dir = dir_selected
        dir_label.config(text=f"保存先: {save_dir}")

def on_start():
    try:
        interval = float(interval_entry.get())
        duration = float(duration_entry.get())
    except ValueError:
        messagebox.showerror("エラー", "数値を正しく入力してください")
        return
    
    try:
        # マウスの場所でスクショの範囲内を決める-------
        # position = screenshot_position()
        # print(position)
        # x1, y1, x2, y2 = position
        # --------------------------------------

        # 手動で設定する(mac画面全体)
        x1, y1, x2, y2 =0, 0, 1400, 900 

        if not interval:
            interval = 2
        elif interval < 1:
            interval = 1
        
        # 保存先ディレクトリの設定
        if not save_dir:
            dir_path = dt.now().strftime('%y%m%d_%H%M')
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
        else:
            dir_path = save_dir

        # 開始時にボタンを無効化
        capture_btn.config(state=tk.DISABLED)
        select_btn.config(state=tk.DISABLED)

        # ステータス更新
        status_label.config(text="ステータス: スクリーンショットを実施しています")

        # スクショ処理
        threading.Thread(target=capture_start, args=(interval, duration, dir_path, x1, y1, x2, y2, on_capture_finished)).start()
    except Exception as e:
        messagebox.showerror("エラー", f"キャプチャ中にエラーが発生しました:\n{e}")
        # 失敗時はボタンを再度有効化
        capture_btn.config(state=tk.NORMAL)
        select_btn.config(state=tk.NORMAL)
        status_label.config(text="ステータス: 待機中")

def on_capture_finished():
    # GUIスレッドで安全に表示するため after() を使う
    def finish_ui():
        global save_dir
        messagebox.showinfo("完了", "スクリーンショットが完了しました")
        capture_btn.config(state=tk.NORMAL)  # ボタンを再度有効化
        select_btn.config(state=tk.NORMAL)

        status_label.config(text="ステータス: 待機中") # ステータスを待機中に戻す
        # 保存先を未選択状態に戻す
        save_dir = None
        dir_label.config(text="保存先: 未選択")

    root.after(0, finish_ui)
    
root = tk.Tk()
root.title("スクショキャプチャ")
root.geometry("500x270")

# ステータス表示ラベル
status_label = tk.Label(root, text="ステータス: 待機中", fg="blue")
status_label.pack(pady=10)

tk.Label(root, text="撮影間隔（秒）").pack()
interval_entry = tk.Entry(root)
interval_entry.insert(0, "2")
interval_entry.pack()

tk.Label(root, text="実行時間（秒）").pack()
duration_entry = tk.Entry(root)
duration_entry.insert(0, "10")
duration_entry.pack()

# 保存先指定ボタン
select_btn = tk.Button(root, text="保存先を選択", command=select_directory)
select_btn.pack(pady=5)

dir_label = tk.Label(root, text="保存先: 未指定")
dir_label.pack()

capture_btn = tk.Button(root, text="キャプチャ開始", command=on_start)
capture_btn.pack(pady=10)

root.mainloop()