import pytest
from tasks.models import Task


@pytest.mark.django_db
def test_task_creation_with_owner(django_user_model):
    """A Task can be created and correctly links to its owner."""
    user = django_user_model.objects.create_user(
        username="ashfall", password="testpass123"
    )
    task = Task.objects.create(
        title="Go to the supermarket",
        description="Buy eggs and bread",
        owner=user,
    )

    assert task.title == "Go to the supermarket"
    assert task.owner == user
    assert task.completed is False


@pytest.mark.django_db
def test_task_str_returns_title(django_user_model):
    """__str__ should return the task's title, not the default object repr."""
    user = django_user_model.objects.create_user(
        username="ashfall", password="testpass123"
    )
    task = Task.objects.create(title="Walk the dog", owner=user)

    assert str(task) == "Walk the dog"


@pytest.mark.django_db
def test_owner_reverse_relation(django_user_model):
    """A user should be able to access their tasks via the related_name."""
    user = django_user_model.objects.create_user(
        username="ashfall", password="testpass123"
    )
    Task.objects.create(title="Task one", owner=user)
    Task.objects.create(title="Task two", owner=user)

    assert user.tasks.count() == 2