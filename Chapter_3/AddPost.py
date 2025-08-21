from API import api_instance
from Models import Post
def add_post(post: Post):
    # Check if the post is None or if any required fields are empty
	 # Returns the result of addition operation
    if post is None or len(post.creator_name) == 0 or len(post.content) == 0:
        return None
	 # Adding the post using the API instance
    did_add = api_instance.add_post(post)
    return did_add
