from surprise import SVD, Dataset, Reader, accuracy, dump
from surprise.model_selection import train_test_split
from items_ratings_treated import ratings

# training and implementations of this is pretty easy, but applying it on the final application is still something I need
# to evaluate.
# for using the svd, a user needs to have his ratings on the system and the model needs to be retrained, so won't be able
# to use this for new users

if __name__ == "__main__":
    reader = Reader(line_format='user item rating', sep=',', skip_lines=1)

    data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader=reader)
    trainset, testset = train_test_split(data, test_size=0.2)

    svd = SVD()
    svd.fit(trainset)
    predictions = svd.test(testset)

    mae = accuracy.mae(predictions=predictions)
    rmse = accuracy.rmse(predictions=predictions)

    dump.dump("svd.pkl", predictions=predictions, algo=svd, verbose=1)
