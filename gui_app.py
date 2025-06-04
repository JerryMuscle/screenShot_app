import os
from datetime import datetime as dt
import tkinter as tk
import threading
from tkinter import messagebox
from service.capture import capture_start, screenshot_position

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
        
        # スクショしたものを保存するファイルの設定
        dir_path = dt.now().strftime('%y%m%d_%H%M')
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        # スクショ処理
        threading.Thread(target=capture_start, args=(interval, duration, dir_path, x1, y1, x2, y2, on_capture_finished)).start()
    except Exception as e:
        messagebox.showerror("エラー", f"キャプチャ中にエラーが発生しました:\n{e}")

def on_capture_finished():
    # GUIスレッドで安全に表示するため after() を使う
    root.after(0, lambda: messagebox.showinfo("完了", "スクリーンショットが完了しました"))
    
root = tk.Tk()
root.title("スクショキャプチャ")
root.geometry("300x180")

tk.Label(root, text="撮影間隔（秒）").pack()
interval_entry = tk.Entry(root)
interval_entry.insert(0, "2")
interval_entry.pack()

tk.Label(root, text="実行時間（秒）").pack()
duration_entry = tk.Entry(root)
duration_entry.insert(0, "10")
duration_entry.pack()

tk.Button(root, text="キャプチャ開始", command=on_start).pack(pady=10)

root.mainloop()