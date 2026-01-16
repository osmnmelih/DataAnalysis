import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from rich.console import Console
from rich.table import Table

# Initialize Console for professional output
console = Console()

# =============================================================================
# PART 1: DATA LOADING AND EXPLORATION
# =============================================================================
console.print("[bold cyan]Initializing Learning Science Analysis...[/bold cyan]\n")

# Load the Data
df = pd.read_csv('math_practice_data.csv')
console.print(f"Data loaded successfully! Total records: {len(df)}")

# =============================================================================
# PART 2: DEFINING RESEARCH GROUPS (Early vs. Late)
# =============================================================================
# Early Group: Sessions 1-5
# Late Group: Sessions 11-15
group_early = df[df['session_number'] <= 5]['is_correct'].astype(int)
group_late = df[df['session_number'] >= 11]['is_correct'].astype(int)

# =============================================================================
# PART 3: GROUP STATISTICS (SPSS Style)
# =============================================================================
def get_stats(group):
    return {
        'N': len(group),
        'Mean': group.mean(),
        'Std. Dev': group.std(),
        'Std. Error': group.std() / np.sqrt(len(group))
    }

stats_early = get_stats(group_early)
stats_late = get_stats(group_late)

group_table = Table(title="[bold blue]Table 1: Group Statistics[/bold blue]")
group_table.add_column("Session Group", style="cyan")
group_table.add_column("N", justify="right")
group_table.add_column("Mean (Success Rate)", justify="right")
group_table.add_column("Std. Deviation", justify="right")
group_table.add_column("Std. Error Mean", justify="right")

group_table.add_row("Early Sessions (1-5)", str(stats_early['N']), f"{stats_early['Mean']:.4f}", f"{stats_early['Std. Dev']:.4f}", f"{stats_early['Std. Error']:.4f}")
group_table.add_row("Late Sessions (11-15)", str(stats_late['N']), f"{stats_late['Mean']:.4f}", f"{stats_late['Std. Dev']:.4f}", f"{stats_late['Std. Error']:.4f}")

console.print(group_table)

# =============================================================================
# PART 4: INDEPENDENT SAMPLES T-TEST
# =============================================================================
# Levene's Test for Equality of Variances
levene_stat, levene_p = stats.levene(group_early, group_late)

# Independent T-test
t_stat, p_val = stats.ttest_ind(group_late, group_early)

# Calculate 95% Confidence Interval
mean_diff = stats_late['Mean'] - stats_early['Mean']
se_diff = np.sqrt(stats_early['Std. Error']**2 + stats_late['Std. Error']**2)
ci_low, ci_high = stats.t.interval(0.95, len(group_early) + len(group_late) - 2, loc=mean_diff, scale=se_diff)

ttest_table = Table(title="[bold blue]Table 2: Independent Samples Test[/bold blue]")
ttest_table.add_column("Statistical Metric", style="magenta")
ttest_table.add_column("Value", justify="right")

ttest_table.add_row("Levene's Test (p-value)", f"{levene_p:.4f}")
ttest_table.add_row("t-value", f"{t_stat:.4f}")
ttest_table.add_row("Degrees of Freedom (df)", str(len(group_early) + len(group_late) - 2))
ttest_table.add_row("Sig. (2-tailed / p-value)", f"{p_val:.4f}")
ttest_table.add_row("Mean Difference", f"{mean_diff:.4f}")
ttest_table.add_row("95% CI Lower Bound", f"{ci_low:.4f}")
ttest_table.add_row("95% CI Upper Bound", f"{ci_high:.4f}")

console.print(ttest_table)

if p_val < 0.05:
    console.print(f"\n[bold green]RESEARCH FINDING:[/bold green] Significant learning gains observed (p < .05). "
                  f"Average success rate increased by {mean_diff*100:.1f}%.")

# =============================================================================
# PART 5: VISUALIZATION (Generating learning_curve.png)
# =============================================================================
console.print("\n[bold yellow]Generating Learning Curve visualization...[/bold yellow]")

plt.figure(figsize=(10, 6))
sns.set_theme(style="whitegrid")

# Calculate success rate per session
session_trend = df.groupby('session_number')['is_correct'].mean() * 100

# Plotting
sns.lineplot(x=session_trend.index, y=session_trend.values, marker='o', color='#2ecc71', linewidth=2.5)

plt.title('Learning Curve: Success Rate Evolution Over Sessions', fontsize=14, fontweight='bold')
plt.xlabel('Session Number', fontsize=12)
plt.ylabel('Success Rate (%)', fontsize=12)
plt.ylim(0, 100)

# SAVE THE IMAGE
plt.savefig('learning_curve.png', dpi=300)
console.print("[bold green][SUCCESS] 'learning_curve.png' has been saved to your project folder.[/bold green]")