from praw import Reddit

class PostGrabber:
    def __init__(self, subreddit_name: str, post_category: str):
        self.reddit_instance = Reddit("bot")
        self.subreddit = self.reddit_instance.subreddit(subreddit_name)
        self.post_iterator = self.get_iterator(post_category)
        self.bad_flairs = ["update", "meta"]
        self.post_counter = 0

    # Return next Reddit post from iterator
    def next_post(self):
        iterations = 0
        for submission in self.post_iterator:
            # Filter any moderator/update posts
            if iterations < self.post_counter or submission.stickied or submission.link_flair_text.lower() in self.bad_flairs:
                iterations += 1
            else:
                self.post_counter += 1
                return submission
            
    # Return post iterator for any category
    def get_iterator(self, post_category: str):
        if post_category == "top":
            return self.subreddit.top()
        elif post_category == "hot":
            return self.subreddit.hot()
        elif post_category == "new":
            return self.subreddit.new()
        elif post_category == "controversial":
            return self.subreddit.controversial()
        elif post_category == "rising":
            return self.subreddit.rising()
        elif post_category == "gilded":
            return self.subreddit.gilded()
        else:
            return self.subreddit.top()
    
    def change_subreddit(self, new_subreddit_name: str, post_category: str):
        self.subreddit = self.reddit_instance.subreddit(new_subreddit_name)
        self.post_iterator = self.get_iterator(post_category)

    def change_post_category(self, new_post_category: str):
        self.post_iterator = self.get_iterator(new_post_category)

    # Format post text and merge with title
    def get_post_text(self, post: str) -> str:
        full = (post.title + " " + post.selftext).replace("\n", " ").replace("\t", " ").replace("AITA", "Am I the Asshole")
        # Removes a last period from the text
        if (full[-1] == '.'):
            full = full[:-1]

        return full