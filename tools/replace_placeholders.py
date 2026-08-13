#!/usr/bin/env python3
# 文章配图工具（默认图 + 单篇覆盖）
#
# 现状：全站文章正文图已统一使用默认产品照片
#   /images/ext/p6-tt_byteimg_com/20bcba42e6af.jpg
#
# 用法：
#   1) 默认图已就位，无需任何操作。
#   2) 若想给「某篇文章」单独配图，把图片按【文章编号】命名放到 images/incoming/，例如：
#        images/incoming/3.jpg     -> 仅替换 article/3.html 的默认图
#        images/incoming/37.png    -> 仅替换 article/37.html 的默认图
#      支持的扩展名：jpg / jpeg / png / webp
#   3) 运行：python3 tools/replace_placeholders.py
#   4) 继续往 images/incoming/ 放图并重跑即可（已覆盖的不会重复处理）。
#
# 说明：脚本只把对应文章里【默认产品照片】替换为 incoming 里的该篇图片；
#       不会动其它已正常显示的真实图片。
import os, glob

ROOT = '/Users/bdeng/Documents/dbweb/shunarcn'
os.chdir(ROOT)
INC = 'images/incoming'
os.makedirs(INC, exist_ok=True)
DEFAULT_IMG = '/images/ext/p6-tt_byteimg_com/20bcba42e6af.jpg'

swapped = 0
for f in sorted(glob.glob('article/[0-9]*.html'), key=lambda p: int(os.path.basename(p)[:-5])):
    n = int(os.path.basename(f)[:-5])
    repl = None
    for ext in ('jpg', 'jpeg', 'png', 'webp'):
        cand = os.path.join(INC, f'{n}.{ext}')
        if os.path.exists(cand):
            repl = f'/images/incoming/{n}.{ext}'
            break
    if not repl:
        continue
    t = open(f, encoding='utf-8').read()
    if DEFAULT_IMG in t:
        t = t.replace(DEFAULT_IMG, repl)
        open(f, 'w', encoding='utf-8').write(t)
        swapped += 1
        print(f'{f}  ->  {repl}')

print(f'\n已为 {swapped} 篇覆盖默认图。其余文章仍用默认产品照片。')
print(f'把更多图片放进 {INC} 后重跑本脚本即可。')
