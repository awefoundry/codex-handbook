# imagegzh 一号样式本地处理：4px 白边 + 主体 8px 圆角 + 外轮廓 12px 圆角
# + 1px #d9d9d9 边框 + 极轻阴影，画布四角透明。无损、不改文字布局、不覆盖原图。
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops

MARGIN = 4          # 白色外边距
R_IN = 8            # 截图主体圆角
R_OUT = 12          # 白色边界外圆角
BORDER = (217, 217, 217, 255)  # #d9d9d9
SHADOW_PAD = 10     # 阴影画布余量
SHADOW_OFFSET = 2
SHADOW_BLUR = 5
SHADOW_ALPHA = 26   # 极轻

def rounded_mask(size, radius):
    m = Image.new('L', size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=radius, fill=255)
    return m

def process(src, dst):
    img = Image.open(src).convert('RGBA')
    w, h = img.size

    # 1) 主体圆角透明裁切
    alpha = img.getchannel('A')
    img.putalpha(ImageChops.multiply(alpha, rounded_mask((w, h), R_IN)))

    # 2) 白色边界（外圆角），主体居中留 4px 白边
    inner = Image.new('RGBA', (w + 2 * MARGIN, h + 2 * MARGIN), (0, 0, 0, 0))
    white = Image.new('RGBA', inner.size, (255, 255, 255, 255))
    white.putalpha(rounded_mask(inner.size, R_OUT))
    inner.alpha_composite(white)
    inner.alpha_composite(img, (MARGIN, MARGIN))

    # 3) 1px 浅灰边框
    d = ImageDraw.Draw(inner)
    d.rounded_rectangle([0, 0, inner.size[0] - 1, inner.size[1] - 1], radius=R_OUT, outline=BORDER, width=1)

    # 4) 极轻阴影 + 透明画布
    W, H = inner.size
    canvas = Image.new('RGBA', (W + 2 * SHADOW_PAD, H + 2 * SHADOW_PAD), (0, 0, 0, 0))
    shadow = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        [SHADOW_PAD, SHADOW_PAD + SHADOW_OFFSET, SHADOW_PAD + W - 1, SHADOW_PAD + H - 1 + SHADOW_OFFSET],
        radius=R_OUT, fill=(0, 0, 0, SHADOW_ALPHA))
    shadow = shadow.filter(ImageFilter.GaussianBlur(SHADOW_BLUR))
    canvas.alpha_composite(shadow)
    canvas.alpha_composite(inner, (SHADOW_PAD, SHADOW_PAD))

    canvas.save(dst)
    print(f"OK {dst} {canvas.size[0]}x{canvas.size[1]}")

if __name__ == '__main__':
    process(sys.argv[1], sys.argv[2])
