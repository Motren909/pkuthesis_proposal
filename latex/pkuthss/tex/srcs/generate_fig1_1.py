"""Generate Figure 1.1: global embodied-AI policy, deployment, and gap.

The output is a vector PDF intended for direct inclusion in the thesis.
Run from any directory with:
    python generate_fig1_1.py
"""

import os
import tempfile
from pathlib import Path


# Keep Matplotlib's cache writable when the script is run in a restricted
# build environment.  This must be set before importing Matplotlib.
MPL_CACHE_DIR = Path(tempfile.gettempdir()) / "thesis_matplotlib_cache"
MPL_CACHE_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE_DIR))

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from matplotlib import font_manager
import seaborn as sns


SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "figs"
OUTPUT_FILE = OUTPUT_DIR / "fig1_1_embodied_ai_landscape.pdf"


def configure_style() -> None:
    """Configure an academic, print-friendly style with a Chinese font."""
    sns.set_theme(style="white", context="paper")

    font_candidates = [
        Path(r"C:\Windows\Fonts\msyh.ttc"),
        Path(r"C:\Windows\Fonts\msyhbd.ttc"),
        Path(r"C:\Windows\Fonts\simhei.ttf"),
        Path(r"C:\Windows\Fonts\simsun.ttc"),
    ]
    for font_path in font_candidates:
        if font_path.exists():
            font_manager.fontManager.addfont(font_path)
            font_name = font_manager.FontProperties(fname=font_path).get_name()
            mpl.rcParams["font.family"] = "sans-serif"
            mpl.rcParams["font.sans-serif"] = [font_name]
            break

    mpl.rcParams.update(
        {
            "axes.unicode_minus": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "savefig.transparent": False,
        }
    )


def rounded_box(ax, x, y, width, height, face, edge, radius=1.2, lw=1.1):
    patch = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle=f"round,pad=0.45,rounding_size={radius}",
        facecolor=face,
        edgecolor=edge,
        linewidth=lw,
    )
    ax.add_patch(patch)
    return patch


def arrow(ax, start, end, color="#60758A", width=1.5):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=14,
            linewidth=width,
            color=color,
            shrinkA=2,
            shrinkB=2,
        )
    )


def add_policy_card(ax, x, title, date, body, color):
    rounded_box(ax, x, 39.0, 27.0, 13.5, "#FFFFFF", color, radius=1.3, lw=1.5)
    ax.text(x + 2.0, 49.7, title, fontsize=14.5, weight="bold", color=color, va="top")
    ax.text(x + 24.8, 49.7, date, fontsize=10.3, color="#667788", ha="right", va="top")
    ax.text(x + 2.0, 46.4, body, fontsize=11.0, color="#263746", va="top", linespacing=1.5)


def add_metric(ax, x, y, value, label, color):
    ax.text(x, y, value, fontsize=18.0, weight="bold", color=color, ha="center")
    ax.text(x, y - 3.0, label, fontsize=9.7, color="#405261", ha="center", linespacing=1.35)


