# from transformers import pipeline

# # Charger le modèle de classification zero-shot
# classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# # Liste de titres de Reddit
# titles = [
#     "The stock market is crashing!",
#     "Global warming is accelerating faster than expected",
#     "New immigration policies spark controversy",
#     "Education reform bill introduced in Congress",
#     "What are the best ways to save energy at home?"
# ]

# # Catégories à définir dynamiquement
# categories = ["économie", "environnement", "immigration", "éducation", "autres"]

# # comment_data = {
# #                     "author": comment.author.name if comment.author else "Deleted",
# #                     "body": comment.body,
# #                     "subreddit": comment.subreddit.display_name.lower(),
# #                     "created_at": datetime.fromtimestamp(comment.created_utc).isoformat(),
# #                     "timestamp": comment.created_utc,
# #                     "topic_title": f"{subreddit.title}: {submission.title}",  # Subreddit title + Topic title
# #                 }

# def topic_clf(comment_data):
#     category = classifier(comment_data['topic_title'], candidate_labels=categories)
#     comment_data['class'] = category['labels'][0]
#     return comment_data