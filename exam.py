import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import random
import time
from concurrent.futures import ThreadPoolExecutor
import unittest



df = pd.read_csv("C:/Users/admin/Downloads/exam.csv")

# Fix encoding issue 
df["exercise_minutes"] = (
    df["exercise_minutes"]
    .str.replace("â€“", "–", regex=False)
    .str.strip()
)


if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"])

# VISUALIZATIONS 

plt.figure(figsize=(15, 10))

# Steps Distribution
plt.subplot(3, 2, 1)
plt.hist(df["steps"], bins=10, color="skyblue", edgecolor="black")
plt.title("Steps Distribution")
plt.xlabel("Steps")
plt.ylabel("Frequency")

# Gender Distribution
plt.subplot(3, 2, 2)
gender_counts = df["Gender"].value_counts()
plt.bar(gender_counts.index, gender_counts.values, color=["pink", "lightblue"])
plt.title("Gender Distribution")
plt.xlabel("Gender")
plt.ylabel("Count")

# Sleep Hours Distribution
plt.subplot(3, 2, 3)
plt.hist(df["sleep_hours"], bins=8, color="lightgreen", edgecolor="black")
plt.title("Sleep Hours Distribution")
plt.xlabel("Hours")
plt.ylabel("Frequency")

# Heart Rate Distribution
plt.subplot(3, 2, 4)
plt.hist(df["heart_rate"], bins=10, color="salmon", edgecolor="black")
plt.title("Heart Rate Distribution")
plt.xlabel("BPM")
plt.ylabel("Frequency")

# Exercise Duration
plt.subplot(3, 2, 5)
exercise_counts = df["exercise_minutes"].value_counts()
plt.bar(exercise_counts.index, exercise_counts.values, color="orange")
plt.title("Daily Exercise Duration")
plt.xlabel("Exercise Time")
plt.ylabel("Count")
plt.xticks(rotation=20)

plt.tight_layout()
plt.savefig("fitness_visualization_report.png")
plt.show()



def upload_fitness_data(user_id):
    steps = random.randint(1000, 15000)
    heart_rate = random.randint(60, 100)
    sleep_hours = round(random.uniform(5, 9), 1)

    # Simulate network / processing delay
    time.sleep(0.5)

    return f"User {user_id}: Steps={steps}, HR={heart_rate}, Sleep={sleep_hours}"

# Sequential processing
def run_sequential(num_users=10):
    start_time = time.time()
    for user in range(num_users):
        print(upload_fitness_data(user))
    end_time = time.time()
    return end_time - start_time

# Multithreaded processing
def run_parallel(num_users=10):
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(upload_fitness_data, range(num_users))
        for result in results:
            print(result)
    end_time = time.time()
    return end_time - start_time

# Run comparison
if __name__ == "__main__":
    print("Running sequential processing...")
    seq_time = run_sequential()

    print("\nRunning multithreaded processing...")
    par_time = run_parallel()

    print("\n--- Performance Comparison ---")
    print(f"Sequential Time: {seq_time:.2f} seconds")
    print(f"Multithreaded Time: {par_time:.2f} seconds")
    print(f"Speed Improvement: {seq_time / par_time:.2f}x faster")




#  Error Handling and Testing
def validate_data(steps, heart_rate, sleep_hours):
    if steps is None or heart_rate is None or sleep_hours is None:
        raise ValueError("Missing data detected")
    if steps < 0:
        raise ValueError("Invalid steps value")
    if heart_rate <= 0:
        raise ValueError("Invalid heart rate value")
    if sleep_hours <= 0 or sleep_hours > 24:
        raise ValueError("Invalid sleep duration")
    return True


class TestFitnessData(unittest.TestCase):

    # This test PASS
    def test_valid_data(self):
        self.assertTrue(validate_data(8000, 72, 7.5))

    # This test FAIL
    def test_invalid_sleep(self):
        self.assertTrue(validate_data(7000, 70, 30))  # 30 hours is invalid



if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)