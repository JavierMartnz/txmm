import pandas as pd
import matplotlib.pyplot as plt

filename = 'tripadvisorattraction.csv'

attraction_df = pd.read_csv(filename) 


clean_df = attraction_df.loc[attraction_df['distance_to_center'].notna() & attraction_df['distance_to_center'] != 0]

fig, ax = plt.subplots()
ax.plot(clean_df['attraction_n_reviews'], clean_df['attraction_rating'], linestyle='', marker='o')
ax.set_xscale('log')
ax.set_xlabel("Popularity (# of reviews)")
ax.set_ylabel("Attraction rating")
ax.set_yticks([3.5, 4, 4.5, 5])


# distance_clean_df.plot.scatter('distance_to_center', 'attraction_rank')
# distance_clean_df.plot.scatter('distance_to_center', 'attraction_rating')
# distance_clean_df.plot.scatter('distance_to_center', 'attraction_n_reviews', logy=True)
# distance_clean_df.plot.scatter('distance_to_center', 'neg_review_ratio')


# attraction_df.plot.scatter('attraction_rank', 'attractions_nearby')
# attraction_df.plot.scatter('attraction_rank', 'attraction_n_reviews')
# attraction_df.plot.scatter('attraction_rank', 'restaurants_nearby')

# attraction_df.plot.scatter('attraction_rating', 'attraction_rank')
# attraction_df.plot.scatter('attraction_rating', 'attraction_n_reviews')