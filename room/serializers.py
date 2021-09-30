from rest_framework import serializers
from room.models import Room, Image, Favorite, Rating
from review.serializers import CommentSerializer


class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'user', 'text', 'created_at', 'updated_at', 'rating_avg', )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['img'] = RoomImagesSerializer(instance.img.all(), many=True).data
        rep['likes_count'] = instance.likes.count()
        return rep


class RoomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        rep['img'] = RoomImagesSerializer(instance.img.all(), many=True).data
        rep['likes_count'] = instance.likes.count()
        return rep


class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        exclude = ('user', )

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class RoomImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('images', )

    def get_image_url(self, obj):
        if obj.images:
            return obj.images.url
        return ''

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['img'] = self.get_image_url(instance)
        return representation


class FavoriteRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'

        def get_favorite(self, obj):
            if obj.is_favorite:
                return obj.is_favorite
            return ''

        def to_representation(self, instance):
            rep = super().to_representation(instance)
            rep['favorites'] = self.get_favorite(instance)
            return rep


class RatingSerializer(serializers.ModelSerializer):
    publication = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Room.objects.all())
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Rating
        fields = '__all__'

    def validate(self, attrs):
        room = attrs.get('room')
        request = self.context.get('request')
        user = request.user
        if Rating.objects.filter(room=room, user=user).exists():
            raise serializers.ValidationError('Вы уже голосовали')
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)
