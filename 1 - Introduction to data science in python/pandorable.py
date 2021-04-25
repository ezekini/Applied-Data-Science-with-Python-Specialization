'''
Suppose we are working on a DataFrame that holds information on our equipment for an upcoming backpacking trip.

Can you use method chaining to modify the DataFrame df in one statement to drop any entries where 'Quantity' is 0 and rename the column 'Weight' to 'Weight (oz.)'?

                      Category  Quantity  Weight
Item
Pack                      Pack         1    33.0
Tent                   Shelter         1    80.0
Sleeping Pad             Sleep         0    27.0
Sleeping Bag             Sleep         1    20.0
Toothbrush/Toothpaste   Health         1     2.0


'''
print(
    df.drop(df[df['Quantity'] == 0].index)
    .rename(columns={'Weight': 'Weight (oz.)'})
)
