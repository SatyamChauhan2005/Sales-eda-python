"""
============================================================
PROJECT 1: Sales Data — Complete EDA (Exploratory Data Analysis)
File: sales_eda.py
============================================================
This project performs a thorough EDA on a sales dataset and
generates 12+ insights with visualizations.

Requirements:
    pip install pandas numpy matplotlib seaborn plotly

Usage:
    python sales_eda.py
    (Charts will save to: charts/ folder)
============================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
import os

warnings.filterwarnings("ignore")
os.makedirs("charts", exist_ok=True)

# ─────────────────────────────────────────
# PALETTE & STYLE
# ─────────────────────────────────────────
COLORS = {
    "primary":   "#1E3A5F",
    "secondary": "#2E6DA4",
    "accent":    "#E8632A",
    "success":   "#2E8B57",
    "warning":   "#E8A020",
    "light":     "#D6E4F0",
    "gray":      "#95A5A6",
}
PALETTE = [COLORS["primary"], COLORS["secondary"], COLORS["accent"],
           COLORS["success"], COLORS["warning"], "#8E44AD", "#C0392B"]

plt.rcParams.update({
    "font.family":      "DejaVu Sans",
    "axes.spines.top":  False,
    "axes.spines.right":False,
    "axes.titlesize":   14,
    "axes.titleweight": "bold",
    "axes.titlecolor":  COLORS["primary"],
    "axes.labelsize":   11,
    "xtick.labelsize":  9,
    "ytick.labelsize":  9,
    "figure.facecolor": "white",
    "axes.facecolor":   "#FAFBFC",
    "grid.color":       "#E8ECF0",
    "grid.linewidth":   0.8,
})


# ─────────────────────────────────────────
# STEP 1: Generate realistic sample dataset
# (In real project: df = pd.read_csv("your_file.csv"))
# ─────────────────────────────────────────
def generate_dataset(n=800, seed=42):
    """
    Generate a realistic sales dataset.
    In your actual project, replace with:
        df = pd.read_csv("sales_data.csv")
        df = pd.read_excel("sales_data.xlsx")
    """
    rng = np.random.default_rng(seed)

    regions      = ["North", "South", "East", "West", "Central"]
    categories   = ["Laptops", "Mobiles", "Accessories", "Furniture", "Stationery", "Printers"]
    cust_types   = ["Retail", "Corporate", "SMB"]
    sales_reps   = [f"Rep_{i:02d}" for i in range(1, 16)]

    # Weighted probabilities for realism
    cat_weights  = [0.20, 0.18, 0.25, 0.12, 0.15, 0.10]
    reg_weights  = [0.22, 0.20, 0.18, 0.22, 0.18]
    type_weights = [0.40, 0.35, 0.25]

    dates = pd.date_range("2023-01-01", "2024-07-31", freq="D")
    order_dates = rng.choice(dates, size=n, replace=True)

    category = rng.choice(categories, size=n, p=cat_weights)

    # Price ranges by category
    price_ranges = {
        "Laptops":      (30000, 90000),
        "Mobiles":      (15000, 85000),
        "Accessories":  (500,    5000),
        "Furniture":    (8000,  35000),
        "Stationery":   (100,    2000),
        "Printers":     (12000, 40000),
    }
    prices = np.array([
        rng.uniform(*price_ranges[c]) for c in category
    ])

    # Cost is 60–75% of price
    cost_pct  = rng.uniform(0.60, 0.75, n)
    costs     = prices * cost_pct
    qty       = rng.integers(1, 20, size=n)
    discount  = rng.choice([0, 0, 0, 5, 7.5, 10, 15], size=n)  # mostly no discount
    net_price = prices * (1 - discount / 100)

    df = pd.DataFrame({
        "order_id":      [f"ORD-{10000+i}" for i in range(n)],
        "order_date":    pd.to_datetime(order_dates),
        "region":        rng.choice(regions, size=n, p=reg_weights),
        "customer_type": rng.choice(cust_types, size=n, p=type_weights),
        "sales_rep":     rng.choice(sales_reps, size=n),
        "category":      category,
        "unit_price":    np.round(prices, 2),
        "cost_price":    np.round(costs, 2),
        "quantity":      qty,
        "discount_pct":  discount,
        "net_unit_price":np.round(net_price, 2),
        "revenue":       np.round(net_price * qty, 2),
        "profit":        np.round((net_price - costs) * qty, 2),
    })

    df["order_month"]   = df["order_date"].dt.to_period("M")
    df["order_quarter"] = df["order_date"].dt.to_period("Q")
    df["order_year"]    = df["order_date"].dt.year
    df["day_of_week"]   = df["order_date"].dt.day_name()
    df["profit_margin"] = (df["profit"] / df["revenue"] * 100).round(2)

    # Introduce 2% missing values for realism
    mask = rng.random(n) < 0.02
    df.loc[mask, "discount_pct"] = np.nan

    return df


# ─────────────────────────────────────────
# STEP 2: Data Overview & Cleaning
# ─────────────────────────────────────────
def data_overview(df):
    print("\n" + "="*60)
    print("  STEP 1: DATA OVERVIEW")
    print("="*60)
    print(f"\n📐 Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"\n📋 Columns:\n{df.dtypes.to_string()}")
    print(f"\n📊 Numerical Summary:")
    print(df[["unit_price","quantity","revenue","profit","profit_margin"]].describe().round(2).to_string())
    print(f"\n❓ Missing Values:")
    print(df.isnull().sum()[df.isnull().sum() > 0].to_string())

def clean_data(df):
    print("\n" + "="*60)
    print("  STEP 2: DATA CLEANING")
    print("="*60)
    before = df.shape[0]

    # Fill missing discount with 0 (no discount)
    df["discount_pct"].fillna(0, inplace=True)

    # Remove any duplicate orders
    df.drop_duplicates(subset="order_id", inplace=True)

    # Ensure no negative revenue or profit
    df = df[df["revenue"] > 0].copy()

    after = df.shape[0]
    print(f"  ✅ Rows before: {before:,}  |  After: {after:,}  |  Removed: {before-after}")
    print(f"  ✅ Missing values filled: discount_pct → 0")
    print(f"  ✅ Duplicates removed, revenue sanity checked")
    return df


# ─────────────────────────────────────────
# STEP 3: EDA — 12 Insights
# ─────────────────────────────────────────
def save(fig, name):
    path = f"charts/{name}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  💾 Saved: {path}")


def insight_01_revenue_overview(df):
    """INSIGHT 1: High-level KPI summary"""
    print("\n── Insight 1: KPI Overview ──")
    total_rev  = df["revenue"].sum()
    total_prof = df["profit"].sum()
    avg_margin = df["profit_margin"].mean()
    avg_order  = df["revenue"].mean()
    total_ord  = df["order_id"].nunique()

    kpis = {
        "Total Revenue (₹)": f"₹{total_rev/1e7:.2f} Cr",
        "Total Profit (₹)":  f"₹{total_prof/1e7:.2f} Cr",
        "Avg Profit Margin": f"{avg_margin:.1f}%",
        "Total Orders":      f"{total_ord:,}",
        "Avg Order Value":   f"₹{avg_order:,.0f}",
    }

    fig, axes = plt.subplots(1, 5, figsize=(18, 4))
    fig.suptitle("Executive Dashboard — Key Performance Indicators", fontsize=16, fontweight="bold", color=COLORS["primary"], y=1.02)

    for ax, (label, value), color in zip(axes, kpis.items(), PALETTE):
        ax.set_facecolor(color)
        ax.text(0.5, 0.6, value, transform=ax.transAxes,
                ha="center", va="center", fontsize=20, fontweight="bold", color="white")
        ax.text(0.5, 0.25, label, transform=ax.transAxes,
                ha="center", va="center", fontsize=9, color="white", alpha=0.9)
        ax.set_xticks([]); ax.set_yticks([])
        for spine in ax.spines.values(): spine.set_visible(False)

    plt.tight_layout()
    save(fig, "01_kpi_overview")
    print(f"    Revenue: ₹{total_rev:,.0f}  |  Profit: ₹{total_prof:,.0f}  |  Margin: {avg_margin:.1f}%")


def insight_02_monthly_trend(df):
    """INSIGHT 2: Monthly revenue & profit trend"""
    print("\n── Insight 2: Monthly Revenue Trend ──")
    monthly = (
        df.groupby("order_month")
        .agg(revenue=("revenue","sum"), profit=("profit","sum"))
        .reset_index()
    )
    monthly["order_month"] = monthly["order_month"].astype(str)

    fig, ax = plt.subplots(figsize=(16, 5))
    ax.fill_between(range(len(monthly)), monthly["revenue"]/1e6, alpha=0.15, color=COLORS["primary"])
    ax.plot(range(len(monthly)), monthly["revenue"]/1e6,
            marker="o", color=COLORS["primary"], linewidth=2.5, markersize=6, label="Revenue (₹M)")
    ax.plot(range(len(monthly)), monthly["profit"]/1e6,
            marker="s", color=COLORS["accent"], linewidth=2, markersize=5,
            linestyle="--", label="Profit (₹M)")

    ax.set_xticks(range(len(monthly)))
    ax.set_xticklabels(monthly["order_month"], rotation=45, ha="right")
    ax.set_title("Monthly Revenue & Profit Trend (2023–2024)")
    ax.set_ylabel("Amount (₹ Millions)")
    ax.legend()
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("₹%.1fM"))
    ax.grid(True, axis="y")

    # Annotate max revenue month
    max_idx = monthly["revenue"].idxmax()
    ax.annotate(f"Peak\n₹{monthly['revenue'][max_idx]/1e6:.1f}M",
                xy=(max_idx, monthly["revenue"][max_idx]/1e6),
                xytext=(max_idx+1, monthly["revenue"][max_idx]/1e6 + 2),
                arrowprops=dict(arrowstyle="->", color=COLORS["accent"]),
                color=COLORS["accent"], fontsize=9, fontweight="bold")

    save(fig, "02_monthly_trend")


def insight_03_region_performance(df):
    """INSIGHT 3: Revenue by region"""
    print("\n── Insight 3: Region Performance ──")
    reg = (
        df.groupby("region")
        .agg(revenue=("revenue","sum"), orders=("order_id","count"))
        .sort_values("revenue", ascending=True)
    )

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Horizontal bar
    bars = ax1.barh(reg.index, reg["revenue"]/1e6, color=PALETTE[:len(reg)], edgecolor="white", height=0.6)
    for bar, val in zip(bars, reg["revenue"]/1e6):
        ax1.text(val + 0.3, bar.get_y() + bar.get_height()/2,
                 f"₹{val:.1f}M", va="center", fontsize=10, fontweight="bold")
    ax1.set_title("Revenue by Region")
    ax1.set_xlabel("Revenue (₹ Millions)")
    ax1.set_xlim(0, reg["revenue"].max()/1e6 * 1.25)

    # Pie chart share
    ax2.pie(reg["revenue"], labels=reg.index, colors=PALETTE[:len(reg)],
            autopct="%1.1f%%", startangle=140, pctdistance=0.82,
            wedgeprops={"edgecolor":"white","linewidth":2})
    ax2.set_title("Revenue Share by Region")

    fig.suptitle("Regional Performance Analysis", fontsize=14, fontweight="bold", color=COLORS["primary"])
    plt.tight_layout()
    save(fig, "03_region_performance")


def insight_04_category_analysis(df):
    """INSIGHT 4: Category revenue & margin"""
    print("\n── Insight 4: Category Analysis ──")
    cat = (
        df.groupby("category")
        .agg(revenue=("revenue","sum"), profit=("profit","sum"),
             units=("quantity","sum"), orders=("order_id","count"))
        .assign(margin=lambda x: x["profit"]/x["revenue"]*100)
        .sort_values("revenue", ascending=False)
    )

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Revenue bars
    axes[0].bar(cat.index, cat["revenue"]/1e6, color=PALETTE[:len(cat)], edgecolor="white")
    axes[0].set_title("Revenue by Category")
    axes[0].set_ylabel("Revenue (₹ Millions)")
    axes[0].set_xticklabels(cat.index, rotation=30, ha="right")

    # Margin scatter
    scatter = axes[1].scatter(cat["revenue"]/1e6, cat["margin"],
                               s=cat["units"]/cat["units"].max()*800 + 100,
                               c=PALETTE[:len(cat)], edgecolors="white", linewidth=1.5, alpha=0.85)
    for i, (idx, row) in enumerate(cat.iterrows()):
        axes[1].annotate(idx, (row["revenue"]/1e6, row["margin"]),
                          textcoords="offset points", xytext=(6, 4), fontsize=8)
    axes[1].set_title("Revenue vs Profit Margin\n(bubble size = units sold)")
    axes[1].set_xlabel("Revenue (₹ Millions)")
    axes[1].set_ylabel("Profit Margin %")
    axes[1].axhline(cat["margin"].mean(), color="gray", linestyle="--", linewidth=1, alpha=0.7)
    axes[1].text(cat["revenue"].max()/1e6*0.7, cat["margin"].mean()+0.5,
                 f"Avg {cat['margin'].mean():.1f}%", color="gray", fontsize=9)

    fig.suptitle("Product Category Deep-Dive", fontsize=14, fontweight="bold", color=COLORS["primary"])
    plt.tight_layout()
    save(fig, "04_category_analysis")


def insight_05_customer_type(df):
    """INSIGHT 5: Customer type breakdown"""
    print("\n── Insight 5: Customer Type Analysis ──")
    ct = (
        df.groupby("customer_type")
        .agg(revenue=("revenue","sum"), orders=("order_id","count"),
             avg_order=("revenue","mean"), profit=("profit","sum"))
        .assign(margin=lambda x: x["profit"]/x["revenue"]*100)
    )

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    for ax, metric, label, fmt in zip(
        axes,
        ["revenue", "avg_order", "margin"],
        ["Total Revenue (₹M)", "Avg Order Value (₹)", "Profit Margin (%)"],
        [1e6, 1, 1]
    ):
        vals = ct[metric] / fmt
        colors_ = [COLORS["primary"], COLORS["accent"], COLORS["success"]]
        bars = ax.bar(ct.index, vals, color=colors_, edgecolor="white", width=0.5)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + vals.max()*0.01,
                    f"{'₹' if fmt>1 else ''}{val:.1f}{'M' if fmt==1e6 else '%' if fmt==1 and 'Margin' in label else ''}",
                    ha="center", fontsize=11, fontweight="bold")
        ax.set_title(label)
        ax.set_ylim(0, vals.max() * 1.25)

    fig.suptitle("Customer Type Performance", fontsize=14, fontweight="bold", color=COLORS["primary"])
    plt.tight_layout()
    save(fig, "05_customer_type")


def insight_06_profit_distribution(df):
    """INSIGHT 6: Profit margin distribution"""
    print("\n── Insight 6: Profit Margin Distribution ──")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Histogram
    axes[0].hist(df["profit_margin"], bins=30, color=COLORS["primary"], edgecolor="white", alpha=0.85)
    axes[0].axvline(df["profit_margin"].mean(), color=COLORS["accent"], linestyle="--", linewidth=2,
                    label=f"Mean: {df['profit_margin'].mean():.1f}%")
    axes[0].axvline(df["profit_margin"].median(), color=COLORS["success"], linestyle=":", linewidth=2,
                    label=f"Median: {df['profit_margin'].median():.1f}%")
    axes[0].set_title("Profit Margin Distribution")
    axes[0].set_xlabel("Profit Margin %")
    axes[0].set_ylabel("Frequency")
    axes[0].legend()

    # Box plot by category
    cat_order = df.groupby("category")["profit_margin"].median().sort_values(ascending=False).index
    df.boxplot(column="profit_margin", by="category", ax=axes[1],
               positions=range(len(cat_order)),
               order=cat_order,
               patch_artist=True,
               boxprops=dict(facecolor=COLORS["light"]),
               medianprops=dict(color=COLORS["accent"], linewidth=2))
    axes[1].set_title("Profit Margin by Category")
    axes[1].set_xlabel("Category")
    axes[1].set_ylabel("Profit Margin %")
    axes[1].set_xticklabels(cat_order, rotation=30, ha="right")
    plt.suptitle("")

    fig.suptitle("Profit Margin Analysis", fontsize=14, fontweight="bold", color=COLORS["primary"])
    plt.tight_layout()
    save(fig, "06_profit_distribution")


def insight_07_discount_impact(df):
    """INSIGHT 7: How discounts affect profitability"""
    print("\n── Insight 7: Discount Impact ──")
    df2 = df.copy()
    df2["discount_band"] = pd.cut(
        df2["discount_pct"],
        bins=[-1, 0, 5, 10, 100],
        labels=["No Discount", "1-5%", "6-10%", ">10%"]
    )
    disc = df2.groupby("discount_band").agg(
        orders=("order_id","count"),
        revenue=("revenue","sum"),
        profit=("profit","sum"),
        avg_qty=("quantity","mean")
    ).assign(margin=lambda x: x["profit"]/x["revenue"]*100)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    colors_ = [COLORS["success"], COLORS["warning"], COLORS["accent"], "#C0392B"]

    axes[0].bar(disc.index.astype(str), disc["margin"], color=colors_, edgecolor="white", width=0.5)
    for i, (idx, row) in enumerate(disc.iterrows()):
        axes[0].text(i, row["margin"] + 0.3, f"{row['margin']:.1f}%",
                     ha="center", fontsize=12, fontweight="bold")
    axes[0].set_title("Profit Margin by Discount Band")
    axes[0].set_ylabel("Profit Margin %")
    axes[0].set_ylim(0, disc["margin"].max()*1.25)

    axes[1].bar(disc.index.astype(str), disc["revenue"]/1e6, color=colors_, edgecolor="white", width=0.5)
    axes[1].set_title("Revenue by Discount Band")
    axes[1].set_ylabel("Revenue (₹ Millions)")

    fig.suptitle("Discount Impact on Revenue & Margin", fontsize=14, fontweight="bold", color=COLORS["primary"])
    plt.tight_layout()
    save(fig, "07_discount_impact")

    print(f"    KEY FINDING: No-discount orders have {disc.loc['No Discount','margin']:.1f}% margin vs "
          f"{disc.iloc[-1]['margin']:.1f}% for >10% discount band")


def insight_08_correlation_heatmap(df):
    """INSIGHT 8: Correlation matrix"""
    print("\n── Insight 8: Correlation Heatmap ──")
    num_cols = ["unit_price", "quantity", "discount_pct", "revenue", "profit", "profit_margin"]
    corr = df[num_cols].corr()

    fig, ax = plt.subplots(figsize=(10, 7))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues",
                mask=mask, ax=ax, linewidths=0.5,
                annot_kws={"size":11, "weight":"bold"},
                cbar_kws={"shrink":0.8})
    ax.set_title("Correlation Matrix — Numerical Features", fontsize=14, fontweight="bold", color=COLORS["primary"])
    plt.tight_layout()
    save(fig, "08_correlation_heatmap")


def insight_09_quarterly_comparison(df):
    """INSIGHT 9: Quarterly YoY comparison"""
    print("\n── Insight 9: Quarterly Comparison ──")
    q_data = (
        df.groupby(["order_year", df["order_date"].dt.quarter])
        .agg(revenue=("revenue","sum"))
        .reset_index()
        .rename(columns={"order_date":"quarter"})
    )
    q_data["label"] = "Q" + q_data["quarter"].astype(str)

    pivot = q_data.pivot(index="label", columns="order_year", values="revenue").fillna(0)

    fig, ax = plt.subplots(figsize=(10, 5))
    x     = np.arange(len(pivot))
    width = 0.35
    for i, (yr, color) in enumerate(zip(pivot.columns, [COLORS["primary"], COLORS["accent"]])):
        bars = ax.bar(x + i*width, pivot[yr]/1e6, width, label=str(yr), color=color, edgecolor="white")
        for bar in bars:
            h = bar.get_height()
            if h > 0:
                ax.text(bar.get_x()+bar.get_width()/2, h+0.3, f"₹{h:.1f}M",
                        ha="center", fontsize=9, fontweight="bold")

    ax.set_xticks(x + width/2)
    ax.set_xticklabels(pivot.index)
    ax.set_title("Quarterly Revenue — Year-over-Year Comparison")
    ax.set_ylabel("Revenue (₹ Millions)")
    ax.legend(title="Year")
    plt.tight_layout()
    save(fig, "09_quarterly_yoy")


def insight_10_day_of_week(df):
    """INSIGHT 10: Day-of-week patterns"""
    print("\n── Insight 10: Day-of-Week Pattern ──")
    dow_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    dow = (
        df.groupby("day_of_week")
        .agg(revenue=("revenue","sum"), orders=("order_id","count"))
        .reindex(dow_order)
    )

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    bar_colors = [COLORS["primary"] if d not in ["Saturday","Sunday"] else COLORS["accent"] for d in dow.index]

    axes[0].bar(dow.index, dow["revenue"]/1e6, color=bar_colors, edgecolor="white")
    axes[0].set_title("Revenue by Day of Week")
    axes[0].set_ylabel("Revenue (₹ Millions)")
    axes[0].set_xticklabels(dow.index, rotation=30, ha="right")

    axes[1].bar(dow.index, dow["orders"], color=bar_colors, edgecolor="white")
    axes[1].set_title("Order Count by Day of Week")
    axes[1].set_ylabel("Number of Orders")
    axes[1].set_xticklabels(dow.index, rotation=30, ha="right")

    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=COLORS["primary"], label="Weekday"),
                       Patch(facecolor=COLORS["accent"], label="Weekend")]
    axes[0].legend(handles=legend_elements)

    fig.suptitle("Order Pattern by Day of Week", fontsize=14, fontweight="bold", color=COLORS["primary"])
    plt.tight_layout()
    save(fig, "10_day_of_week")


def insight_11_top_reps(df):
    """INSIGHT 11: Top sales representatives"""
    print("\n── Insight 11: Sales Rep Performance ──")
    reps = (
        df.groupby("sales_rep")
        .agg(revenue=("revenue","sum"), orders=("order_id","count"), profit=("profit","sum"))
        .assign(margin=lambda x: x["profit"]/x["revenue"]*100,
                avg_order=lambda x: x["revenue"]/x["orders"])
        .sort_values("revenue", ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(13, 5))
    bars = ax.barh(reps.index[::-1], reps["revenue"][::-1]/1e6,
                   color=[COLORS["primary"] if i < 3 else COLORS["light"] for i in range(len(reps)-1, -1, -1)],
                   edgecolor="white", height=0.6)
    for bar, val, margin in zip(bars, reps["revenue"][::-1]/1e6, reps["margin"][::-1]):
        ax.text(val + 0.1, bar.get_y() + bar.get_height()/2,
                f"₹{val:.1f}M  |  {margin:.0f}% margin",
                va="center", fontsize=9)
    ax.set_title("Top 10 Sales Representatives by Revenue")
    ax.set_xlabel("Revenue (₹ Millions)")
    ax.set_xlim(0, reps["revenue"].max()/1e6 * 1.35)
    plt.tight_layout()
    save(fig, "11_top_sales_reps")


def insight_12_pareto(df):
    """INSIGHT 12: Pareto — 80/20 analysis"""
    print("\n── Insight 12: Pareto (80/20) Analysis ──")
    cat_rev = df.groupby("category")["revenue"].sum().sort_values(ascending=False)
    cumulative = (cat_rev.cumsum() / cat_rev.sum() * 100)

    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax2 = ax1.twinx()

    bars = ax1.bar(cat_rev.index, cat_rev/1e6, color=PALETTE[:len(cat_rev)], edgecolor="white", width=0.5)
    ax2.plot(cat_rev.index, cumulative, color=COLORS["accent"],
             marker="D", linewidth=2.5, markersize=7, label="Cumulative %")
    ax2.axhline(80, color="gray", linestyle="--", linewidth=1.2, alpha=0.7)
    ax2.text(len(cat_rev)-0.5, 81, "80% threshold", color="gray", fontsize=9)

    ax1.set_title("Pareto Analysis — Revenue by Category")
    ax1.set_ylabel("Revenue (₹ Millions)")
    ax2.set_ylabel("Cumulative Revenue %")
    ax2.set_ylim(0, 115)
    ax2.legend(loc="center right")

    plt.tight_layout()
    save(fig, "12_pareto_analysis")


# ─────────────────────────────────────────
# STEP 4: Print Summary Insights
# ─────────────────────────────────────────
def print_insights(df):
    print("\n" + "="*60)
    print("  FINAL INSIGHTS SUMMARY")
    print("="*60)

    insights = [
        ("Revenue",        f"₹{df['revenue'].sum():,.0f} total revenue across {df['order_id'].nunique():,} orders"),
        ("Profit Margin",  f"{df['profit_margin'].mean():.1f}% average margin | {df['profit_margin'].median():.1f}% median"),
        ("Top Region",     f"{df.groupby('region')['revenue'].sum().idxmax()} leads in revenue"),
        ("Best Category",  f"{df.groupby('category')['revenue'].sum().idxmax()} is the top revenue category"),
        ("Best Cust Type", f"Corporate customers have highest avg order value: ₹{df[df['customer_type']=='Corporate']['revenue'].mean():,.0f}"),
        ("Discounts",      f"{(df['discount_pct']==0).mean()*100:.0f}% of orders have NO discount"),
        ("Growth",         f"Revenue peaked in {df.groupby('order_month')['revenue'].sum().idxmax()}"),
        ("Weekend Pattern",f"Weekday orders avg ₹{df[~df['day_of_week'].isin(['Saturday','Sunday'])]['revenue'].mean():,.0f} vs ₹{df[df['day_of_week'].isin(['Saturday','Sunday'])]['revenue'].mean():,.0f} on weekends"),
    ]

    for key, val in insights:
        print(f"\n  📌 {key}:\n     → {val}")

    print(f"\n  📂 All charts saved to: charts/ folder ({12} PNG files)")
    print("\n" + "="*60)


# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
def main():
    print("="*60)
    print("  PROJECT 1 — SALES EDA | Complete Analysis")
    print("="*60)

    # Load data
    df = generate_dataset(n=800)
    # In real project: df = pd.read_csv("sales_data.csv")

    data_overview(df)
    df = clean_data(df)

    print("\n📊 Generating 12 Insights...\n")
    insight_01_revenue_overview(df)
    insight_02_monthly_trend(df)
    insight_03_region_performance(df)
    insight_04_category_analysis(df)
    insight_05_customer_type(df)
    insight_06_profit_distribution(df)
    insight_07_discount_impact(df)
    insight_08_correlation_heatmap(df)
    insight_09_quarterly_comparison(df)
    insight_10_day_of_week(df)
    insight_11_top_reps(df)
    insight_12_pareto(df)

    print_insights(df)
    print("\n✅ EDA Complete! Open charts/ folder to see all visualizations.\n")


if __name__ == "__main__":
    main()
