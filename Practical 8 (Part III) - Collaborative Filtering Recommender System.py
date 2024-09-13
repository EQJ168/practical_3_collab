{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Practical 8 (Part III) - Recommender System (Collaborative Filtering)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Recommender systems are algorithms aimed at suggesting relevant items to users. Collaborative filtering based solely on the past interactions recorded between users and items in order to produce new recommendations. These interactions are stored in the so-called “user-item interactions matrix”. This practical demonstrates how to build a recommender system that identify movies to view based on collaborative filtering method."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Section 1 Data Preparation"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "1. Reading data from files\n",
    "\n",
    "\"file.tsv\" contains 100,003 rows of records that store the user ratings as shown in the table below.\n",
    "\n",
    "| user_id | item_id | rating | timestamp |\n",
    "| --- | --- | --- | --- |\n",
    "|0 | 50 |\t5 |\t881250949|\n",
    "|0 | 172 |\t5 |\t881250949|\n",
    "|0 | 133 |\t1 |\t881250949|\n",
    "|196 | 242 | 3 | 881250949|\n",
    "|186 | 302 | 3 | 891717742|\n",
    "\n",
    "On the other hand, \"Movie_Id_Titles.csv\" contains 1682 movie titles associated with their item_id."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Can do two recommender system > user-user or item-item\n",
    "if people A and people b like the same categories then the people A will recommend the googles to the people B (it may recommend different product based on your behaviour)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>user_id</th>\n",
       "      <th>item_id</th>\n",
       "      <th>rating</th>\n",
       "      <th>timestamp</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>0</td>\n",
       "      <td>50</td>\n",
       "      <td>5</td>\n",
       "      <td>881250949</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>0</td>\n",
       "      <td>172</td>\n",
       "      <td>5</td>\n",
       "      <td>881250949</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>0</td>\n",
       "      <td>133</td>\n",
       "      <td>1</td>\n",
       "      <td>881250949</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>196</td>\n",
       "      <td>242</td>\n",
       "      <td>3</td>\n",
       "      <td>881250949</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>186</td>\n",
       "      <td>302</td>\n",
       "      <td>3</td>\n",
       "      <td>891717742</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   user_id  item_id  rating  timestamp\n",
       "0        0       50       5  881250949\n",
       "1        0      172       5  881250949\n",
       "2        0      133       1  881250949\n",
       "3      196      242       3  881250949\n",
       "4      186      302       3  891717742"
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import pandas as pd              # import pandas as pd \n",
    "  \n",
    "# Get the data \n",
    "column_names = ['user_id', 'item_id', 'rating', 'timestamp']   # define 4 columns ['user_id', 'item_id', 'rating', 'timestamp'] \n",
    "  \n",
    "path = r'C:\\Users\\User\\Downloads\\file.tsv'                                #read file 'file.tsv'\n",
    "\n",
    "# tsv is tab-separated values file\n",
    "df = pd.read_csv(path, sep='\\t', names=column_names) \n",
    "  \n",
    "# Check the head of the data \n",
    "df.head() "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>item_id</th>\n",
       "      <th>title</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>1</td>\n",
       "      <td>Toy Story (1995)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>2</td>\n",
       "      <td>GoldenEye (1995)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>3</td>\n",
       "      <td>Four Rooms (1995)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>4</td>\n",
       "      <td>Get Shorty (1995)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>5</td>\n",
       "      <td>Copycat (1995)</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   item_id              title\n",
       "0        1   Toy Story (1995)\n",
       "1        2   GoldenEye (1995)\n",
       "2        3  Four Rooms (1995)\n",
       "3        4  Get Shorty (1995)\n",
       "4        5     Copycat (1995)"
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Check out all the movies and their respective IDs \n",
    "movie_titles = pd.read_csv(r'C:\\Users\\User\\Downloads\\Movie_Id_Titles.csv')              #read another file Movie_Id_Titles.csv\n",
    "movie_titles.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<hr/>\n",
    "2. Now let's merge these 2 files together.\n",
    "<hr/>"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "****************no need to merge if one file only****************"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>user_id</th>\n",
       "      <th>item_id</th>\n",
       "      <th>rating</th>\n",
       "      <th>timestamp</th>\n",
       "      <th>title</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>0</td>\n",
       "      <td>50</td>\n",
       "      <td>5</td>\n",
       "      <td>881250949</td>\n",
       "      <td>Star Wars (1977)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>0</td>\n",
       "      <td>172</td>\n",
       "      <td>5</td>\n",
       "      <td>881250949</td>\n",
       "      <td>Empire Strikes Back, The (1980)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>0</td>\n",
       "      <td>133</td>\n",
       "      <td>1</td>\n",
       "      <td>881250949</td>\n",
       "      <td>Gone with the Wind (1939)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>196</td>\n",
       "      <td>242</td>\n",
       "      <td>3</td>\n",
       "      <td>881250949</td>\n",
       "      <td>Kolya (1996)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>186</td>\n",
       "      <td>302</td>\n",
       "      <td>3</td>\n",
       "      <td>891717742</td>\n",
       "      <td>L.A. Confidential (1997)</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   user_id  item_id  rating  timestamp                            title\n",
       "0        0       50       5  881250949                 Star Wars (1977)\n",
       "1        0      172       5  881250949  Empire Strikes Back, The (1980)\n",
       "2        0      133       1  881250949        Gone with the Wind (1939)\n",
       "3      196      242       3  881250949                     Kolya (1996)\n",
       "4      186      302       3  891717742         L.A. Confidential (1997)"
      ]
     },
     "execution_count": 11,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "data = pd.merge(df, movie_titles, on='item_id')     #merge both file based on item_id\n",
    "data.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<hr/>\n",
    "3. We need to group the movie titles and view their ratings in the descending order.\n",
    "<hr/>"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "title\n",
       "They Made Me a Criminal (1939)                5.0\n",
       "Marlene Dietrich: Shadow and Light (1996)     5.0\n",
       "Saint of Fort Washington, The (1993)          5.0\n",
       "Someone Else's America (1995)                 5.0\n",
       "Star Kid (1997)                               5.0\n",
       "Name: rating, dtype: float64"
      ]
     },
     "execution_count": 13,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Calculate mean rating of all movies \n",
    "data.groupby('title')['rating'].mean().sort_values(ascending=False).head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Section 2 Data Exploration"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "****************Not important******************"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "4 . Let's observe the top rated movies"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "title\n",
       "Star Wars (1977)             584\n",
       "Contact (1997)               509\n",
       "Fargo (1996)                 508\n",
       "Return of the Jedi (1983)    507\n",
       "Liar Liar (1997)             485\n",
       "Name: rating, dtype: int64"
      ]
     },
     "execution_count": 18,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Calculate count rating of all movies \n",
    "data.groupby('title')['rating'].count().sort_values(ascending=False).head() "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<bound method DataFrame.info of                                        user_id  item_id  rating  timestamp\n",
       "title                                                                     \n",
       "'Til There Was You (1997)                    9        9       9          9\n",
       "1-900 (1994)                                 5        5       5          5\n",
       "101 Dalmatians (1996)                      109      109     109        109\n",
       "12 Angry Men (1957)                        125      125     125        125\n",
       "187 (1997)                                  41       41      41         41\n",
       "...                                        ...      ...     ...        ...\n",
       "Young Guns II (1990)                        44       44      44         44\n",
       "Young Poisoner's Handbook, The (1995)       41       41      41         41\n",
       "Zeus and Roxanne (1997)                      6        6       6          6\n",
       "unknown                                      9        9       9          9\n",
       "Á köldum klaka (Cold Fever) (1994)           1        1       1          1\n",
       "\n",
       "[1664 rows x 4 columns]>"
      ]
     },
     "execution_count": 20,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "data.groupby('title').count().info"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "5. We can observe that there are 1664 movies with rating. Let's calculate the average rating of each movie"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>rating</th>\n",
       "      <th>num of ratings</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>title</th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>'Til There Was You (1997)</th>\n",
       "      <td>2.333333</td>\n",
       "      <td>9</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1-900 (1994)</th>\n",
       "      <td>2.600000</td>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>101 Dalmatians (1996)</th>\n",
       "      <td>2.908257</td>\n",
       "      <td>109</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>12 Angry Men (1957)</th>\n",
       "      <td>4.344000</td>\n",
       "      <td>125</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>187 (1997)</th>\n",
       "      <td>3.024390</td>\n",
       "      <td>41</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Young Guns II (1990)</th>\n",
       "      <td>2.772727</td>\n",
       "      <td>44</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Young Poisoner's Handbook, The (1995)</th>\n",
       "      <td>3.341463</td>\n",
       "      <td>41</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Zeus and Roxanne (1997)</th>\n",
       "      <td>2.166667</td>\n",
       "      <td>6</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>unknown</th>\n",
       "      <td>3.444444</td>\n",
       "      <td>9</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Á köldum klaka (Cold Fever) (1994)</th>\n",
       "      <td>3.000000</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>1664 rows × 2 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "                                         rating  num of ratings\n",
       "title                                                          \n",
       "'Til There Was You (1997)              2.333333               9\n",
       "1-900 (1994)                           2.600000               5\n",
       "101 Dalmatians (1996)                  2.908257             109\n",
       "12 Angry Men (1957)                    4.344000             125\n",
       "187 (1997)                             3.024390              41\n",
       "...                                         ...             ...\n",
       "Young Guns II (1990)                   2.772727              44\n",
       "Young Poisoner's Handbook, The (1995)  3.341463              41\n",
       "Zeus and Roxanne (1997)                2.166667               6\n",
       "unknown                                3.444444               9\n",
       "Á köldum klaka (Cold Fever) (1994)     3.000000               1\n",
       "\n",
       "[1664 rows x 2 columns]"
      ]
     },
     "execution_count": 23,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# creating dataframe with 'rating' count values \n",
    "ratings = pd.DataFrame(data.groupby('title')['rating'].mean())  \n",
    "\n",
    "#add another column called \"num of ratings\" that count the total rating\n",
    "ratings['num of ratings'] = pd.DataFrame(data.groupby('title')['rating'].count()) \n",
    "  \n",
    "ratings"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "6. Let's create a histogram to check out the number of ratings received against the count"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<Axes: >"
      ]
     },
     "execution_count": 26,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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",
      "text/plain": [
       "<Figure size 1000x400 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "import matplotlib.pyplot as plt \n",
    "import seaborn as sns \n",
    "  \n",
    "sns.set_style('white') \n",
    "%matplotlib inline \n",
    " \n",
    "# plot graph of 'num of ratings column' \n",
    "plt.figure(figsize =(10, 4)) \n",
    "  \n",
    "ratings['num of ratings'].hist(bins = 60) "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "From the histogram, we can observe that majority of the movies (more than 500) obtained less than 10 ratings"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<Axes: >"
      ]
     },
     "execution_count": 28,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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",
      "text/plain": [
       "<Figure size 1000x400 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "# plot graph of 'ratings' column \n",
    "plt.figure(figsize =(10, 4)) \n",
    "  \n",
    "ratings['rating'].hist(bins = 60) "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "From the histogram, we can observe that majority of the movies (more than120) obtained a rating around 3."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Section 3 Building User-Item Interactions Matrix"
   ]
  },
  {
   "attachments": {
    "image.png": {
     "image/png": "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"
    }
   },
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "User-item matrix is a basic foundation of traditional collaborative filtering techniques. In this practical, the rating for target movie item i for an active user can be predicted by using a simple weighted average (mean). \n",
    "\n",
    "![image.png](attachment:image.png)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "7. Let's build the user-item matrix"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 35,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>rating</th>\n",
       "      <th>num of ratings</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>title</th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>Star Wars (1977)</th>\n",
       "      <td>4.359589</td>\n",
       "      <td>584</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Contact (1997)</th>\n",
       "      <td>3.803536</td>\n",
       "      <td>509</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Fargo (1996)</th>\n",
       "      <td>4.155512</td>\n",
       "      <td>508</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Return of the Jedi (1983)</th>\n",
       "      <td>4.007890</td>\n",
       "      <td>507</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Liar Liar (1997)</th>\n",
       "      <td>3.156701</td>\n",
       "      <td>485</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>English Patient, The (1996)</th>\n",
       "      <td>3.656965</td>\n",
       "      <td>481</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Scream (1996)</th>\n",
       "      <td>3.441423</td>\n",
       "      <td>478</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Toy Story (1995)</th>\n",
       "      <td>3.878319</td>\n",
       "      <td>452</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Air Force One (1997)</th>\n",
       "      <td>3.631090</td>\n",
       "      <td>431</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Independence Day (ID4) (1996)</th>\n",
       "      <td>3.438228</td>\n",
       "      <td>429</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                                 rating  num of ratings\n",
       "title                                                  \n",
       "Star Wars (1977)               4.359589             584\n",
       "Contact (1997)                 3.803536             509\n",
       "Fargo (1996)                   4.155512             508\n",
       "Return of the Jedi (1983)      4.007890             507\n",
       "Liar Liar (1997)               3.156701             485\n",
       "English Patient, The (1996)    3.656965             481\n",
       "Scream (1996)                  3.441423             478\n",
       "Toy Story (1995)               3.878319             452\n",
       "Air Force One (1997)           3.631090             431\n",
       "Independence Day (ID4) (1996)  3.438228             429"
      ]
     },
     "execution_count": 35,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Sorting values according to  \n",
    "# the 'num of rating column' \n",
    "moviemat = data.pivot_table(index ='user_id',                        #use pivot_table to build 'rating' matrix based on 'user_id' and 'title'\n",
    "              columns ='title', values ='rating') \n",
    "  \n",
    "moviemat.head() \n",
    "  \n",
    "ratings.sort_values('num of ratings', ascending = False).head(10) "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "8. Now check out the Star Wars movie"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "This is item-item based"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 39,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "user_id\n",
       "0      5.0\n",
       "1      5.0\n",
       "2      5.0\n",
       "3      NaN\n",
       "4      5.0\n",
       "      ... \n",
       "939    NaN\n",
       "940    4.0\n",
       "941    NaN\n",
       "942    5.0\n",
       "943    4.0\n",
       "Name: Star Wars (1977), Length: 944, dtype: float64"
      ]
     },
     "execution_count": 39,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# analysing correlation with similar movies \n",
    "starwars_user_ratings = moviemat['Star Wars (1977)']            #to obtain the rating for Star Wars (1977)\n",
    "\n",
    "# you may try with other movie titles later\n",
    "starwars_user_ratings"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "9. We are interested to find out movies with similar ratings"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 42,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\User\\anaconda3\\Lib\\site-packages\\numpy\\lib\\function_base.py:2897: RuntimeWarning: invalid value encountered in divide\n",
      "  c /= stddev[:, None]\n",
      "C:\\Users\\User\\anaconda3\\Lib\\site-packages\\numpy\\lib\\function_base.py:2898: RuntimeWarning: invalid value encountered in divide\n",
      "  c /= stddev[None, :]\n",
      "C:\\Users\\User\\anaconda3\\Lib\\site-packages\\numpy\\lib\\function_base.py:2889: RuntimeWarning: Degrees of freedom <= 0 for slice\n",
      "  c = cov(x, y, rowvar, dtype=dtype)\n",
      "C:\\Users\\User\\anaconda3\\Lib\\site-packages\\numpy\\lib\\function_base.py:2748: RuntimeWarning: divide by zero encountered in divide\n",
      "  c *= np.true_divide(1, fact)\n",
      "C:\\Users\\User\\anaconda3\\Lib\\site-packages\\numpy\\lib\\function_base.py:2748: RuntimeWarning: invalid value encountered in multiply\n",
      "  c *= np.true_divide(1, fact)\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Correlation</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>title</th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>'Til There Was You (1997)</th>\n",
       "      <td>0.872872</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1-900 (1994)</th>\n",
       "      <td>-0.645497</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>101 Dalmatians (1996)</th>\n",
       "      <td>0.211132</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>12 Angry Men (1957)</th>\n",
       "      <td>0.184289</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>187 (1997)</th>\n",
       "      <td>0.027398</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                           Correlation\n",
       "title                                 \n",
       "'Til There Was You (1997)     0.872872\n",
       "1-900 (1994)                 -0.645497\n",
       "101 Dalmatians (1996)         0.211132\n",
       "12 Angry Men (1957)           0.184289\n",
       "187 (1997)                    0.027398"
      ]
     },
     "execution_count": 42,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# analysing correlation with similar movies \n",
    "similar_to_starwars = moviemat.corrwith(starwars_user_ratings)  #to find the correlation from all movies to the user input in previous step using .corrwith(starwars_user_ratings) \n",
    "  \n",
    "corr_starwars = pd.DataFrame(similar_to_starwars, columns =['Correlation']) \n",
    "corr_starwars.dropna(inplace = True) \n",
    "  \n",
    "corr_starwars.head() "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 44,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Correlation</th>\n",
       "      <th>num of ratings</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>title</th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>Star Wars (1977)</th>\n",
       "      <td>1.000000</td>\n",
       "      <td>584</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Empire Strikes Back, The (1980)</th>\n",
       "      <td>0.748353</td>\n",
       "      <td>368</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Return of the Jedi (1983)</th>\n",
       "      <td>0.672556</td>\n",
       "      <td>507</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Raiders of the Lost Ark (1981)</th>\n",
       "      <td>0.536117</td>\n",
       "      <td>420</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Austin Powers: International Man of Mystery (1997)</th>\n",
       "      <td>0.377433</td>\n",
       "      <td>130</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                                                    Correlation  \\\n",
       "title                                                             \n",
       "Star Wars (1977)                                       1.000000   \n",
       "Empire Strikes Back, The (1980)                        0.748353   \n",
       "Return of the Jedi (1983)                              0.672556   \n",
       "Raiders of the Lost Ark (1981)                         0.536117   \n",
       "Austin Powers: International Man of Mystery (1997)     0.377433   \n",
       "\n",
       "                                                    num of ratings  \n",
       "title                                                               \n",
       "Star Wars (1977)                                               584  \n",
       "Empire Strikes Back, The (1980)                                368  \n",
       "Return of the Jedi (1983)                                      507  \n",
       "Raiders of the Lost Ark (1981)                                 420  \n",
       "Austin Powers: International Man of Mystery (1997)             130  "
      ]
     },
     "execution_count": 44,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Similar movies like starwars \n",
    "corr_starwars.sort_values('Correlation', ascending = False).head(10) \n",
    "corr_starwars = corr_starwars.join(ratings['num of ratings']) \n",
    "  \n",
    "corr_starwars.head() \n",
    "  \n",
    "corr_starwars[corr_starwars['num of ratings']>100].sort_values('Correlation', ascending = False).head() "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Exercise"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Perform steps in <b>Section 3</b> to recommend similar movies to the user if he likes \n",
    "\n",
    "1) Liar Liar (1997)\n",
    "\n",
    "2) Return of the Jedi (1983)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
