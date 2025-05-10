from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

# Base model for tour company content (articles, tips, etc.)
class Post(models.Model):
    title = models.CharField(max_length=255, help_text=_("The title of the content."))
    slug = models.SlugField(unique=True, help_text=_("URL-friendly identifier."))
    content = models.TextField(help_text=_("The main body of the content."))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts")
    is_published = models.BooleanField(default=True, help_text=_("Is this content visible to users?"))

    def __str__(self):
        return self.title
    
    def comment(self):
        return self.comments.all()

    class Meta:
        ordering = ["-created_at"]


# Model for user comments
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", help_text=_("The post associated with this comment."))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", help_text=_("The user who posted the comment."))
    content = models.TextField(help_text=_("The text content of the comment."))
    # parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies", help_text=_("If this is a reply, link to the parent comment."))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"
    
    def reply(self):
        return self.replies.all()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        
        
class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="replies", help_text="The comment being replied to.")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="replies", help_text="The user who made the reply.")
    content = models.TextField(help_text="The text content of the reply.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reply by {self.user.username} to {self.comment.id}"

    class Meta:
        ordering = ["-created_at"]


# Model for user actions (track Remove, Reply, Edit)
# class CommentAction(models.Model):
#     ACTION_TYPES = [
#         ('remove', _('Remove')),
#         ('reply', _('Reply')),
#         ('edit', _('Edit')),
#     ]

#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="actions")
#     action_type = models.CharField(max_length=10, choices=ACTION_TYPES, help_text=_("The type of action performed."))
#     performed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_actions", help_text=_("The user who performed this action."))
#     performed_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.get_action_type_display()} on {self.comment}"

#     class Meta:
#         ordering = ["-performed_at"]
#         verbose_name = _("Comment Action")
#         verbose_name_plural = _("Comment Actions")
