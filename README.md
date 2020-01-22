# fxMatrix
Extract all currency crosses from a given set of FX rates. Argument taken are set of FX rates as a dictionnary and function returns 
pandas DataFrame with local currencies as index, base currencies as columns and rates as values.

If USD CAD is 1.35, CAD = local and USD = base.
Algorithm select a random currency pair that includes the base currency. Then currencies pairs are crossed 
until local currency is found. If no more pairs are left to cross with then the random starting currency pair is 
removed and another pair including the base is randomly chosen to start over.
