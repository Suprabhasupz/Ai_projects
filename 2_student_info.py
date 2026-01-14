import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def analyze_student_scores():
    """
    Fetches student test score data from a public API, calculates the
    average score, and visualizes the scores using a bar chart.
    """

    # Fetch data from API
    url = "https://fakestoreapi.com/products"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return

    # Extract scores (using product price as score)
    scores = [item["price"] for item in data]

    if not scores:
        print("No scores found.")
        return

    # Calculate average scores
    average_score = np.mean(scores)

    df = pd.DataFrame(data)
    average_score_pd = df["price"].mean()

    print(f"Average score using NumPy: {average_score:.2f}")
    print(f"Average score using Pandas: {average_score_pd:.2f}")

    # Prepare data for visualization
    names = [item["title"][:20] + "..." for item in data]
    values = scores

    # Plot bar chart
    plt.figure(figsize=(12, 7))
    plt.bar(names, values)
    plt.axhline(average_score, linestyle="dashed", linewidth=2, label="Average Score")

    plt.xlabel("Student / Item Name")
    plt.ylabel("Score")
    plt.title("Student Scores Visualization")
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    analyze_student_scores()
