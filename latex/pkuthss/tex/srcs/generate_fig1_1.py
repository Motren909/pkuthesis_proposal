"""Generate Figure 1.1: industry growth and the collaboration gap."""

import os
import tempfile
from pathlib import Path


MPL_CACHE_DIR = Path(tempfile.gettempdir()) / "thesis_matplotlib_cache"
MPL_CACHE_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE_DIR))

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager


SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "figs"
OUTPUT_FILE = OUTPUT_DIR / "fig1_1_embodied_ai_landscape.pdf"
PREVIEW_FILE = OUTPUT_DIR / "fig1_1_embodied_ai_landscape.png"

# Latest public figures available by September 2026.
# Industry growth: State Taxation Administration of China, 30 June 2026.
EMBODIED_REVENUE_GROWTH_2026 = 22.4
INTEGRATION_REVENUE_GROWTH_2026 = 27.9

# Deployment and task performance: Stanford AI Index Report 2026.
# The cobot figure is based on IFR World Robotics 2025; BEHAVIOR-1K is a
# simulated, realistic household benchmark rather than a field deployment.
COBOT_SHARE_2024 = 13.6
TRADITIONAL_SHARE_2024 = 100 - COBOT_SHARE_2024
HOUSEHOLD_TASK_SUCCESS_2025 = 12.4
HOUSEHOLD_TASK_INCOMPLETE_2025 = 100 - HOUSEHOLD_TASK_SUCCESS_2025


def configure_style() -> None:
    """Set a minimal, publication-ready style and use an available CJK font."""
    for font_path in (
        Path(r"C:\Windows\Fonts\msyh.ttc"),
        Path(r"C:\Windows\Fonts\simhei.ttf"),
        Path(r"C:\Windows\Fonts\simsun.ttc"),
    ):
        if font_path.exists():
            font_manager.fontManager.addfont(font_path)
            font_name = font_manager.FontProperties(fname=font_path).get_name()
            mpl.rcParams["font.family"] = "sans-serif"
            mpl.rcParams["font.sans-serif"] = [font_name]
            break

    mpl.rcParams.update(
        {
            "axes.unicode_minus": False,
            "font.size": 10,
            "axes.titlesize": 11.5,
            "axes.titleweight": "bold",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
            "savefig.transparent": False,
        }
    )


def clean_axes(ax) -> None:
    """Remove chart decoration that does not carry data."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#B8C0C8")
    ax.spines["bottom"].set_color("#B8C0C8")
    ax.tick_params(length=0, colors="#586574")
    ax.grid(axis="y", color="#E8ECEF", linewidth=0.8)
    ax.set_axisbelow(True)


def main() -> None:
    configure_style()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    blue = "#4676A9"
    orange = "#DF743A"
    grey = "#CBD2D9"
    text = "#263746"
    muted = "#66727D"

    fig, axes = plt.subplots(
        1,
        3,
        figsize=(11.4, 4.5),
        gridspec_kw={"width_ratios": [1.12, 1, 1], "wspace": 0.36},
    )
    fig.subplots_adjust(left=0.07, right=0.98, top=0.83, bottom=0.32)

    panels = (
        {
            "title": "产业增长｜2026 年 1—5 月",
            "labels": ["具身智能\n产业", "系统集成与\n行业应用"],
            "values": [EMBODIED_REVENUE_GROWTH_2026, INTEGRATION_REVENUE_GROWTH_2026],
            "colors": [blue, blue],
            "ylabel": "销售收入同比增长（%）",
            "ylim": 35,
            "yticks": [0, 10, 20, 30],
        },
        {
            "title": "协作部署｜实际装机",
            "labels": ["传统型", "协作型"],
            "values": [TRADITIONAL_SHARE_2024, COBOT_SHARE_2024],
            "colors": [grey, orange],
            "ylabel": "2025 年新增安装占比（%）",
            "ylim": 100,
            "yticks": [0, 20, 40, 60, 80, 100],
        },
        {
            "title": "具体场景｜拟真家庭任务",
            "labels": ["未完整\n完成", "完整\n完成"],
            "values": [HOUSEHOLD_TASK_INCOMPLETE_2025, HOUSEHOLD_TASK_SUCCESS_2025],
            "colors": [grey, orange],
            "ylabel": "2025 年完整任务占比（%）",
            "ylim": 100,
            "yticks": [0, 20, 40, 60, 80, 100],
        },
    )

    for ax, panel in zip(axes, panels):
        bars = ax.bar(panel["labels"], panel["values"], width=0.56, color=panel["colors"])
        ax.set_title(panel["title"], loc="left", pad=12, color=text)
        ax.set_ylabel(panel["ylabel"], color=muted)
        ax.set_ylim(0, panel["ylim"])
        ax.set_yticks(panel["yticks"])
        clean_axes(ax)
        for bar, value, color in zip(bars, panel["values"], panel["colors"]):
            label_color = orange if color == orange else (blue if color == blue else muted)
            ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + panel["ylim"] * 0.035,
            f"{value:.1f}%",
            ha="center",
            va="bottom",
            color=label_color,
            fontweight="bold",
        )

    fig.text(
        0.07,
        0.13,
        "数据来源：国家税务总局（2026-06-30）；Stanford HAI《AI Index Report 2026》；IFR《World Robotics 2025》。",
        fontsize=8.0,
        color=muted,
    )

    fig.savefig(OUTPUT_FILE, bbox_inches="tight", pad_inches=0.06)
    fig.savefig(PREVIEW_FILE, dpi=220, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    print(f"Generated vector figure: {OUTPUT_FILE}")
    print(f"Generated preview: {PREVIEW_FILE}")


if __name__ == "__main__":
    main()
