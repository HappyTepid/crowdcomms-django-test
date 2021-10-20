from rest_framework import serializers

from bunnies.models import Bunny, RabbitHole


class RabbitHoleSerializer(serializers.ModelSerializer):

    bunnies = serializers.PrimaryKeyRelatedField(many=True, queryset=Bunny.objects.all())
    bunny_count = serializers.SerializerMethodField()

    @staticmethod
    def get_bunny_count(obj):
        return obj.bunnies.count()

    class Meta:
        model = RabbitHole
        fields = ('location', 'bunnies', 'bunny_count', 'owner')


class BunnySerializer(serializers.ModelSerializer):

    home = serializers.SlugRelatedField(queryset=RabbitHole.objects.all(), slug_field='location')
    family_members = serializers.SerializerMethodField()

    @staticmethod
    def get_family_members(obj):
        bunny_names = Bunny.objects.filter(
            home=obj.home.id).exclude(pk=obj.pk).values_list('name', flat=True)
        return bunny_names

    def validate(self, attrs):
        rabbit_hole = attrs['home']
        current_bunnies = rabbit_hole.bunnies.count()
        if current_bunnies >= rabbit_hole.bunnies_limit:
            raise serializers.ValidationError("Maximum number of bunnies exceeded")
        return attrs

    class Meta:
        model = Bunny
        fields = ('name', 'home', 'family_members')
