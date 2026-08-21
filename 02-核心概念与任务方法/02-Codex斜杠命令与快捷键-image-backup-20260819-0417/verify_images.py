# 验收：画布四角透明、边框/白边/主体像素正确、主体内容与原图一致
import sys
from PIL import Image

PAD, MARGIN = 10, 4

def check(orig, out):
    o = Image.open(orig).convert('RGBA')
    n = Image.open(out).convert('RGBA')
    W, H = n.size
    issues = []

    # 1) 画布四角必须透明
    for name, (x, y) in {'TL': (0, 0), 'TR': (W - 1, 0), 'BL': (0, H - 1), 'BR': (W - 1, H - 1)}.items():
        if n.getpixel((x, y))[3] != 0:
            issues.append(f'canvas corner {name} not transparent: {n.getpixel((x, y))}')

    cy = H // 2
    # 2) 边框像素（左边缘中线）应为 #d9d9d9
    b = n.getpixel((PAD, cy))
    if abs(b[0] - 217) > 12 or abs(b[1] - 217) > 12 or abs(b[2] - 217) > 12 or b[3] < 200:
        issues.append(f'border pixel unexpected: {b}')
    # 3) 白边像素应为白色不透明
    wpx = n.getpixel((PAD + 2, cy))
    if wpx[:3] != (255, 255, 255) or wpx[3] != 255:
        issues.append(f'white margin pixel unexpected: {wpx}')
    # 4) 主体内容与原图一致（中心线采样）
    sx, sy = PAD + MARGIN + 2, cy
    ox, oy = 2, o.size[1] // 2
    if n.getpixel((sx, sy))[:3] != o.getpixel((ox, oy))[:3]:
        issues.append(f'subject mismatch: new {n.getpixel((sx, sy))} vs orig {o.getpixel((ox, oy))}')
    # 5) 主体圆角处应被透明裁切（透出白边则证明已裁；仍显示原图角像素则未裁）
    c = n.getpixel((PAD + MARGIN + 1, PAD + MARGIN + 1))
    oc = o.getpixel((1, 1))
    if c[:3] != (255, 255, 255) and c[:3] == oc[:3] and oc[:3] != (255, 255, 255):
        issues.append(f'subject corner not rounded-cut: new {c} == orig {oc}')

    print(('PASS ' if not issues else 'FAIL ') + out)
    for i in issues:
        print('   - ' + i)

pairs = [
    (r'D:\codexguide_all\教程\02-核心概念与任务方法\02-Codex斜杠命令与快捷键-图片\online\cli-01-version.png',
     r'D:\codexguide_all\教程\02-核心概念与任务方法\02-Codex斜杠命令与快捷键-图片\online\图一.png'),
    (r'D:\codexguide_all\教程\02-核心概念与任务方法\02-Codex斜杠命令与快捷键-图片\online\cli-02-start.png',
     r'D:\codexguide_all\教程\02-核心概念与任务方法\02-Codex斜杠命令与快捷键-图片\online\图二.png'),
    (r'D:\codexguide_all\教程\02-核心概念与任务方法\02-Codex斜杠命令与快捷键-图片\online\cli-03-slash-menu.png',
     r'D:\codexguide_all\教程\02-核心概念与任务方法\02-Codex斜杠命令与快捷键-图片\online\图三.png'),
    (r'D:\codexguide_all\教程\02-核心概念与任务方法\02-Codex斜杠命令与快捷键-图片备份-20260818-0552\online\figure-01-slash-menu.png',
     r'D:\codexguide_all\教程\02-核心概念与任务方法\02-Codex斜杠命令与快捷键-图片备份-20260818-0552\online\图四.png'),
    (r'D:\codexguide_all\教程\02-核心概念与任务方法\02-Codex斜杠命令与快捷键-图片备份-20260818-0552\online\figure-02-task-flow.png',
     r'D:\codexguide_all\教程\02-核心概念与任务方法\02-Codex斜杠命令与快捷键-图片备份-20260818-0552\online\图五.png'),
    (r'D:\codexguide_all\教程\02-核心概念与任务方法\02-Codex斜杠命令与快捷键-图片备份-20260818-0552\online\figure-03-input-layers.png',
     r'D:\codexguide_all\教程\02-核心概念与任务方法\02-Codex斜杠命令与快捷键-图片备份-20260818-0552\online\图六.png'),
    (r'D:\codexguide_all\教程\02-核心概念与任务方法\02-Codex斜杠命令与快捷键-图片\online\cli-04-keymap.png',
     r'D:\codexguide_all\教程\02-核心概念与任务方法\02-Codex斜杠命令与快捷键-图片\online\图七.png'),
]
for orig, out in pairs:
    check(orig, out)
