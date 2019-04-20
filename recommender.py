import cPickle
import pandas as pd
import numpy as np
from scipy.spatial.distance import squareform, pdist


class UserRecommender():
    def __init__(self, outfile):
        self.cold_start_message = 'COLD_START'
        self.cold_start = False
        self.outfile = outfile
        
    def train(self):
        df = self.get_train_data()
        # lowercase username
        df['username'] = df['username'].str.lower()
        # only score varieties that are shared between users
        _varieties = self.get_common_varieties(df)
        dfvar = df.loc[df['variety'].isin(_varieties)].copy()

        # standardize scores then scale to [0,1]
        dfvar['norm_01_points'] = self._scale(self._standardize(dfvar['points']))

        # user, item dataframe (matrix) input to distance calcs
        user_variety = dfvar.pivot_table(index='username',columns='variety',values='norm_01_points', aggfunc='mean').fillna(0)

        # returns a dictionary of user, buddy, where buddy is closest match
        user_user_matches = self.user_matches(user_variety)

        with open(self.outfile, "wb") as output_file:
            cPickle.dump(user_user_matches, output_file)
        print 'TRAINING FINISHED, RECOMMENDATIONS WRITTEN TO: ', self.outfile


    @staticmethod
    def get_train_data(file='csv_files/reviews3.csv', sep=';'):
        return pd.read_csv(file, sep)

    @staticmethod
    def get_common_varieties(df):
        varieties = df.groupby('variety')['username'].nunique()
        common_varieties = varieties.loc[varieties > 1].index.values
        return common_varieties
    
    @staticmethod
    def _standardize(df_series):
        assert isinstance(df_series, pd.Series), 'Input is not pandas.Series'
        return (df_series - df_series.mean()) / df_series.std()

    @staticmethod
    def _scale(df_series):
        assert isinstance(df_series, pd.Series), 'Input is not pandas.Series'
        return ((df_series - df_series.min()) / (df_series.max() - df_series.min()))

    @staticmethod
    def user_user_distances(df_user_item, distance='cosine'):
        assert isinstance(df_user_item, pd.DataFrame), 'Input is not pandas.DataFrame'
        res = pdist(df_user_item, distance)
        return squareform(res)

    @staticmethod
    def idx_closest_user(distance_mat):
        # WARNING: this is an inplace operation :(
        np.fill_diagonal(distance_mat, np.inf)
        best_matches = []
        for i in range(distance_mat.shape[0]):        
            best_matches.append(distance_mat[i,:].argmin())
            
        return np.array(best_matches)

    def user_matches(self, df_user_item, distance='cosine'):
        user_user = self.user_user_distances(df_user_item, distance)
        best_matches = self.idx_closest_user(user_user)

        users = df_user_item.index.values.tolist()
        buddies = df_user_item.index.values[best_matches].tolist()
        return dict(zip(users, buddies))

    def recommend(self, username):
        with open(self.outfile, "rb") as input_file:
            self._recommender_dict = cPickle.load(input_file)

        if username in self._recommender_dict:
            self.cold_start = False
            return self._recommender_dict[username]
        else:
            self.cold_start = True
            return self.cold_start_message


# test file: # r"recommendations/dummy_recs.pickle"
user_user_file = r"recommendations/user_user_matches.pickle"
recommender = UserRecommender(user_user_file)


if __name__ == "__main__":
    recommender = UserRecommender(user_user_file)
    recommender.train()