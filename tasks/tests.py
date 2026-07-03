import pytest
from tasks.models import Task
from rest_framework.test import APIClient

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


@pytest.mark.django_db
class TestTaskAPI:

    def test_unauthenticated_user_cannot_list_tasks(self):
        client = APIClient()
        response = client.get('/api/tasks/')
        assert response.status_code == 401



    def test_user_cannot_see_other_users_tasks(self, django_user_model):
        user1 = django_user_model.objects.create_user(username="user1", password="testpass123")
        user2 = django_user_model.objects.create_user(username="user2", password="testpass123")

        Task.objects.create(title="User1's task", owner=user1)

        client = APIClient()
        client.force_authenticate(user=user2)

        response = client.get('/api/tasks/')

        assert response.status_code == 200
        assert len(response.data) == 0