
if __name__ == '__main__':


    #Define the parameters
    #Instanciate the class
    pdef = param_def( dataset, Y_name="failure",
                     X_name = list(dataset.columns[2:50]))

    #Get maximum and minimum limit of length split ( such that we have more than
    # 10 events, parameter for split data)
    pdef.get_lim()

    #split the dataset
    pdef.split_data()

    #get default parameters of the design
    #largeur, ecart_int, ecart_CC
    pdef.param_def()


    #Instanciate the method Case Crossover
    method = Case_Cross(largeur = pdef.largeur, ecart_int = pdef.ecart_int,
                        ecart_CC = pdef.ecart_CC, dataset = pdef.data,
                        comp = False,threshold = [[0.7, 1]],
                        num_val = np.shape(pdef.data)[-1], num_control= 3 )

                        
    #Run the algorithm that output the table
    data_mfl =  method.ARM_CC()