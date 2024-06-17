class param_def :

    """ class to split the dataset and get the parameters to apply the Case Crossover """


    def __init__(self, dataset, Y_name, X_name):
        self.data = None
        self.dataset = dataset
        self.target = Y_name
        self.X = X_name

    def get_lim(self):
        """
        Function to get minimum and maximum split length of the time series
        """
        #sort by length of time series
        column = pd.Series(self.dataset.loc[:,self.target])
        arg = np.argwhere((column.diff()==1).values).flatten()
        len_split = pd.Series(arg).diff().fillna(pd.Series(arg))
        val = len_split.sort_values().drop_duplicates()
        num_evt = 11
        i=0
        while num_evt >= 10 and i < len(val):
          lim_sup = val.iloc[i]
          num_evt = np.sum(len_split>=lim_sup)
          i+=1
        self.lim_sup = int(lim_sup)
        self.lim_inf = int(val.iloc[0])

    def split_data(self, len_ts=None):
        """
        Function to split the long time series dataset into events
        """
        df = []
        column = pd.Series(self.dataset.loc[:,self.target])
        arg = np.argwhere((column.diff()==1).values).flatten()
        len_split = pd.Series(arg).diff().fillna(pd.Series(arg))
        if len_ts == None:
            len_ts = self.lim_inf
        diff = arg[len_split>=len_ts]
        for val in diff:
            df.append(self.dataset.iloc[val-len_ts:val,:].loc[:,self.X].reset_index(drop=True))
        #Add mean at the end
        df_concat = pd.concat(df)
        by_row_index = df_concat.groupby(df_concat.index)
        df_means = by_row_index.mean()
        df.append(df_means)
        self.data = df

    def param_def(self):
      """
      Function to set the default parameters for the control and the case periods
      """
      length = np.shape(self.data)[1]
      self.largeur = int(length*0.05)
      self.ecart_int = int(length*0.05)
      self.ecart_CC = int(length*0.5)