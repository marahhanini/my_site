from rest_framework import mixins,viewsets
from .models import Question, Choice
from .serializers import QuestionSerializer, ChoiceSerializer

class QuestionViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class ChoiceViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
