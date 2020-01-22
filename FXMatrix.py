# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 10:41:50 2020

@author: Laguema
"""

import pandas as pd
def FXMatrix(FXDict):
    """Receives a dictionary of currency pair:rate in the form {CADUSD:1.3} and computes a matrix with all the possible cross between rates"""
    
    FX=pd.DataFrame(index =set([x[:3] for x in FXDict.keys()]+[x[3:] for x in FXDict.keys()]),columns =set([x[:3] for x in FXDict.keys()]+[x[3:] for x in FXDict.keys()]))
    
    for curfrom in FX.columns:
        
        for curto in FX.index:
            #If currency to itself set rate to 1
            if curfrom==curto:
                
                FX.loc[curto,curfrom] = 1
                
            else:
                
                #We'll use a algorithm that tries all combination until solution if found
                
                #curPool will be used for a single path until no possibilities are left
                curPool=FXDict.copy()
                
                #LastIteration will be used to remove paths taken without success
                LastIteration=FXDict.copy()
    
                
                while len(curPool.keys())>1:
                    
                    #We start by looking for the currency we want to get to (the base)
                    lookfor=curto
                    #Set initial previous rate iteration to 1
                    prevrate=1
                    #Loop through the remaining currency pairs that contains the sought currency
                    while list(filter(lambda x:x.find(lookfor)!=-1,curPool.keys())):
                        #Get the first eligible pair that contains the sought after currency
                        pair = list(filter(lambda x:x.find(lookfor)!=-1,curPool.keys()))[0]
                        
                        #If the sought currency is the local in the pair
                        if lookfor==pair[3:]:
                            #Inverse rate and change new sought currency to the other member of the pair
                            rate = 1/curPool[pair]
                            lookfor=pair[:3]
                        #If the sought currency is the base in the pair
                        else:
                            #Take rate and change new sought currency to the other member of the pair
                            rate = curPool[pair]
                            lookfor=pair[3:]
                            
                        #Remove the currency pair used from the pool
                        curPool.pop(pair)
                        #Cross the rate
                        rate*=prevrate
                        
                        #If the new sought currency is the initial starting currency (local) then we got a match
                        if lookfor==curfrom:
                            FX.loc[curto,curfrom]=rate
                            LastIteration = {pair:rate}
                            break
                        #If no match is found continue with latest rate computed
                        else:
                            prevrate=rate
                            
                    #If no more currencies are left in the pool, and no match is found, means either the rate cannot be obtain due 
                    #to missing pairs or the path taken do not lead to a match
                    else:
                        #Remove the origination of the last path taken
                        LastIteration.pop(pair)
                        #Reset the pool for the next path to take
                        curPool=LastIteration.copy()
                        continue
                    
                    #If match has been found break from pool loop and go to next currency pair
                    break
                    
    return FX