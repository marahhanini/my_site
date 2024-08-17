import logging
from rest_framework import mixins, viewsets
from .models import Question, Choice
from .serializers import QuestionSerializer, ChoiceSerializer

polls_logger = logging.getLogger('polls')

class QuestionViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def list(self, request, *args, **kwargs):
        polls_logger.info('QuestionViewSet list called')
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        polls_logger.info('QuestionViewSet create called')
        return super().create(request, *args, **kwargs)

class ChoiceViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

    def list(self, request, *args, **kwargs):
        polls_logger.info('ChoiceViewSet list called')
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        polls_logger.info('ChoiceViewSet create called')
        return super().create(request, *args, **kwargs)
