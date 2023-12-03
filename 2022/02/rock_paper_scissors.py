
rock = 1
paper = 2
scissors = 3
win = 6
draw = 3
lose = 0

scores_by_response = {
    "A X": rock+draw,
    "A Y": paper+win,
    "A Z": scissors+lose,
    "B X": rock+lose,
    "B Y": paper+draw,
    "B Z": scissors+win,
    "C X": rock+win,
    "C Y": paper+lose,
    "C Z": scissors+draw,
}


scores_by_strategy = {
    "A X": scissors+lose,
    "A Y": rock+draw,
    "A Z": paper+win,
    "B X": rock+lose,
    "B Y": paper+draw,
    "B Z": scissors+win,
    "C X": paper+lose,
    "C Y": scissors+draw,
    "C Z": rock+win,
}

def ideal_score(scores):
    total_score = 0
    with open("input", "r") as f:
        for line in f:
            total_score += scores.get(line.strip(), 0)

    return total_score


if __name__ == "__main__":
    print(ideal_score(scores_by_response))
    print(ideal_score(scores_by_strategy))