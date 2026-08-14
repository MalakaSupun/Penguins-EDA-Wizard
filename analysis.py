import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

os.makedirs("figs", exist_ok=True)
sns.set_theme(style="whitegrid", palette="Set2")
plt.rcParams["figure.dpi"] = 150

df = pd.read_csv("Data\penguins.csv")

numeric_cols = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
categorical_cols = ["species", "island", "sex"]

df_clean = df.dropna(subset=numeric_cols).copy()

# ------------------------------------------------------------------
# 1. DESCRIPTIVE STATISTICS - NUMERIC
# ------------------------------------------------------------------
desc_rows = []
for col in numeric_cols:
    s = df_clean[col]
    mode_val = s.mode().iloc[0] if not s.mode().empty else np.nan
    desc_rows.append({
        "Variable": col,
        "N": s.count(),
        "Mean": round(s.mean(), 2),
        "Median": round(s.median(), 2),
        "Mode": round(mode_val, 2),
        "Std Dev": round(s.std(), 2),
        "Variance": round(s.var(), 2),
        "Min": round(s.min(), 2),
        "Max": round(s.max(), 2),
        "Range": round(s.max() - s.min(), 2),
        "Q1": round(s.quantile(0.25), 2),
        "Q3": round(s.quantile(0.75), 2),
        "IQR": round(s.quantile(0.75) - s.quantile(0.25), 2),
        "Skewness": round(s.skew(), 3),
        "Kurtosis": round(s.kurtosis(), 3),
        "CV%": round(s.std() / s.mean() * 100, 2),
    })
desc_numeric = pd.DataFrame(desc_rows)
desc_numeric.to_csv("tables/desc_numeric.csv", index=False)
print(desc_numeric.to_string(index=False))

# ------------------------------------------------------------------
# 2. DESCRIPTIVE STATISTICS - CATEGORICAL (frequency tables)
# ------------------------------------------------------------------
print("\n--- Categorical frequency tables ---")
for col in categorical_cols:
    freq = df[col].value_counts(dropna=True)
    pct = (freq / freq.sum() * 100).round(1)
    tab = pd.DataFrame({"Count": freq, "Percent": pct})
    print(f"\n{col}:\n{tab}")
    tab.to_csv(f"freq_{col}.csv")

# ------------------------------------------------------------------
# 3. GRAPHS - Distribution of each numeric variable (histogram + KDE)
# ------------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(11, 8))
for ax, col in zip(axes.flat, numeric_cols):
    sns.histplot(df_clean, x=col, hue="species", kde=True, ax=ax, alpha=0.6, legend=(col == numeric_cols[0]))
    ax.set_title(f"Distribution of {col}")
plt.tight_layout()
plt.savefig("figs/01_histograms.png", bbox_inches="tight")
plt.close()

# ------------------------------------------------------------------
# 4. GRAPHS - Boxplots of each numeric variable by species
# ------------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(11, 8))
for ax, col in zip(axes.flat, numeric_cols):
    sns.boxplot(df_clean, x="species", y=col, ax=ax, hue="species", legend=False)
    ax.set_title(f"{col} by Species")
plt.tight_layout()
plt.savefig("figs/02_boxplots_species.png", bbox_inches="tight")
plt.close()

# ------------------------------------------------------------------
# 5. GRAPHS - Categorical bar charts
# ------------------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))
for ax, col in zip(axes, categorical_cols):
    order = df[col].value_counts(dropna=True).index
    sns.countplot(df.dropna(subset=[col]), x=col, order=order, ax=ax, hue=col, legend=False)
    ax.set_title(f"Count by {col}")
    ax.set_xlabel("")
plt.tight_layout()
plt.savefig("figs/03_categorical_counts.png", bbox_inches="tight")
plt.close()

# ------------------------------------------------------------------
# 6. GRAPHS - Correlation heatmap
# ------------------------------------------------------------------
plt.figure(figsize=(6, 5))
corr = df_clean[numeric_cols].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1, fmt=".2f")
plt.title("Correlation Matrix - Numeric Variables")
plt.tight_layout()
plt.savefig("figs/04_correlation_heatmap.png", bbox_inches="tight")
plt.close()

# ------------------------------------------------------------------
# 7. GRAPHS - Pairwise scatter matrix colored by species
# ------------------------------------------------------------------
g = sns.pairplot(df_clean, vars=numeric_cols, hue="species", diag_kind="kde", height=2.1, plot_kws={"alpha": 0.6, "s": 25})
g.fig.suptitle("Pairwise Relationships Between Numeric Variables", y=1.02)
g.savefig("figs/05_pairplot.png", bbox_inches="tight")
plt.close()

# ------------------------------------------------------------------
# 8. GROUPED ANALYSIS - behavior of variables by category
# ------------------------------------------------------------------
print("\n--- Grouped means by species ---")
grouped_species = df_clean.groupby("species")[numeric_cols].agg(["mean", "std", "count"]).round(2)
print(grouped_species)
grouped_species.to_csv("tables/grouped_species.csv")

print("\n--- Grouped means by island ---")
grouped_island = df_clean.groupby("island")[numeric_cols].agg(["mean", "std", "count"]).round(2)
print(grouped_island)
grouped_island.to_csv("tables/grouped_island.csv")

print("\n--- Grouped means by sex ---")
df_sex = df_clean.dropna(subset=["sex"])
grouped_sex = df_sex.groupby("sex")[numeric_cols].agg(["mean", "std", "count"]).round(2)
print(grouped_sex)
grouped_sex.to_csv("tables/grouped_sex.csv")

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(df_sex, x="species", y="body_mass_g", hue="sex", ax=ax, errorbar="sd")
ax.set_title("Mean Body Mass by Species and Sex")
ax.set_ylabel("Body Mass (g)")
plt.tight_layout()
plt.savefig("figs/06_bodymass_species_sex.png", bbox_inches="tight")
plt.close()

fig, ax = plt.subplots(figsize=(8, 5))
comp = pd.crosstab(df["island"], df["species"])
comp.plot(kind="bar", stacked=True, ax=ax, colormap="Set2")
ax.set_title("Species Composition by Island")
ax.set_ylabel("Count")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("figs/07_species_by_island.png", bbox_inches="tight")
plt.close()
print("\nCrosstab island x species:")
print(comp)
comp.to_csv("tables/crosstab_island_species.csv")

# ------------------------------------------------------------------
# 9. ANOVA checks
# ------------------------------------------------------------------
groups = [g["body_mass_g"].values for _, g in df_clean.groupby("species")]
f_stat, p_val = stats.f_oneway(*groups)
print(f"\nOne-way ANOVA (body_mass_g by species): F={f_stat:.2f}, p={p_val:.2e}")

groups_bl = [g["bill_length_mm"].values for _, g in df_clean.groupby("species")]
f_stat2, p_val2 = stats.f_oneway(*groups_bl)
print(f"One-way ANOVA (bill_length_mm by species): F={f_stat2:.2f}, p={p_val2:.2e}")

print("\nDone. Figures in figs/, tables as CSV in current dir.")
