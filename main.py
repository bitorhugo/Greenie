#!/usr/bin/python3

import re
import snlp, asyncio, csv, os
from bot.context import Context
from bot.role import Role
from bot.grennie import Greenie
from sklearn.metrics import f1_score
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
# messages will be a json array
# json object -> dict[str, str]
# e.g.
# context = [
#     {"role": "system", "content": "You are a helpful, pattern-following assistant that helps field operators and citizens on a smart city."},
#     {"role": "system", "content": "If you don't know the answer to a question say, I don't know."},
#     {"role": "system", "content": f'{raw}'},
#     {"role": "user", "content": "Tell me the first item needed"},
# ]
# context will be composed of a list of dictionaries

def test_cossine_similarity():
    # define two example sentences
    sentence1 = "I like pizza"
    sentence2 = "I like pizza"

    # create a CountVectorizer object
    vectorizer = CountVectorizer()

    # fit the vectorizer on the sentences
    vectorizer.fit_transform([sentence1, sentence2])

    # transform the sentences into vectors
    vector1 = vectorizer.transform([sentence1]).toarray()
    vector2 = vectorizer.transform([sentence2]).toarray()

    # calculate cosine similarity between the two vectors
    cosine_sim = cosine_similarity(vector1, vector2)

    # print the cosine similarity
    print("Cosine similarity:", cosine_sim[0][0])

async def f1(debug: bool=False):
    f1_path = 'logs/f1.csv'
    f = open ("data/en/pcb.txt")
    data = f.read()
    # run questions through chatbot
    qna = load_QnA_F1()
    rows = []
    for item in qna:
        a, q = item.pop(), item.pop()
        context = Context(initial_msg=True)
        context.add_knowledge(Role.SYSTEM, snlp.filter_raw(data, debug=False))
        context.add_question(q)
        context.tokens(debug=False)
        print(f'Question: {context.get_question()}')

        bot = Greenie()
        r = await bot.response(context, debug=False)

        print(f'bot-answer:{r}')
        print(f'human-answer:{a}')
        rows.append([q, a, r])

    with open(f1_path, 'a+t', newline='') as f:
        w = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        if os.stat(f1_path).st_size == 0: # file is empty, write headers
            w.writerow(['question', 'human-answer', 'bot-answer'])
        w.writerows(rows)
        
def test():
    questions = []
    human = []
    bot = []
    f1_scores = []
    with open('logs/f1.csv') as f:
        r = csv.reader(f)
        next(r)
        for row in r:
            b, h, q = row.pop(), row.pop(), row.pop()
            questions.append(q)
            human.append(h)
            bot.append(re.sub('\n', '', b))
    for i in range(min(len(questions), len(human))):
        question = questions[i]
        answer = human[i]
        predicted_answer = bot[i]
        print(f'question:{question}')
        print(f'human:{answer}')
        print(f'bot:{predicted_answer}')
        f1 = f1_score([answer], [predicted_answer], average='weighted')
        f1_scores.append(f1)
    # Calculate the average F1 score across all question and answer pairs
    average_f1 = sum(f1_scores) / len(f1_scores)
    print(f'f1:{f1_scores}')

            
def load_QnA_F1(debug: bool=False) -> list[list[str]]:
    qna = []
    with open('data/QnA/qa.csv') as f:
        r = csv.reader(f)
        for row in r:            # each row is a list containing a question and its answer
            if debug:
                print(f'qna:{row}')
            qna.append(row)
    return qna
            
            
async def main():
    f = open ("data/en/pcb.txt")
    data = f.read()

    q = "whats the last step in the pcb charger assembly?"
    context = Context(initial_msg=True)
    
    context.add_knowledge(Role.SYSTEM, snlp.filter_raw(data, debug=True))
    context.add_question(q)
    context.tokens(debug=False)
    print(f'Context: {context}')
    print(f'Question: {context.get_question()}')

    bot = Greenie()
    tokens = bot.count_tokens(context)
    total = bot.req_price(tokens)
    print (f'Tokens: {tokens}')
    print (f'Total Price est ~ {total}$')
    await bot.response(context, debug=True)

    
if __name__ == '__main__':
    # asyncio.run(main())
    # asyncio.run(f1())
    test_cossine_similarity()
