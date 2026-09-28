import os, sys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as ndi

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'source.webp')
N = 2048
GREEN = np.array([33, 243, 12], float) / 255
BLACK = np.array([27, 25, 26], float) / 255


def glyph_mask(n):
    a = np.asarray(Image.open(SRC).convert('L'), float)
    m = (a < 120).astype(float)
    im = Image.fromarray((m * 255).astype(np.uint8)).resize((n * 2, n * 2), Image.LANCZOS)
    im = im.filter(ImageFilter.GaussianBlur(n / 700))
    b = (np.asarray(im, float) > 127).astype(np.uint8) * 255
    return np.asarray(Image.fromarray(b).resize((n, n), Image.LANCZOS), float) / 255


def blur(x, s):
    return ndi.gaussian_filter(x, s)


def over(base, col, a):
    a = a[..., None]
    return base * (1 - a) + np.asarray(col) * a


def screen(base, col, a):
    a = a[..., None]
    c = np.asarray(col)
    return base * (1 - a) + (1 - (1 - base) * (1 - c)) * a


def render(M, bg=True, n=N):
    s = n / 1024
    yy, xx = np.mgrid[0:n, 0:n] / n
    img = np.zeros((n, n, 3)) + (GREEN if bg else 0)
    alpha = np.ones((n, n)) if bg else np.zeros((n, n))
    if bg:
        # glass pane lighting on the green: soft top light, deeper edges
        img = screen(img, (1, 1, 1), 0.16 * np.clip(1 - yy * 1.6, 0, 1) ** 2)
        r = np.hypot(xx - .5, yy - .45)
        img = over(img, (0, 0.12, 0), np.clip((r - .35) / .45, 0, 1) ** 1.6 * 0.22)
        img = over(img, (0.05, 0.35, 0.02), 0.18 * np.clip(yy - .55, 0, 1) * 2)
    # drop + contact shadows
    sh = blur(np.roll(M, int(22 * s), 0), 26 * s)
    sh2 = blur(np.roll(M, int(6 * s), 0), 6 * s)
    if bg:
        img = over(img, (0, 0.1, 0), sh * 0.45)
        img = over(img, (0, 0.05, 0), sh2 * 0.35)
    else:
        alpha = np.maximum(alpha, sh * 0.4)
    # ---- black glass body ----
    body = np.zeros((n, n, 3)) + BLACK
    body = over(body, (0.16, 0.16, 0.17), np.clip(0.5 - yy, 0, 1) * 0.35)
    H = blur(M, 14 * s)
    gy, gx = np.gradient(H)
    light = np.array([-0.55, -0.85]); light /= np.linalg.norm(light)
    d = -(gx * light[0] + gy * light[1]); d /= np.abs(d).max() + 1e-9
    bev = d * (H < 0.999) * M
    body = screen(body, (1, 1, 1), np.clip(bev, 0, 1) ** 1.3 * 0.55)
    body = over(body, (0, 0, 0), np.clip(-bev, 0, 1) * 0.6)
    # green refraction at inner edges
    inner = np.clip(M * (1 - blur(M, 5 * s)) * 2.4, 0, 1)
    body = screen(body, GREEN, inner * 0.30)
    deep = M * (1 - blur(M, 40 * s))
    body = screen(body, GREEN * 0.6, np.clip(deep * 1.2, 0, 1) * 0.10)
    # crisp rim light
    k = max(3, int(5 * s))
    er = ndi.grey_erosion(M, size=(k, k))
    rim = np.clip(M - er, 0, 1) * np.clip(d * 1.6 + 0.25, 0, 1)
    body = screen(body, (1, 1, 1), rim * 0.7)
    # curved specular gloss
    inside = np.hypot(xx - 0.5, yy + 0.55) < 1.18
    gloss = inside * (0.10 + 0.16 * np.clip(1 - (yy - 0.05) / 0.5, 0, 1) ** 1.5)
    body = screen(body, (1, 1, 1), gloss * M)
    # diagonal glint streaks
    t = xx + yy * 0.55
    streak = np.exp(-((t - 0.62) / 0.02) ** 2) * 0.12 + np.exp(-((t - 0.69) / 0.006) ** 2) * 0.10
    body = screen(body, (1, 1, 1), streak * M * np.clip(1.1 - yy, 0, 1))
    img = img * (1 - M[..., None]) + body * M[..., None]
    alpha = np.maximum(alpha, M)
    if bg:
        img = screen(img, (1, 1, 1), 0.10 * np.exp(-(yy / 0.10) ** 2))
        img = screen(img, (1, 1, 1), np.exp(-(((xx + yy) - 0.28) / 0.05) ** 2) * 0.07)
    return np.clip(img, 0, 1), alpha


def save(img, alpha, path, size, rgba=False):
    arr = (img * 255 + 0.5).astype(np.uint8)
    if rgba:
        im = Image.fromarray(np.dstack([arr, (alpha * 255 + .5).astype(np.uint8)]), 'RGBA')
    else:
        im = Image.fromarray(arr, 'RGB')
    im.resize((size, size), Image.LANCZOS).save(path, optimize=True)


if __name__ == '__main__':
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    M = glyph_mask(N)
    img, a = render(M)
    save(img, a, f'{out}/icon-1024.png', 1024)
    save(img, a, f'{out}/icon-master-2048.png', 2048)
    save(img, a, f'{out}/play-store-512.png', 512)
    # Android adaptive: glyph inside the 66/108 safe zone
    k = 0.70
    sz = int(N * k)
    small = np.asarray(Image.fromarray((M * 255).astype(np.uint8)).resize((sz, sz), Image.LANCZOS), float) / 255
    Ma = np.zeros((N, N)); o = (N - sz) // 2; Ma[o:o + sz, o:o + sz] = small
    fi, fa = render(Ma, bg=False)
    save(fi, fa, f'{out}/android-adaptive-foreground-432.png', 432, rgba=True)
    bi, _ = render(np.zeros((N, N)))
    save(bi, None, f'{out}/android-adaptive-background-432.png', 432)