def main() -> None:
    configure_style()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    palette = sns.color_palette("deep")
    blue = mpl.colors.to_hex(palette[0])
    orange = mpl.colors.to_hex(palette[1])
    green = mpl.colors.to_hex(palette[2])
    red = mpl.colors.to_hex(palette[3])
    navy = "#274C69"
    ink = "#263746"
    muted = "#60758A"

    fig, ax = plt.subplots(figsize=(13.2, 7.1))
    fig.patch.set_facecolor("#F7F9FB")
    ax.set_facecolor("#F7F9FB")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.axis("off")

    # Policy layer
    ax.text(4, 57.1, "政策牵引", fontsize=17, weight="bold", color=navy, va="center")
    ax.plot([15, 96], [57.1, 57.1], color="#C9D5DF", linewidth=1.0)
    add_policy_card(
        ax,
        4,
        "中国",
        "2021—2025",
        "机器人产业规划与“人工智能+”行动\n推动人机协同和智能社会新形态",
        red,
    )
    add_policy_card(
        ax,
        36.5,
        "美国",
        "2025",
        "AI Action Plan 支持下一代制造\n关注机器人规模化与供应链能力",
        blue,
    )
    add_policy_card(
        ax,
        69,
        "欧盟",
        "2025—2026",
        "Apply AI 覆盖机器人与制造\n强调测试验证、可信安全和以人为本",
        green,
    )

    # Transition from policy to deployment.
    for x in (17.5, 50, 82.5):
        arrow(ax, (x, 38.1), (x, 34.7), color="#8CA0B2", width=1.1)

    # Industry layer
    ax.text(4, 33.0, "产业落地（2026）", fontsize=17, weight="bold", color=navy, va="center")
    ax.plot([23, 96], [33.0, 33.0], color="#C9D5DF", linewidth=1.0)

    rounded_box(ax, 4, 13.2, 43.5, 16.3, "#FFFFFF", "#AFC5D8", radius=1.4, lw=1.2)
    ax.text(6, 27.4, "中国：供给增长与场景扩展", fontsize=13.5, weight="bold", color=ink, va="top")
    add_metric(ax, 11.5, 22.2, "+22.4%", "产业销售收入\n同比增长", blue)
    add_metric(ax, 23.3, 22.2, "2.3 倍", "工业企业购进\n金额同比增长", orange)
    add_metric(ax, 35.2, 22.2, ">4 万台", "上半年人形机器人\n出货量", green)
    ax.text(
        25.7,
        14.9,
        "物流中心 · 药店 · 景区 · 社区 · 商业服务",
        fontsize=10.4,
        color=muted,
        ha="center",
    )

    rounded_box(ax, 51, 13.2, 26.0, 16.3, "#FFFFFF", "#AFC5D8", radius=1.4, lw=1.2)
    ax.text(53, 27.4, "国际：真实产线试点", fontsize=13.5, weight="bold", color=ink, va="top")
    ax.text(53, 23.6, "德国莱比锡", fontsize=10.0, color=muted)
    ax.text(53, 21.0, "AEON：电池装配与物料配送", fontsize=11.2, color=ink)
    ax.plot([53, 75], [19.2, 19.2], color="#E0E6EB", linewidth=0.9)
    ax.text(53, 17.7, "美国斯帕坦堡", fontsize=10.0, color=muted)
    ax.text(53, 15.1, "Figure 02：参与 >3 万辆汽车生产", fontsize=11.2, color=ink)

    arrow(ax, (77.8, 21.3), (81.2, 21.3), color=orange, width=1.8)

    # Gap layer
    rounded_box(ax, 82, 11.4, 14.5, 20.0, "#FFF7EF", orange, radius=1.5, lw=1.5)
    ax.text(89.25, 28.6, "关键落差", fontsize=14.5, weight="bold", color=orange, ha="center")
    ax.text(89.25, 24.8, "样机 / 小批试用", fontsize=11.2, color=ink, ha="center")
    ax.text(89.25, 21.8, "↓", fontsize=18, weight="bold", color=orange, ha="center")
    ax.text(89.25, 18.9, "自然、稳定、\n普遍的人机共生", fontsize=11.5, weight="bold", color=red, ha="center", va="center")
    ax.text(89.25, 13.2, "环境适应 · 对象绑定\n意图理解 · 持续协作", fontsize=9.7, color=muted, ha="center", linespacing=1.45)

    # Bottom takeaway and source line.
    rounded_box(ax, 4, 5.0, 92.0, 4.6, "#EAF1F6", "#D1DCE5", radius=1.0, lw=0.9)
    ax.text(
        50,
        7.3,
        "共同趋势：智能机器加速进入物理世界；核心问题由“机器能做”转向“人与机器如何一起做”",
        fontsize=11.3,
        weight="bold",
        color=navy,
        ha="center",
        va="center",
    )
    ax.text(
        4,
        1.8,
        "数据与案例来源：国家税务总局（2026）、新华每日电讯（2026）、BMW Group（2026）。",
        fontsize=8.8,
        color="#687B8B",
    )

    fig.savefig(OUTPUT_FILE, bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)
    print(f"Generated vector figure: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
