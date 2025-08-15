import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_register_view_get(client):
    url = reverse('register')
    response = client.get(url)

    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['form_type'] == 'register'
    assert 'add_form.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_register_view_post_valid_data(client):
    url = reverse('register')
    data = {
        'first_name': 'Test',
        'last_name': 'User',
        'username': 'testuser',
        'email': 'test@gmail.com',
        'password1': 'strongpassword123',
        'password2': 'strongpassword123',
    }
    response = client.post(url, data, follow=True)

    assert User.objects.filter(username='testuser').exists()
    assert response.context['user'].is_authenticated
    assert response.redirect_chain[-1][0] == reverse('home')

@pytest.mark.django_db
def test_register_view_post_invalid_data(client):
    url = reverse('register')
    data = {
        'username': '',
        'password1': '123',
        'password2': '456',
    }
    response = client.post(url, data)

    assert response.status_code == 200
    assert not User.objects.exists()
    assert 'add_form.html' in [t.name for t in response.templates]


@pytest.fixture
def test_user(db):
    return User.objects.create_user(username='testuser', password='strongpassword123')

@pytest.mark.django_db
def test_login_view_get(client):
    url = reverse('login')
    response = client.get(url)

    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['form_type'] == 'login'
    assert 'add_form.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_login_view_post_valid_data(client, test_user):
    url = reverse('login')
    data = {
        'username': 'testuser',
        'password': 'strongpassword123',
    }
    response = client.post(url, data, follow=True)

    assert response.context['user'].is_authenticated
    assert response.redirect_chain[-1][0] == reverse('home')

@pytest.mark.django_db
def test_login_view_post_invalid_data(client, test_user):
    url = reverse('login')
    data = {
        'username': 'testuser',
        'password': 'wrongpassword',
    }
    response = client.post(url, data)

    assert response.status_code == 200
    assert not response.context['user'].is_authenticated
    assert 'error' in response.context

@pytest.fixture
def test_user(db):
    user = User.objects.create_user(
        username='testuser',
        password='strongpassword123',
        email='old@example.com'
    )
    # zakładam, że masz OneToOne do modelu Profile tworzony sygnałem post_save
    user.profile.bio = "Old bio"
    user.profile.save()
    return user

@pytest.mark.django_db
def test_profile_view_get(client, test_user):
    """GET zwraca formularze edycji profilu i użytkownika"""
    client.login(username='testuser', password='strongpassword123')
    url = reverse('profile')
    response = client.get(url)

    assert response.status_code == 200
    assert 'user_form' in response.context
    assert 'profile_form' in response.context
    assert 'profile.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_profile_view_post_valid_data(client, test_user):
    client.login(username='testuser', password='strongpassword123')
    url = reverse('profile')
    data = {
        'first_name': 'New',
        'last_name': 'Name',
        'username': 'newusername',
        'email': 'new@example.com',
        'bio': 'New bio text',
    }
    response = client.post(url, data, follow=True)

    test_user.refresh_from_db()

    assert response.status_code == 200
    assert response.redirect_chain[-1][0] == reverse('profile')
    assert test_user.first_name == 'New'
    assert test_user.last_name == 'Name'
    assert test_user.username == 'newusername'
    assert test_user.email == 'new@example.com'
    assert test_user.profile.bio == 'New bio text'
