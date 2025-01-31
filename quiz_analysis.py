import requests
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns

# API endpoints
CURRENT_QUIZ_API = "https://api.example.com/current_quiz"
HISTORICAL_QUIZ_API = "https://api.example.com/historical_quizzes"

def fetch_current_quiz_data(user_id):
    """Fetch current quiz data for a given user"""
    response = requests.get(f"{CURRENT_QUIZ_API}/{user_id}")
    return response.json()

def fetch_historical_quiz_data(user_id):
    """Fetch historical quiz data for a given user"""
    response = requests.get(f"{HISTORICAL_QUIZ_API}/{user_id}")
    return response.json()

def analyze_quiz_performance(current_quiz, historical_quizzes):
    """Analyze quiz performance and generate insights"""
    # Combine current and historical quiz data
    all_quizzes = [current_quiz] + historical_quizzes
    
    # Create a DataFrame for analysis
    df = pd.DataFrame(all_quizzes)
    
    # Calculate overall performance metrics
    avg_score = df['score'].mean()
    score_trend = df['score'].diff().mean()
    
    # Analyze performance by topic
    topic_performance = df.groupby('topic')['score'].mean().sort_values(ascending=False)
    
    # Analyze performance by difficulty level
    difficulty_performance = df.groupby('difficulty')['score'].mean().sort_values(ascending=False)
    
    # Identify weak areas
    weak_topics = topic_performance[topic_performance < avg_score].index.tolist()
    
    return {
        'avg_score': avg_score,
        'score_trend': score_trend,
        'topic_performance': topic_performance,
        'difficulty_performance': difficulty_performance,
        'weak_topics': weak_topics
    }

def generate_recommendations(analysis):
    """Generate personalized recommendations based on the analysis"""
    recommendations = []
    
    if analysis['score_trend'] < 0:
        recommendations.append("Your scores are trending downward. Consider increasing your study time.")
    
    for topic in analysis['weak_topics'][:3]:
        recommendations.append(f"Focus on improving your knowledge in {topic}.")
    
    if analysis['difficulty_performance'].index[0] == 'easy':
        recommendations.append("Challenge yourself with more difficult questions to improve overall performance.")
    
    return recommendations

def predict_neet_rank(user_performance, previous_year_results):
    """Predict NEET rank based on quiz performance and previous year results"""
    # Combine user performance with previous year results
    data = pd.concat([user_performance, previous_year_results])
    
    # Prepare features and target
    X = data[['avg_score', 'topic_coverage', 'difficulty_level']]
    y = data['neet_rank']
    
    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train a Random Forest model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Make prediction for the user
    user_features = user_performance[['avg_score', 'topic_coverage', 'difficulty_level']]
    predicted_rank = model.predict(user_features)
    
    return predicted_rank[0]

def visualize_performance(analysis):
    """Create visualizations for key insights"""
    # Topic performance bar plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x=analysis['topic_performance'].index, y=analysis['topic_performance'].values)
    plt.title("Performance by Topic")
    plt.xlabel("Topic")
    plt.ylabel("Average Score")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("topic_performance.png")
    plt.close()
    
    # Difficulty performance bar plot
    plt.figure(figsize=(8, 5))
    sns.barplot(x=analysis['difficulty_performance'].index, y=analysis['difficulty_performance'].values)
    plt.title("Performance by Difficulty Level")
    plt.xlabel("Difficulty")
    plt.ylabel("Average Score")
    plt.tight_layout()
    plt.savefig("difficulty_performance.png")
    plt.close()

def main(user_id):
    # Fetch quiz data
    current_quiz = fetch_current_quiz_data(user_id)
    historical_quizzes = fetch_historical_quiz_data(user_id)
    
    # Analyze performance
    analysis = analyze_quiz_performance(current_quiz, historical_quizzes)
    
    # Generate recommendations
    recommendations = generate_recommendations(analysis)
    
    # Predict NEET rank (assuming we have previous year results)
    previous_year_results = pd.read_csv("previous_year_results.csv")  # You'll need to provide this data
    user_performance = pd.DataFrame({
        'avg_score': [analysis['avg_score']],
        'topic_coverage': [len(analysis['topic_performance'])],
        'difficulty_level': [analysis['difficulty_performance'].index[0]]
    })
    predicted_rank = predict_neet_rank(user_performance, previous_year_results)
    
    # Visualize performance
    visualize_performance(analysis)
    
    # Print results
    print("Performance Analysis:")
    print(f"Average Score: {analysis['avg_score']:.2f}")
    print(f"Score Trend: {analysis['score_trend']:.2f}")
    print("\nTop Performing Topics:")
    print(analysis['topic_performance'].head())
    print("\nWeak Topics:")
    print(analysis['weak_topics'])
    print("\nRecommendations:")
    for rec in recommendations:
        print(f"- {rec}")
    print(f"\nPredicted NEET Rank: {predicted_rank:.0f}")

if __name__ == "__main__":
    user_id = input("Enter user ID: ")
    main(user_id)

