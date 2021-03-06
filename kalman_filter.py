# -*- coding: utf-8 -*-
"""
Created on Sun May 14 18:13:03 2017

@author: Gamal
"""

'''
% This file calculates kalman filter output from input dataframe of a specific patient
% the output is a dataframe with kalman filter values
% 
% /**************************************************************************** 
%  * Job:             Kalman Filter                                      * 
%  * Description: This script calculates kalman filter for the input dataframe
%                                     * 
%  *Inputs: signal dataframe
%  *Outputs: Kalman filter results  as a dataframe                            * 
%  * Generated on:    Mon, May 15, 2017                                       * 
%  * Generated by:    Gamal Elkomy                                            * 
%  * Version:         1                                                       * 
%  ****************************************************************************/ 
'''
''' usefull example https://www.quantopian.com/posts/quantopian-lecture-series-kalman-filters'''
''' ******* pip install pykalman ************'''

from pykalman import KalmanFilter
#import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
#from scipy import poly1d

def kalman_filter(data):
    result=pd.DataFrame() # will hold the results
    for col in data.columns:
        
#        creating kalman filter object
        kf = KalmanFilter(transition_matrices = [1],
                          observation_matrices = [1],
                          initial_state_mean = 0,
                          initial_state_covariance = 1,
                          observation_covariance=6,  # fixes the error
                          transition_covariance=.01)
        
#        auto compute kalman filter parameters
        kf = kf.em(data.loc[:,col], n_iter=5)
                
        # Use the observed values of the price to get a rolling mean
        # perform smoothing
        state_means, _ = kf.smooth(data.loc[:,col])
        # convert to pandas series
        state_means = pd.Series(state_means.flatten(), index=data.loc[:,col].index)
        
        # Plot original data and estimated mean
#        plt.plot(state_means)
#        plt.plot(x)
#        plt.title('Kalman filter estimate of average')
#        plt.legend(['Kalman Estimate','Kalman Estimate Emulate', 'X'])

        #concat the result with the output data frame
        result=pd.concat([result, state_means ] ,axis=1)
    result.columns= data.columns    
    return result

