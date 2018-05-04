import nltk

if __name__ == '__main__':
    with open('nltk.txt') as f:
        for row in f:
            nltk.download(row.strip())
