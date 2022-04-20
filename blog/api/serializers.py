from rest_framework import serializers
from blog.models import Post
MIN_TITLE_LENGTH = 5
MIN_BODY_LENGTH = 50

class PostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username_from_author')

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'date_posted', 'username']

    def get_username_from_author(self, post):
        username = post.author.username
        return username

class PostUpdateSerializer(serializers.ModelSerializer):

	class Meta:
		model = Post
		fields = ['title', 'content']

	def validate(self, post):
		try:
			title = post['title']
			if len(title) < MIN_TITLE_LENGTH:
				raise serializers.ValidationError({"response": f"Enter a title longer than {str(MIN_TITLE_LENGTH)} characters."})
			
			content = post['content']
			if len(content) < MIN_BODY_LENGTH:
				raise serializers.ValidationError({"response": f"Enter a body longer than {str(MIN_BODY_LENGTH)} characters."})
		except KeyError:
			pass
		return post

class PostCreateSerializer(serializers.ModelSerializer):

	class Meta:
		model = Post
		fields = ['title', 'content', 'date_posted', 'author']

	def save(self):
		
		try:
			title = self.validated_data['title']
			if len(title) < MIN_TITLE_LENGTH:
				raise serializers.ValidationError({"response": f"Enter a title longer than {str(MIN_TITLE_LENGTH)} characters."})
			
			content = self.validated_data['content']
			if len(content) < MIN_BODY_LENGTH:
				raise serializers.ValidationError({"response": f"Enter a body longer than {str(MIN_BODY_LENGTH)} characters."})
			
			post = Post(
						author=self.validated_data['author'],
						title=title,
						content=content
						)
			post.save()
			return post
		except KeyError:
			raise serializers.ValidationError({"response": "You must have a title and some content"}) 