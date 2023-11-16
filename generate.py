import pickle


def get_hint(model="model.pkl", length=8, prefix="Ты опять"):
    model = pickle.load(open(model, "rb"))
    return model.generate(length, prefix)
