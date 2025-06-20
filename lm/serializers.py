from rest_framework import serializers
from lms.models import Course, Lesson, Subscription
from lms.validators import VideoValidator


class CourseSerializer(serializers.ModelSerializer):
    lesson = serializers.SerializerMethodField()
    subscription = serializers.SerializerMethodField(read_only=True)

    def get_subscription(self, instance):
        user = self.context["request"].user
        return Subscription.objects.filter(user=user).filter(course=instance).exists()

    def get_lesson(self, course):
        return [lesson.title for lesson in Lesson.objects.filter(course=course)]

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
    count_course_with_same_lessons = serializers.SerializerMethodField()
    course = CourseSerializer()
    subscription_course = serializers.SerializerMethodField()
    sign_up = serializers.SerializerMethodField()

    def get_count_course_with_same_lessons(self, lesson):
        return Course.objects.filter(course=lesson.course).count()

    def get_subscription_course(self, course):
        return Course.objects.filter(course=course)

    def get_sign_up(self, course):
        return Course.objects.filter(course=course)

    class Meta:
        model = Course
        fields = ("lesson", "course", "count_course_with_same_lessons", "subscription")


class LessonSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Lesson
        fields = "__all__"
        video = (serializers.CharField(validators=[VideoValidator(field="title")]),)


class LessonCreateSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Lesson
        fields = "__all__"
        video = serializers.CharField(
            validators=[
                VideoValidator(field="title"),
                serializers.UniqueTogetherValidator(
                    fields="title", queryset=Lesson.objects.all()
                ),
            ]
        )


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = "__all__"
