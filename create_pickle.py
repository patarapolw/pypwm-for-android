from memorable_password import GeneratePassword
import pickle


if __name__ == '__main__':
    with open('generate_password.pkl', 'wb') as f:
        pickle.dump(GeneratePassword(do_markovify=True), f)
