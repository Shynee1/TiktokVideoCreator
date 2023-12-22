from praw import Reddit
import random
import string

class PostGrabber:
    def __init__(self, subreddit_name: str, post_category: str):
        self.reddit_instance = Reddit("bot")
        self.subreddit = self.reddit_instance.subreddit(subreddit_name)
        self.posts = list(self.get_iterator(post_category))
        self.bad_flairs = ["update", "meta"]
        self.post_counter = 0

    # Return next Reddit post from iterator
    def next_post(self):
        index = random.randint(0, len(self.posts) - 1)
        post = self.posts[index]
    
        while post.stickied or post.link_flair_text.lower() in self.bad_flairs:
            index = random.randint(0, len(self.posts) - 1)
            post = self.posts[index]

        print(f'Successfully grabbed Reddit post from r/{self.subreddit.display_name}')
        print(f'Post Title: {post.title}')
        return post
            
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
        full = ((post.title + " " + post.selftext)
                .replace("\n", " ")
                .replace("\t", " ")
                .replace("AITA", "Am I the Asshole")
                .replace("SIL", "sister-in-law")
                .replace("GF", "girlfriend")
                .replace("”", "")
                .replace("“", "")
                .replace("\"", "")
                .replace("\'", "")
        )

        # Removes last punctuation mark from the text
        if (full[-1] in string.punctuation ):
            full = full[:-1]

        return full