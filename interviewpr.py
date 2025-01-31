import random

# Sample data (replace this with actual data in a real scenario)
sample_quiz_data = [
    {"topic": "Physics", "score": 7, "total": 10, "difficulty": "medium"},
    {"topic": "Chemistry", "score": 8, "total": 10, "difficulty": "easy"},
    {"topic": "Biology", "score": 6, "total": 10, "difficulty": "hard"},
]

def analyze_performance(quiz_data):
    """Analyze quiz performance and return insights"""
    total_score = sum(quiz['score'] for quiz in quiz_data)
    total_questions = sum(quiz['total'] for quiz in quiz_data)
    overall_percentage = (total_score / total_questions) * 100

    topic_performance = {}
    for quiz in quiz_data:
        topic = quiz['topic']
        percentage = (quiz['score'] / quiz['total']) * 100
        topic_performance[topic] = percentage

    weak_topics = [topic for topic, score in topic_performance.items() if score < overall_percentage]

    return {
        "overall_percentage": overall_percentage,
        "topic_performance": topic_performance,
        "weak_topics": weak_topics
    }

def generate_recommendations(analysis):
    """Generate personalized recommendations based on the analysis"""
    recommendations = []

    if analysis["overall_percentage"] < 60:
        recommendations.append("Focus on improving your overall performance across all subjects.")

    for topic in analysis["weak_topics"]:
        recommendations.append(f"Spend more time studying {topic}.")

    if len(recommendations) == 0:
        recommendations.append("Great job! Keep up the good work and practice consistently.")

    return recommendations

def predict_rank(overall_percentage):
    """Simple rank prediction based on overall percentage"""
    if overall_percentage > 90:
        return random.randint(1, 1000)
    elif overall_percentage > 80:
        return random.randint(1000, 5000)
    elif overall_percentage > 70:
        return random.randint(5000, 20000)
    else:
        return random.randint(20000, 50000)

def main():
    print("NEET Exam Preparation Analysis")
    print("==============================")

    # In a real scenario, you would fetch this data from an API or database
    quiz_data = sample_quiz_data

    analysis = analyze_performance(quiz_data)
    recommendations = generate_recommendations(analysis)
    predicted_rank = predict_rank(analysis["overall_percentage"])

    print(f"\nOverall Performance: {analysis['overall_percentage']:.2f}%")
    print("\nTopic-wise Performance:")
    for topic, score in analysis["topic_performance"].items():
        print(f"- {topic}: {score:.2f}%")

    print("\nAreas for Improvement:")
    for topic in analysis["weak_topics"]:
        print(f"- {topic}")

    print("\nPersonalized Recommendations:")
    for recommendation in recommendations:
        print(f"- {recommendation}")

    print(f"\nPredicted NEET Rank Range: Around {predicted_rank}")

if __name__ == "__main__":
    main()

