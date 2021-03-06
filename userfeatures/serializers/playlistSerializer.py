from rest_framework import serializers
from django.conf import settings
from users.models import SoundFileUser
from podcasts.models import Episode
from users.serializers import UserSerializerTokenized
from userfeatures.models import Playlist, EpisodePlaylist, PlaylistLike, EpisodeSavePoint, Subscription
from podcasts.serializers import EpisodeSerializerSmall, PodcastSerializerTiny

from django.contrib.auth.models import AnonymousUser

class EpisodePlaylistSerializer(serializers.ModelSerializer):
    episode = EpisodeSerializerSmall()
    time = serializers.SerializerMethodField(method_name='calculate_time')
    class Meta:
        model = EpisodePlaylist
        fields = ['episode','time']
    
    def calculate_time(self, instance):
        request = self.context.get('request')
        user = request.user
        if isinstance(user, AnonymousUser):
            return False; # No more work to do here.
        save = EpisodeSavePoint.objects.filter(user = user, episode=instance.episode).first()
        if save is None: 
            return 0
        else:
            return save.time

class PlaylistSerializerSmall(serializers.ModelSerializer):
    user = UserSerializerTokenized()
    class Meta:
        model = Playlist
        fields= ['name', 'pk', 'user', 'update_time']

class PlaylistSerializerPopular(serializers.ModelSerializer):
    user = UserSerializerTokenized()
    num_likes = serializers.SerializerMethodField(method_name='calculate_num_likes')    
    num_subs = serializers.SerializerMethodField(method_name='calculate_num_subs')
    
    class Meta:
        model = Playlist
        fields = ['name', 'user', 'pk', 'public', 'num_likes', 'num_subs', 'update_time']

    def calculate_num_subs(self, instance):
        if not instance.public:
            return 0
        return Subscription.objects.filter(playlist__pk=instance.pk).count()

    def calculate_num_likes(self, instance):
        """
            Calculate the number of likes for this given comment
        """
        if not instance.public:
            return 0
        return PlaylistLike.objects.filter(playlist__pk = instance.pk).count()


class PlaylistSerializer(serializers.ModelSerializer):
    episodes = EpisodePlaylistSerializer(many=True)
    user = UserSerializerTokenized()
    num_likes = serializers.SerializerMethodField(method_name='calculate_num_likes')
    cur_user_liked = serializers.SerializerMethodField(method_name='calculate_cur_user_liked')    
    num_subs = serializers.SerializerMethodField(method_name='calculate_num_subs')
    cur_user_sub= serializers.SerializerMethodField(method_name='calculate_cur_user_sub')

    class Meta:
        model = Playlist
        fields = ['name', 'user', 'pk', 
        'episodes', 'public', 'num_likes', 
        'cur_user_liked', 'num_subs', 'cur_user_sub', 'update_time']
    
    def calculate_num_subs(self, instance):
        if not instance.public:
            return 0
        return Subscription.objects.filter(playlist__pk=instance.pk).count()

    def calculate_cur_user_sub(self, instance):
        """
        
        """
        request = self.context.get('request')
        user = request.user

        if not instance.public:
            return False

        if isinstance(user, AnonymousUser):
            return False; # No more work to do here.

        sub = Subscription.objects.filter(playlist__pk = instance.pk, user=user).first()
        if sub is not None:
            return True
        else:
            return False

    def calculate_num_likes(self, instance):
        """
            Calculate the number of likes for this given comment
        """
        if not instance.public:
            return 0
        return PlaylistLike.objects.filter(playlist__pk = instance.pk).count()

    def calculate_cur_user_liked(self, instance):
        """
            Return true or false based on if current user liked given comment
        """
        request = self.context.get('request')
        user = request.user

        if not instance.public:
            return False 

        if isinstance(user, AnonymousUser):
            return False; # No more work to do here. 

        like = PlaylistLike.objects.filter(user=user, playlist__pk=instance.pk).first()

        if like is not None:
            return True
        else:
            return False