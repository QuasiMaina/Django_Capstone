from django.db import models
import uuid

DISORDER_TYPES = (
    ('GAD', 'Generalized Anxiety Disorder'),
    ('SAD', 'Social Anxiety Disorder'),
    ('PD', 'Panic Disorder'),
    ('OCD', 'Obsessive Compulsive Disorder'),
    ('PTSD', 'Post-Traumatic Stress Disorder'),
)

# Generate unique session IDs
def generate_session_id():
    return str(uuid.uuid4())


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    order = models.IntegerField(default=0)  # Added so fixture can load

    def __str__(self):
        return f"{self.order}. {self.text[:50]}"


class Choice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices'
    )
    text = models.CharField(max_length=255)
    order = models.IntegerField(default=0)
    score = models.IntegerField()
    disorder_type = models.CharField(
        max_length=100,
        choices=DISORDER_TYPES,
        blank=True,
        null=True
    )
    next_question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='next_choices',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.order}. {self.text[:50]}"


class GameSession(models.Model):
    session_id = models.CharField(
        max_length=100,
        default=generate_session_id,
        unique=True
    )
    score = models.IntegerField(default=0)
    current_node_id = models.CharField(max_length=100, blank=True, null=True)
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.session_id}"

    @property
    def session_key(self):
        return self.session_id


class ChoiceLog(models.Model):
    session = models.ForeignKey(GameSession, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    disorder_type = models.CharField(
        choices=DISORDER_TYPES,
        max_length=10,
        blank=True,
        null=True
    )
    score_given = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.session} - {self.choice.text} ({self.disorder_type})"
