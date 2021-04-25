'''
Looking at our backpacking equipment DataFrame, suppose we are interested in finding our total weight for each category. Use groupby to group the dataframe, and apply a function to calculate the total weight (Weight x Quantity) by category.
                       Category  Quantity  Weight (oz.)
Item
Pack                       Pack         1          33.0
Tent                    Shelter         1          80.0
Sleeping Pad              Sleep         1          27.0
Sleeping Bag              Sleep         1          20.0
Toothbrush/Toothpaste    Health         1           2.0
Sunscreen                Health         1           5.0
Medical Kit              Health         1           3.7
Spoon                   Kitchen         1           0.7
Stove                   Kitchen         1          20.0
Water Filter            Kitchen         1           1.8
Water Bottles           Kitchen         2          35.0
Pack Liner              Utility         1           1.0
Stuff Sack              Utility         1           1.0
Trekking Poles          Utility         1          16.0
Rain Poncho            Clothing         1           6.0
Shoes                  Clothing         1          12.0
Hat                    Clothing         1           2.5
'''
print(df.groupby('Category').apply(lambda x: sum(x['Quantity'] * x['Weight (oz.)'])))

# or
print(df.groupby('Category').apply(lambda df, a, b: sum(df[a] * df[b]), 'Weight (oz.)', 'Quantity'))
# or


def totalweight(df, w, q):
    return sum(df[w] * df[q])


print(df.groupby('Category').apply(totalweight, 'Weight (oz.)', 'Quantity'))
