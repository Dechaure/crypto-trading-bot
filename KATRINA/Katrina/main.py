
import san
import pandas as pd
import datetime

today = datetime.date.today()
week_early = today - datetime.timedelta(days=7)
interval = "1d"


api_key = None
with open("./auth","r") as f:
    api_key=f.readline()


san.ApiConfig.api_key =api_key


metrics = ['sentiment_balance_total']

def get_metric(metric,coin, start_date,end_date,interv):
    """Returns a Pandas Dataframe that contains the specified metric.
    Parameters:
        metr: Metric you want to get. Use san.available_metrics() to see them all.
        coin: name of the cryptocurrency you want to get the metric of.
        start_date, end_date:  A date or datetime in iso8601 format specifying the start and end datetime
                              for the returned data or the string for ex: 2018-06-01,
                              or a string, representing the relative datetime utc_now-<interval>
        interv: The interval of the returned data - an integer followed by one of: s, m, h, d or w
    """

    metr = metric + "/" + coin
    result = san.get(metr, from_date=start_date, to_date=end_date, interval=interv)

    return result



"""res = get_metric(metric=metrics[0] ,
                 coin="Decentraland",
                 start_date=week_early.isoformat(),
                 end_date=today.isoformat(),
                 interv=interval)
"""

res = san.get(
    metrics[0] + "/" + "santiment",
    from_date="2021-09-01",
    to_date="2021-10-14",
    interval="30m"
)




