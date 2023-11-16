from model import *

parser = argparse.ArgumentParser(description='Train model')
parser.add_argument('--input-dir', help='Path to folder with training texts in .txt format', required=True)
parser.add_argument('--model', help='Directory for saving model', default='./', required=False)
parser.add_argument('--grams', help='Amount of grams', default=3, type=int, required=False)
parser.add_argument('--verbose', help='Print timings etc.', default=True, type=bool, required=False)

args = parser.parse_args()
if __name__ == "__main__":
    start = time.time()
    model = n_gram_model(args.grams)
    model.fit(args.input_dir)
    if args.verbose:
        print(f'Model training took {time.time() - start} seconds.')
    pickle.dump(model, open(f'{args.model}/model.pkl', 'wb'))
    print(f'The model was saved to {args.model} model.pkl')
