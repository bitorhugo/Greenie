#!/usr/bin/python

from sklearn.metrics import f1_score

# Define the ground truth answers and GPT-3's responses
questions = ["What is the capital of France?", "Who directed The Godfather?", "What is the highest mountain in the world?"]
answers = ["Paris", "Francis Ford Coppola"]

# Calculate the F1 score for each question and answer pair
f1_scores = []
for i in range(min(len(questions), len(answers))):
    question = questions[i]
    answer = answers[i]
    predicted_answer = ""
    print(question)
    print(answer)
    f1 = f1_score([answer], [predicted_answer], average='weighted')
    f1_scores.append(f1)

# Calculate the average F1 score across all question and answer pairs
average_f1 = sum(f1_scores) / len(f1_scores)

print("Average F1 score:", average_f1)
