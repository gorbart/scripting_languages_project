import plotly.express as px
import pandas as pd


class PlotPainter:
    """
    Class PlotPainter is used to plot data associated with Tweets and Hashtags; the plots will be rendered at view pages
    """

    @staticmethod
    def plot_tweets(tweet_list):
        """
        plot_tweets produces bar plots of retweet and like numbers contained in Tweet objects
        :param tweet_list: list of Tweet objects
        :return: bar plot of Tweet continuous attributes as a HTML code in str object
        """

        tweet_df = pd.DataFrame({'retweets': [tweet.retweets for tweet in tweet_list],
                                 'likes': [tweet.likes for tweet in tweet_list]},
                                index=[' '.join(tweet.text.split()[:3]) + "..." for tweet in tweet_list])
        fig = px.bar(tweet_df, barmode='group', labels={'index': 'Tweet', 'value': 'count', 'variable': 'metric'},
                     hover_name=tweet_df.index)

        return fig.to_html()

    @staticmethod
    def plot_hashtags(hashtag_list):
        """
        plot_hashtags produces bar plots of tweet_volume numbers contained in Hashtag objects
        :param hashtag_list: list of Hashtag objects
        :return: bar plot of Hashtag continuous attributes as a HTML code in str object
        """

        hashtag_df = pd.DataFrame({'tweet_volume': [hashtag.tweet_volume for hashtag in hashtag_list]},
                                  index=[hashtag.text for hashtag in hashtag_list])
        fig = px.bar(hashtag_df, labels={'index': 'Hashtag', 'value': 'count', 'variable': 'metric'},
                     hover_name=hashtag_df.index)
        fig.update_layout(showlegend=False)
        return fig.to_html()
