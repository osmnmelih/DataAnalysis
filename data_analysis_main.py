# =============================================================================
# PART 1: SETUP AND EXPLORATION
# =============================================================================

# Step 1: Import Pandas
import pandas as pd

print("Pandas imported successfully!")
print()

# Step 2: Load the Data
df=pd.read_csv('math_practice_data.csv')

print("Data loaded successfully!")
print(f"Total records: {len(df)}")
print()

# Step 3: Basic Exploration
print("="*50)
print("BASIC DATA EXPLORATION")
print("="*50)

# Display first 10 rows (use .head(10))
print(df.head(10))


# Display dataset shape (use .shape)
print("\nShape:", df.shape)


# Display column names (use .columns)
print("\nColumns:")
print(df.columns)

# Display summary statistics for numeric columns (use .describe())
print("\nSummary Statistics:")
print(df.describe())

print()
# =============================================================================
# PART 2: SIMPLE FILTERING
# =============================================================================

# Step 4: Find Correct Answers
print("="*50)
print("CORRECT ANSWERS")
print("="*50)

# Filter to show only correct answers
correct_answers = df[df['is_correct'] == True]

# Display total count and first 5 rows
print(f"Total correct answers: {len(correct_answers)}")
print(correct_answers.head(5))

print()

# Step 5: Find Slow Problems
print("="*50)
print("SLOWEST PROBLEMS (>20 seconds)")
print("="*50)

# Filter for time_spent_seconds > 20
slow_problems = df[df['time_spent_seconds'] > 20]

# Sort by time_spent_seconds from highest to lowest
slow_problems = slow_problems.sort_values(by='time_spent_seconds', ascending=False)


# Display top 10
print(slow_problems.head(10))


print()

# Step 6: Find Specific Operation
print("="*50)
print("MULTIPLICATION PROBLEMS")
print("="*50)

# Filter for operation == 'Multiplication'
multiplication = df[df['operation'] == 'Multiplication']


# Count total and display first 5
print(f"Total multiplication problems: {len(multiplication)}")
print(multiplication.head(5))

print()

# Step 7: Find Difficult Problems
print("="*50)
print("HARD DIFFICULTY PROBLEMS")
print("="*50)

# Filter for difficulty_level == 'Hard'
hard_problems = df[df['difficulty_level'] == 'Hard']


# Count total and display first 10
print(f"Total hard problems: {len(hard_problems)}")
print(hard_problems.head(10))

print()

# =============================================================================
# PART 3: COMBINING CONDITIONS
# =============================================================================

# Step 8: Wrong Multiplication Problems
print("="*50)
print("INCORRECT MULTIPLICATION")
print("="*50)

# Find problems that are BOTH:
# - Multiplication operation
# - Incorrect answer
wrong_multiplication = df[
    (df['operation'] == 'Multiplication') &
    (df['is_correct'] == False)
]
# Count total and display first 10
print(f"Total incorrect multiplication problems: {len(wrong_multiplication)}")
print(wrong_multiplication.head(10))

print()

# Step 9: Quick Correct Answers
print("="*50)
print("QUICK & CORRECT (< 10 seconds)")
print("="*50)

# Find problems that are BOTH:
quick_correct = df[
    (df['is_correct'] == True) &
    (df['time_spent_seconds'] < 10)
]

# Sort by time from fastest to slowest
quick_correct = quick_correct.sort_values(by='time_spent_seconds')


# Display first 10
print(quick_correct.head(10))


print()

# Step 10: Struggling with Hard Problems
print("="*50)
print("STRUGGLING WITH HARD PROBLEMS")
print("="*50)

# Find attempts where ALL THREE are true:
struggling_hard = df[
    (df['difficulty_level'] == 'Hard') &
    (df['is_correct'] == False) &
    (df['attempts_needed'] > 2)
]

# Count total and display first 10
print(f"Total struggling attempts: {len(struggling_hard)}")
print(struggling_hard.head(10))


print()

# Step 11: Early Sessions vs Late Sessions
print("="*50)
print("IMPROVEMENT OVER TIME")
print("="*50)

# Filter for early practice (session_number <= 5)
early_practice = df[df['session_number'] <= 5]

# Calculate: count problems and success rate (mean of is_correct * 100)
early_success = early_practice['is_correct'].mean() * 100


print(f"Early Sessions (1-5): {len(early_practice)} problems, "
      f"{early_success:.1f}% success rate")

# Filter for late practice (session_number >= 11)
late_sessions = df[df['session_number'] >= 11]
late_success = late_sessions['is_correct'].mean() * 100

# Calculate: count problems and success rate
print(f"Late Sessions (11-15): {len(late_sessions)} problems, "
      f"{late_success:.1f}% success rate")


# Calculate improvement
improvement = late_success - early_success
print(f"Improvement: {improvement:.1f}% better!")
print()

# =============================================================================
# PART 4: FINDING EXTREMES
# =============================================================================

# Step 12: Fastest and Slowest
print("="*50)
print("FASTEST AND SLOWEST PROBLEMS")
print("="*50)

# Find the fastest problem (minimum time_spent_seconds)
fastest_problem = df[df['time_spent_seconds'] == df['time_spent_seconds'].min()]

print("Fastest Problem:")
print(fastest_problem[['student_id', 'problem', 'time_spent_seconds']])

# Find the slowest problem (maximum time_spent_seconds)
slowest_problem = df[df['time_spent_seconds'] == df['time_spent_seconds'].max()]
print("\nSlowest Problem:")
print(slowest_problem[['student_id', 'problem', 'time_spent_seconds']])
print()

# Step 13: Most Attempts Needed
print("="*50)
print("PROBLEMS NEEDING MOST ATTEMPTS")
print("="*50)

# Find the maximum number of attempts needed
max_attempts = df['attempts_needed'].max()
print(f"Maximum attempts needed: {max_attempts}")

# Filter for problems that needed this many attempts
most_difficult = df[df['attempts_needed'] == max_attempts]
print(f"\nProblems requiring {max_attempts} attempts:")
print(most_difficult[['student_id', 'problem', 'attempts_needed', 'operation']])
print()

print("="*50)
print("ANALYSIS COMPLETE!")
print("="*50)
print("\nGreat work!!")

# =============================================================================

# performance analysis
print("="*50)
print("PERFORMANCE BY OPERATION")
print("="*50)

operation_stats = (
    df
    .groupby('operation')
    .agg(
        total_problems=('problem', 'count'),
        avg_time=('time_spent_seconds', 'mean'),
        success_rate=('is_correct', 'mean'),
        avg_attempts=('attempts_needed', 'mean')
    )
)

operation_stats['success_rate'] *= 100
print(operation_stats)

# MAKE BEAUTIFUL VISUALIZATION !!!
from rich.console import Console
from rich.table import Table

console = Console()

table = Table(title="📊 Operation Performance Summary")

table.add_column("Operation", style="cyan")
table.add_column("Problems", justify="right")
table.add_column("Avg Time (s)", justify="right")
table.add_column("Success Rate (%)", justify="right")

for op, row in operation_stats.iterrows():
    table.add_row(
        op,
        str(row['total_problems']),
        f"{row['avg_time']:.1f}",
        f"{row['success_rate']:.1f}"
    )

console.print(table)

# =============================================================================

print("Awesome effort!!!")
print("ENJOY!!!")

