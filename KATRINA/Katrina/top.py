import san
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import os
import gc
from time import sleep
import sys
scaler = StandardScaler()

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
api_key = None
with open("./auth","r") as f:
    api_key=f.readline()
san.ApiConfig.api_key =api_key
top_10 = [

    "vechain",
    "stellar"
]


def query_price(coin):

    result =san.get(
        "price_usd/" + coin,
        from_date="2021-10-01",
        to_date="2021-10-14",
            interval="2h")

    return result


def query_social_trend(coin,met):

    result = san.get(
        met + "/" + coin,
        from_date="2021-10-01",
        to_date="2021-10-14",
        interval="2h")


    return result


def get_all_graphs(coin,met):

    df1 = query_price(coin)
    df2 = query_social_trend(coin,met)

    df1 = pd.DataFrame(scaler.fit_transform(df1), columns=df1.columns, index=df1.index)
    df2 = pd.DataFrame(scaler.fit_transform(df2), columns=df2.columns, index=df2.index)


    plt.figure().set_size_inches(45, 20)
    plt.plot(df1,color="blue",label="price")
    plt.plot(df2,color="red",label=met)

    plt.title(coin)

    plt.legend()
    if not os.path.exists('./graphics/'+coin):
        os.makedirs("./graphics/"+coin)

    plt.savefig("./graphics/"+coin + "/"+ coin+"_"+met+".jpg",dpi=60)
    plt.clf()
    plt.cla()
    plt.close("all")
    gc.collect()




data = []

for coin in top_10:

    metrics = ['sentiment_balance_bitcointalk',
     'sentiment_balance_reddit',
     'sentiment_balance_telegram',
     'sentiment_balance_total',
     'sentiment_balance_total_change_1d',
     'sentiment_balance_total_change_30d',
     'sentiment_balance_total_change_7d',
     'sentiment_balance_twitter',
     'sentiment_negative_bitcointalk',
     'sentiment_negative_reddit',
     'sentiment_negative_telegram',
     'sentiment_negative_total',
     'sentiment_negative_twitter',
     'sentiment_positive_bitcointalk',
     'sentiment_positive_reddit',
     'sentiment_positive_telegram',
     'sentiment_positive_total',
     'sentiment_positive_twitter',
     'sentiment_volume_consumed_bitcointalk',
     'sentiment_volume_consumed_reddit',
     'sentiment_volume_consumed_telegram',
     'sentiment_volume_consumed_total',
     'sentiment_volume_consumed_total_change_1d',
     'sentiment_volume_consumed_total_change_30d',
     'sentiment_volume_consumed_total_change_7d',
     'sentiment_volume_consumed_twitter',
     'social_dominance_bitcointalk',
     'social_dominance_bitcointalk_1h_moving_average',
     'social_dominance_bitcointalk_24h_moving_average',
     'social_dominance_reddit',
     'social_dominance_reddit_1h_moving_average',
     'social_dominance_reddit_24h_moving_average',
     'social_dominance_telegram',
     'social_dominance_telegram_1h_moving_average',
     'social_dominance_telegram_24h_moving_average',
     'social_dominance_total',
     'social_dominance_total_1h_moving_average',
     'social_dominance_total_1h_moving_average_change_1d',
     'social_dominance_total_1h_moving_average_change_30d',
     'social_dominance_total_1h_moving_average_change_7d',
     'social_dominance_total_24h_moving_average',
     'social_dominance_total_24h_moving_average_change_1d',
     'social_dominance_total_24h_moving_average_change_30d',
     'social_dominance_total_24h_moving_average_change_7d',
     'social_dominance_total_change_1d',
     'social_dominance_total_change_30d',
     'social_dominance_total_change_7d',
     'social_dominance_twitter',
     'social_dominance_twitter_1h_moving_average',
     'social_dominance_twitter_24h_moving_average',
     'social_volume_bitcointalk',
     'social_volume_reddit',
     'social_volume_telegram',
     'social_volume_total',
     'social_volume_total_change_1d',
     'social_volume_total_change_30d',
     'social_volume_total_change_7d',
     'social_volume_twitter',
     'twitter_followers',
     'unique_social_volume_total_1h',
     'unique_social_volume_total_5m']
    df1 = query_price(coin)
    for met in metrics:
        df2 = query_social_trend(coin, met)
        try:
            correl =df1.corrwith(df2).values[0]
        except Exception as e:
            print(sys.exc_info()[0])
            print(e)
            correl = int("-100")
        data.append([coin,met,correl])



print(data)
df = pd.DataFrame(data=data,columns=["coin","metric","correl"])




df.to_csv("THE_CORRELATION.csv")



