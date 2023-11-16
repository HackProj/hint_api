from model import *

parser = argparse.ArgumentParser(description='Train model')
parser.add_argument('--model', help='Path to model.pkl', required=True)
parser.add_argument('--prefix', help='Prefix for text generation', default='', required=False)
parser.add_argument('--length', help='Length of text to generate', default=20, type=int, required=False)
parser.add_argument('--verbose', help='Print timings etc.', default=True, type=bool, required=False)

args = parser.parse_args()


def get_hint(model='model.pkl', length=8, prefix='Ты опять'):
    model = pickle.load(open(model, 'rb'))
    return model.generate(length, prefix)


if __name__ == "__main__":
    # model = pickle.load(open('model.pkl', 'rb'))
    print(f'Generated sample:')
    start = time.time()
    print(get_hint('model.pkl', args.length, args.prefix))
    if args.verbose:
        print(f'Sample generating took {time.time() - start} seconds.')
