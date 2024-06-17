
class Case_Cross :

    """ class for applying Case Crossover Design """


    def __init__(self,largeur, ecart_int, ecart_CC, dataset, comp = False,
                 threshold = [[0.6, 1]], num_val = 1200, num_control=1 ):
        self.data = dataset
        self.comp = comp
        self.threshold = threshold
        self.thresh = threshold[0]
        self.l = largeur
        self.e_int = ecart_int
        self.e_CC = ecart_CC
        self.num_val = num_val
        self.num_control = num_control

    def abs_dist(self,t):
        """
        Parameters
        ----------
        t : tuple
            contains value to compare.

        Returns
        -------
        absolute distance.

        """
        #return np.abs(t[1]-t[0]/t[1])
        #return np.abs((max(t)-min(t))/max(t))
        if max(t)==0:
            return 0
        return (np.abs(max(t))-np.abs(min(t)))/np.abs(max(t))


    def MFL(self,X):
        """
        Function comparing the mean of the control and case period
        Parameters
        ----------
        data : dataframe
            variable to study.
        comp: bool
            If False, we will have the case period, otherwise the control period
        c: int
            Choose a period, the bigger it is, the less distant from the event
            the period is

        Returns
        -------
        mean_control : list
            mean of the control period.
        mean_case : list
            mean of the case period.

        """
        # split dataset
        case1, case2 = X[-(1+self.l):-1],\
            X[-(1+self.e_int+2*self.l):-(1+self.e_int+self.l)]
        control1, control2 = X[-(1+self.l+self.e_CC+self.c):-(
            1+self.e_CC+self.c)],\
            X[-(1+self.e_int+2*self.l+self.e_CC+self.c):-(
                1+self.l+self.e_CC+self.c)]
        mean_case1 = case1.mean()
        mean_case2 = case2.mean()
        if self.comp:
            mean_control1 = control1.mean()
            mean_control2 = control2.mean()
            return mean_control1, mean_control2
        return mean_case1, mean_case2

    def compare(self):
        """
        Function comparing the events using a method and a treshold

        Parameters
        ----------
        method : func
            Method to use. ex: AR models
        thresh : float
            threshold on the value that we compare.
        comp : bool
            True if we want to compare the two control periods
        Returns
        -------
        count : Series
            Give the count of each variable that respected the thresh.
        df_flood : DataFrame
            Contain bool columns for each event telling which
            variable respeted the threshold
        """
        nb_flood = len(self.data)
        df = self.data[0].apply(self.MFL)
        col = df.apply(self.abs_dist)
        count = ((col>self.thresh[0])*1)&((col<=self.thresh[1])*1)
        column = [count.rename('flood_1')]
        for i in range(1,nb_flood):
            df = self.data[i].apply(self.MFL)
            col = df.apply(self.abs_dist)
            column.append((((col>self.thresh[0])*1)&((col<=self.thresh[1])*1)
            ).rename('flood_'+str(i+1)))
            count += column[-1]
        return count

    def ARM_CC(self):
      df_MFL = pd.DataFrame()
      num_evt = np.shape(self.data)[0]
      for i in range(self.num_control):
          self.c = int(i*(self.l/2))
          self.comp = True
          count_MFL = self.compare()
          #case-control comparison
          self.comp = False
          count_MFL_c = self.compare()
          df_MFL['case'+str(i)]  = count_MFL
          df_MFL['control'+str(i)] = count_MFL_c


          df_MFL['odd_ratio'+str(i)]= (df_MFL['case'+str(i)]+1) *(num_evt-
                                      df_MFL['control'+str(i)])/((num_evt-
                          df_MFL['case'+str(i)]) *(df_MFL['control'+str(i)]+1))
      df_MFL['case'] = df_MFL.filter(regex='^case',axis=1).mean(axis=1)
      df_MFL['control'] = df_MFL.filter(regex='^control',axis=1).mean(axis=1)
      df_MFL['odd_ratio'] = df_MFL.filter(regex='^odd_ratio',axis=1).mean(axis=1)
      return df_MFL.loc[:,['case','control','odd_ratio']]