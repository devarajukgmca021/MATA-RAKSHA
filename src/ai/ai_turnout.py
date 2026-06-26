# src/utils/ai/ai_turnout.py
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

def predict_turnout(voter_history):
    """
    voter_history = list of numbers representing turnout per past election.
    """
    X = np.array(range(len(voter_history))).reshape(-1, 1)
    y = np.array(voter_history)

    model = LinearRegression()
    model.fit(X, y)

    next_turnout = model.predict([[len(voter_history)]])

    return int(next_turnout[0])


def show_turnout_graph(voter_history):
    X = np.array(range(len(voter_history)))
    y = np.array(voter_history)

    model = LinearRegression()
    model.fit(X.reshape(-1,1), y)
    pred_next = model.predict([[len(X)]])

    plt.plot(X, y, marker='o')
    plt.scatter([len(X)], pred_next, label=f"Predicted: {int(pred_next)}")
    plt.title("AI Voter Turnout Prediction")
    plt.xlabel("Election Year Index")
    plt.ylabel("Turnout")
    plt.legend()
    plt.show()
