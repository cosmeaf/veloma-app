from rest_framework import serializers

from .models import (
    Person,
    UserProfile
)


class PersonSerializer(serializers.ModelSerializer):

    class Meta:

        model = Person

        fields = (
            "id",
            "name",
            "nif",
            "phone",
            "created_at"
        )

        read_only_fields = ("created_at",)


class UserProfileSerializer(serializers.ModelSerializer):

    person = PersonSerializer()

    class Meta:

        model = UserProfile

        fields = (
            "id",
            "user",
            "person",
            "onboarding_completed",
            "created_at"
        )

        read_only_fields = (
            "user",
            "onboarding_completed",
            "created_at"
        )

    def update(self, instance, validated_data):

        person_data = validated_data.pop("person", None)

        if person_data:

            for field, value in person_data.items():

                setattr(instance.person, field, value)

            instance.person.save()

        instance.onboarding_completed = True

        instance.save()

        return instance