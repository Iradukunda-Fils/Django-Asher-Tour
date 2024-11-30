from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .social import Post, Comment, Reply

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for Post model
    """
    # Columns to display in the list view
    list_display = (
        'title', 
        'slug', 
        'author', 
        'created_at', 
        'updated_at', 
        'is_published'
    )
    
    # Fields to use in search
    search_fields = (
        'title', 
        'content', 
        'author__username', 
        'slug'
    )
    
    # Filtering options
    list_filter = (
        'is_published', 
        'created_at', 
        'updated_at', 
        'author'
    )
    
    # Automatically generate slug from title
    prepopulated_fields = {'slug': ('title',)}
    
    # Customize the edit page
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'content')
        }),
        (_('Metadata'), {
            'fields': ('author', 'is_published')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    # Make created and updated fields read-only
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for Comment model
    """
    # Columns to display in the list view
    list_display = (
        'get_post_title', 
        'user', 
        'content_preview', 
        'created_at', 
        'updated_at'
    )
    
    # Fields to use in search
    search_fields = (
        'content', 
        'user__username', 
        'post__title'
    )
    
    # Filtering options
    list_filter = (
        'created_at', 
        'updated_at', 
        'user', 
        'post'
    )
    
    # Method to display post title in list view
    def get_post_title(self, obj):
        return obj.post.title
    get_post_title.short_description = _('Post')
    
    # Method to show a preview of comment content
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = _('Content Preview')

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for Reply model
    """
    # Columns to display in the list view
    list_display = (
        'get_comment_id', 
        'user', 
        'content_preview', 
        'created_at', 
        'updated_at'
    )
    
    # Fields to use in search
    search_fields = (
        'content', 
        'user__username', 
        'comment__id'
    )
    
    # Filtering options
    list_filter = (
        'created_at', 
        'updated_at', 
        'user'
    )
    
    # Method to display comment ID in list view
    def get_comment_id(self, obj):
        return obj.comment.id
    get_comment_id.short_description = _('Comment ID')
    
    # Method to show a preview of reply content
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = _('Content Preview')

class SocialAdmin(admin.AdminSite):
    """
    Custom admin site for social application
    """
    site_header = _('Social Platform Administration')
    site_title = _('Social Admin')
    index_title = _('Welcome to Social Platform Admin')

# Create an instance of the custom admin site
social_admin_site = SocialAdmin(name='socialadmin')

# Register models with the custom admin site
social_admin_site.register(Post, PostAdmin)
social_admin_site.register(Comment, CommentAdmin)
social_admin_site.register(Reply, ReplyAdmin)