
<p align='center'>
    <img width=1024 src="Repo_Img\Repo_img_01.png">
</p>

#  🐧 Palmer Penguins Descriptive Analysis 🐧

*Comprehensive Exploratory Data Analysis using Python*

---

## Repository Information
- **Repository:** [Penguins-EDA-Wizard](https://github.com/MalakaSupun/Penguins-EDA-Wizard)
- **Dataset:** Palmer Penguins (344 observations, 7 variables)
- **Tools:** Python (pandas, seaborn, matplotlib, scipy)

---

## 📋 1. Introduction

This report presents a descriptive analysis of the Palmer Penguins dataset, which records physical measurements for 344 penguins across three species (Adelie, Chinstrap, and Gentoo) sampled from three islands in the Palmer Archipelago, Antarctica.

The dataset contains four numeric variables — bill length, bill depth, flipper length, and body mass — and three categorical variables: species, island, and sex.

### Goals of this analysis:
1. Compute descriptive statistics for each variable
2. Visualize the distribution and behavior of each variable
3. Examine how numeric variables differ across categories (species, island, sex)
4. Draw conclusions from observed patterns and relationships

---

## 🔍 2. Dataset Overview

### Variables

**Categorical Variables:**
- `species` — Adelie, Chinstrap, Gentoo
- `island` — Biscoe, Dream, Torgersen
- `sex` — Male, Female (11 missing values)

**Numeric Variables:**
- `bill_length_mm`
- `bill_depth_mm`
- `flipper_length_mm`
- `body_mass_g`

> **Data Quality Note:** Two rows were missing all four numeric measurements and were excluded from the numeric analysis, leaving 342 usable records. All categorical variables retain their full counts where relevant.

---

## 📊 3. Descriptive Statistics — Numeric Variables

All four numeric variables have skewness close to zero (between -0.14 and 0.47), indicating roughly symmetric distributions with a slight right-skew for body mass. Negative kurtosis values (around -0.7 to -1.0) indicate flatter-than-normal distributions — consistent with three distinct species creating multiple humps rather than one sharp peak.

| Variable | N | Mean | Median | Std Dev | Min | Max | Skew |
|----------|---|------|--------|---------|-----|-----|------|
| Bill length (mm) | 342 | 43.92 | 44.45 | 5.46 | 32.1 | 59.6 | 0.05 |
| Bill depth (mm) | 342 | 17.15 | 17.30 | 1.97 | 13.1 | 21.5 | -0.14 |
| Flipper length (mm) | 342 | 200.92 | 197.00 | 14.06 | 172.0 | 231.0 | 0.35 |
| Body mass (g) | 342 | 4201.75 | 4050.00 | 801.95 | 2700 | 6300 | 0.47 |

---

## 🎯 4. Descriptive Statistics — Categorical Variables

![Categorical Variable Counts](figs/03_categorical_counts.png)
*Figure 1: Distribution of observations by species, island, and sex*

### Species Counts

| Species | Count | Percent |
|---------|-------|---------|
| Adelie | 152 | 44.2% |
| Gentoo | 124 | 36.0% |
| Chinstrap | 68 | 19.8% |

### Island Counts

| Island | Count | Percent |
|--------|-------|---------|
| Biscoe | 168 | 48.8% |
| Dream | 124 | 36.0% |
| Torgersen | 52 | 15.1% |

### Sex Counts

| Sex | Count | Percent |
|-----|-------|---------|
| Male | 168 | 50.5% |
| Female | 165 | 49.5% |

**Key Findings:** Adelie is the most common species (44.2%), and Biscoe is the most-sampled island (48.8%). Sex is almost perfectly balanced (50.5% male vs. 49.5% female).

---

## 📈 5. Distribution of Numeric Variables

![Histograms by Species](figs/01_histograms.png)
*Figure 2: Histograms of the four numeric variables, colored by species*

Each histogram reveals that the apparent single distribution is actually a mixture of three species-specific sub-distributions. **Bill depth** and **body mass** show the clearest separation, with Gentoo penguins standing apart from Adelie and Chinstrap.

![Correlation Matrix](figs/04_correlation_heatmap.png)
*Figure 3: Correlation matrix of the numeric variables*

### Correlation Insights:
- **Flipper length & Body mass:** Strong positive correlation (r ≈ 0.87) — as expected for overall body size
- **Bill depth vs. other variables:** Negatively correlated with flipper length (r ≈ -0.58) and body mass (r ≈ -0.47) — a between-species effect
- **Species Effect:** Gentoo penguins have long flippers, high body mass, and shallow bills, while Adelie/Chinstrap show the opposite pattern

---

## 🎲 6. Behavior of Variables by Category

### 6.1 By Species

![Boxplots by Species](figs/02_boxplots_species.png)
*Figure 4: Boxplots of each numeric variable by species*

**Species is the dominant source of variation** in this dataset:

- **Gentoo penguins** are markedly larger (body mass, flipper length) but have notably shallower bills than the other two species
- **Adelie** has the shortest bill length
- **Chinstrap** and Gentoo have similar bill lengths but very different bill depths and body sizes

#### Mean Measurements by Species

| Species | Mean Bill Length (mm) | Mean Bill Depth (mm) | Mean Flipper Length (mm) | Mean Body Mass (g) |
|---------|----------------------|----------------------|--------------------------|-------------------|
| Adelie | 38.79 | 18.35 | 189.95 | 3700.66 |
| Chinstrap | 48.83 | 18.42 | 195.82 | 3733.09 |
| Gentoo | 47.50 | 14.98 | 217.19 | 5076.02 |

**Statistical Significance:** One-way ANOVA confirms these differences are statistically significant for:
- Body mass (F = 343.6, p < 0.001)
- Bill length (F = 410.6, p < 0.001)

### 6.2 By Island

![Species Composition by Island](figs/07_species_by_island.png)
*Figure 5: Species composition by island*

> **⚠️ Island Confounding:** Island is **not** an independent grouping factor — it is almost a proxy for species:
> - Torgersen contains **only** Adelie penguins
> - Dream contains Adelie and Chinstrap
> - Biscoe contains Adelie and Gentoo
> 
> As a result, apparent differences in measurements 'by island' (e.g., higher average body mass on Biscoe) are largely driven by which species happen to live there, rather than an island effect in itself.

### 6.3 By Sex

![Body Mass by Species and Sex](figs/06_bodymass_species_sex.png)
*Figure 6: Mean body mass by species and sex, with standard deviation error bars*

Within every species, **males are consistently heavier than females** — a pattern known as **sexual size dimorphism**. The gap is present across all three species, meaning sex and species act as independent, additive sources of variation in body mass rather than one masking the other.

### 6.4 Pairwise Relationships

![Pairwise Scatterplots](figs/05_pairplot.png)
*Figure 7: Pairwise scatterplots and marginal distributions for all numeric variables, colored by species*

The pairplot shows that combinations of just two variables (e.g., bill length and bill depth, or flipper length and bill depth) are enough to separate the three species almost perfectly into distinct clusters. This suggests the four numeric measurements together carry strong discriminative information about species identity.

---

## ✅ 7. Conclusions

1. **Species Dominance:** Species is the primary driver of variation in all four numeric variables. Gentoo penguins are distinctly larger with shallower bills; Adelie has the shortest bills; Chinstrap sits between Adelie and Gentoo on most measures but overlaps closely with Gentoo on bill length.

2. **Island Confounding:** Island differences are confounded with species — each island hosts a different subset of species, so island-level averages mainly reflect species composition rather than a geographic effect.

3. **Sexual Dimorphism:** Sex creates a consistent, additive effect: males are heavier than females within every species, indicating sexual dimorphism independent of species differences.

4. **Bivariate Relationships:** Flipper length and body mass are strongly correlated (larger-bodied birds have longer flippers), while bill depth behaves almost inversely to overall body size across species — driven by Gentoo's unusually shallow bill relative to its large body.

5. **Distribution Properties:** All four numeric variables are reasonably symmetric (low skew) but flatter than a normal distribution (negative kurtosis), which is explained by the underlying three-species mixture rather than any single well-behaved population distribution.

6. **Practical Implication:** Species can be predicted with high accuracy from just two of the four numeric measurements (e.g., bill length and bill depth), as shown in the pairplot clustering — a useful basis for a simple classification exercise as a follow-up to this descriptive analysis.

---

## 📚 Tools & Technologies

- **Python** — Data analysis and visualization
- **pandas** — Data manipulation and analysis
- **matplotlib & seaborn** — Statistical visualization
- **scipy** — Statistical testing and analysis

---

**Last Updated:** 2026  
**Repository:** [Penguins-EDA-Wizard](https://github.com/MalakaSupun/Penguins-EDA-Wizard)
