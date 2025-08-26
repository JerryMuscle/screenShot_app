import cv2
import time
import pyautogui
import numpy as np
from PIL import ImageGrab
from datetime import datetime as dt


# 実際にスクショを実施する処理：キーボード入力があったら停止
def capture_start(interval_time, finish_time, dir_path, x1, y1, x2, y2, on_finish=None):
    """スクショ処理
    
    Args:
        interval_time: スクショ間隔時間
        finish_time: スクショ終了時間
        dir_path: 保存するパス
        x1, y1, x2, y2: スクショする画面の座標
        on_fiish: 終了後の処理の有無
    """
    
    start_time = time.time()
    next_time = start_time
    print(f'スクショ間隔時間:{interval_time}')
    print(f'終了時間:{finish_time}')
    print('\n■■キャプチャ開始■■\n')

    try:
        while True:
            now = time.time()
            if now > next_time:
                
                # 座標をもとにスクショを撮る
                img = ImageGrab.grab(bbox=(x1, y1, x2, y2), all_screens=True)
                img_now = np.array(img)

                # 背景差分法を使った前の画像との比較
                if 'img_before' in locals():
                    backSub = cv2.createBackgroundSubtractorMOG2()
                    fgmask = backSub.apply(img_before)
                    fgmask = backSub.apply(img_now)
                    # 閾値を設定(default: 0.5)
                    if np.count_nonzero(fgmask) / fgmask.size * 100 < 0.5:
                        if time.time() - start_time >= finish_time:
                            print('\n■■キャプチャ終了■■')
                            break
                        continue
                print(f'経過時間：{time.time() - start_time}')
                # 画像のファイル名の設定
                img.save(f'{dir_path}/{dt.now().strftime("%d%H%M%S")}.png')
                img_before = img_now

                # 次に撮る時間を更新
                next_time += interval_time

                if now - start_time >= finish_time:
                    break
            time.sleep(0.1)

    except KeyboardInterrupt:
        # 処理待ち時間の問題でうまくいかん
        print('\n■■キャプチャ終了■■')
        print("なぜかできないよおおおお")
    finally:
        print('\n■■キャプチャ終了■■')
        if on_finish:
            on_finish()


# スクリーンショットをする範囲を指定(現在は未使用)
def screenshot_position():

    def position_get():
        # マウスカーソルの位置を取得し、座標を返す
        return pyautogui.position()

    input('取得したい箇所の"左上"にカーソルを当てEnterキー押してください')
    x1, y1 = position_get()
    print(f'X:{str(x1)}, Y:{str(y1)}')
    input('取得したい箇所の"右下"にカーソルを当てEnterキー押してください')
    x2, y2 = position_get()
    print(f'X:{str(x2)}, Y:{str(y2)}')

    # text fileにスクショする範囲の座標を記入
    return [x1, y1, x2, y2]