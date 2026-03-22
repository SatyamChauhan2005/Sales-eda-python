# Sales-eda-python

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Pandas](https://img.shields.io/badge/Pandas-2.0-green)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7-orange)
![Seaborn](https://img.shields.io/badge/Seaborn-0.12-red)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

## Overview
Complete Exploratory Data Analysis (EDA) on a sales dataset containing
800+ orders across 5 regions, 6 product categories, and 3 customer types
covering the period January 2023 to July 2024.

**Author:** Satyam Chauhan | MIS Executive → Data Analyst
**Tools:** Python | Pandas | NumPy | Matplotlib | Seaborn

---

## Business Questions Answered
- Which regions and categories drive the most revenue?
- How does revenue and profit trend month by month?
- Do discounts help or hurt profitability?
- Which customer type — Retail, Corporate or SMB — is most valuable?
- Who are the top performing sales representatives?
- Which 20% of categories make 80% of total revenue? (Pareto Rule)

---

## Key Findings
1. **North region** leads with the highest revenue share
2. **Corporate customers** generate 2.5x higher average order value than Retail
3. **Discounts above 10%** reduce profit margins by ~8 percentage points
4. **Top 2 categories** drive 60%+ of total revenue — Pareto rule confirmed
5. **Q4** shows consistent 20%+ revenue spike compared to Q2
6. **Accessories** category has the highest volume of units sold

---

## 12 Charts Generated

| # | Chart | Business Insight |
|---|-------|-----------------|
| 01 | KPI Overview | Total Revenue, Profit, Margin, Orders |
| 02 | Monthly Trend | Revenue and profit trend month by month |
| 03 | Region Performance | Revenue by region — bar and pie chart |
| 04 | Category Analysis | Revenue vs profit margin bubble chart |
| 05 | Customer Type | Retail vs Corporate vs SMB comparison |
| 06 | Profit Distribution | Margin histogram and box plot by category |
| 07 | Discount Impact | How discount bands affect profit margin |
| 08 | Correlation Heatmap | Correlation between all numerical variables |
| 09 | Quarterly YoY | Year over year quarterly comparison |
| 10 | Day of Week | Weekday vs weekend order patterns |
| 11 | Top Sales Reps | Top 10 representatives by revenue |
| 12 | Pareto Analysis | 80/20 rule — which categories drive revenue |

---

## Project Structure

```
Sales-eda-python/
│
├── sales_eda.py            <- Main Python analysis script
├── README.md               <- Project documentation
│
├── 01_kpi_overview.png
├── 02_monthly_trend.png
├── 03_region_performance.png
├── 04_category_analysis.png
├── 05_customer_type.png
├── 06_profit_distribution.png
├── 07_discount_impact.png
├── 08_correlation_heatmap.png
├── 09_quarterly_yoy.png
├── 10_day_of_week.png
├── 11_top_sales_reps.png
└── 12_pareto_analysis.png
```

---

## How to Run

**Step 1 — Clone this repository**
```bash
git clone https://github.com/SatyamChauhan2005/Sales-eda-python.git
cd Sales-eda-python
```

**Step 2 — Install required libraries**
```bash
pip install pandas numpy matplotlib seaborn
```

**Step 3 — Run the script**
```bash
python sales_eda.py
```

**Step 4 — View your charts**
All 12 charts will be saved automatically in the same folder.

---

## Libraries Used

| Library | Purpose |
|---------|---------|
| Pandas | Data loading, cleaning, groupby analysis |
| NumPy | Numerical operations and array handling |
| Matplotlib | Chart creation and customization |
| Seaborn | Statistical visualizations and heatmaps |

---

## About Me
I am an MIS Executive transitioning into Data Analytics.
This is Project 1 of my Data Analyst portfolio.

**Skills:** Python | SQL | Power BI | Google Sheets | MySQL | App Script

