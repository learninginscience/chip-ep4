"""組建網站：把 src/ 裡的原始檔組成可以直接上線的 index.html（學生）、teacher.html（老師投影）與 play.html（直接玩版）。

用法（在專案根目錄）：
    python build.py

會做的事：
  1. 把 src/live_core.js（即時房間核心）塞進兩個頁面的 {{LIVE_CORE}}
  2. 把 src/firebase_config.json 塞進 live_core 的 {{FIREBASE_CONFIG}}
  3. 把 src/chars/*.jpg 角色圖轉成 base64，塞進 {{IMG:名稱}}
  4. 加上 <!doctype html>、<head> 等外框，輸出到根目錄
  5. play.html：學生頁把最後的 renderStart(); 換成 src/play_boot.js（打開就直接玩，不登記、不連房間）

不要直接改根目錄的 index.html、teacher.html、play.html，下次組建會被蓋掉。
"""
import base64, json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'src')
IMGS = ['bot', 'bot_happy', 'kilby', 'kilby_happy', 'noyce']


def read(*p):
    return open(os.path.join(SRC, *p), encoding='utf-8').read()


cfg_path = os.path.join(SRC, 'firebase_config.json')
cfg = json.dumps(json.load(open(cfg_path, encoding='utf-8')), ensure_ascii=False) if os.path.exists(cfg_path) else 'null'
core = read('live_core.js').replace('{{FIREBASE_CONFIG}}', cfg)


def fill(src):
    src = src.replace('{{LIVE_CORE}}', core)
    for k in IMGS:
        b = base64.b64encode(open(os.path.join(SRC, 'chars', f'{k}.jpg'), 'rb').read()).decode()
        src = src.replace('{{IMG:%s}}' % k, 'data:image/jpeg;base64,' + b)
    assert '{{IMG' not in src and '{{LIVE_CORE}}' not in src and '{{FIREBASE_CONFIG}}' not in src, '還有沒填好的 {{...}}'
    return src


def page(src, desc):
    cut = src.index('</style>') + len('</style>')
    return ('<!doctype html>\n<html lang="zh-Hant">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<meta name="description" content="{desc}">\n'
            + src[:cut] + '\n</head>\n<body>' + src[cut:] + '\n</body>\n</html>\n')


game = fill(read('game.src.html'))
teacher = fill(read('teacher.src.html'))
with open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(page(game, '晶片系列 EP4 課堂活動：用兩位科學家的想法，親手設計出阿寶的晶片。'))
with open(os.path.join(ROOT, 'teacher.html'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(page(teacher, '導線走線大師老師投影頁：開房間、即時排行榜、暫停、頒獎台。'))
# 直接玩版：只換掉啟動那一行，其他程式和學生頁完全一樣
BOOT = '\nrenderStart();\n})();'
assert game.count(BOOT) == 1, '找不到學生頁最後的 renderStart();'
play = game.replace(BOOT, '\n' + read('play_boot.js') + '})();')
with open(os.path.join(ROOT, 'play.html'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(page(play, '晶片系列 EP4 課堂活動（直接玩版）：打開就開始，親手設計出阿寶的晶片。'))
print('組建完成：index.html', os.path.getsize(os.path.join(ROOT, 'index.html')) // 1024, 'KB，teacher.html',
      os.path.getsize(os.path.join(ROOT, 'teacher.html')) // 1024, 'KB，play.html',
      os.path.getsize(os.path.join(ROOT, 'play.html')) // 1024, 'KB，Firebase', '已連線' if cfg != 'null' else '未設定')
