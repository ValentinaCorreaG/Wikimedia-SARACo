"""
Tests for users app authentication and profile functionality.

High-priority tests for authentication pipeline and user management.
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from users.models import UserProfile, TeamArea, Position
from users.pipeline import associate_by_wiki_handle, get_username
from django.contrib.auth.models import Group

User = get_user_model()


class UserProfileModelTest(TestCase):
    """Test UserProfile model and signal creation."""

    def test_user_profile_created_on_user_creation(self):
        """Test that UserProfile is automatically created when User is created."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Profile should be created automatically
        self.assertTrue(hasattr(user, 'profile'))
        self.assertIsInstance(user.profile, UserProfile)

    def test_user_profile_string_representation(self):
        """Test UserProfile __str__ method."""
        user = User.objects.create_user(username='testuser')
        user.profile.professional_wiki_handle = 'WikiTestUser'
        user.profile.save()
        
        self.assertEqual(str(user.profile), 'WikiTestUser')


class AuthenticationPipelineTest(TestCase):
    """Test custom authentication pipeline functions."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username='existing_user')
        self.user.profile.professional_wiki_handle = 'ExistingWikiUser'
        self.user.profile.save()

    def test_associate_by_wiki_handle_existing_user(self):
        """Test matching existing users by wiki handle (case-insensitive)."""
        result = associate_by_wiki_handle(
            backend=None,
            uid='12345',
            user=None,
            details={'username': 'existingwikiuser'}  # lowercase
        )
        
        self.assertIn('user', result)
        self.assertEqual(result['user'], self.user)

    def test_associate_by_wiki_handle_by_username(self):
        """Test fallback to username matching."""
        result = associate_by_wiki_handle(
            backend=None,
            uid='12345',
            user=None,
            details={'username': 'existing_user'}
        )
        
        self.assertIn('user', result)
        self.assertEqual(result['user'], self.user)

    def test_associate_by_wiki_handle_no_match(self):
        """Test when no user matches."""
        result = associate_by_wiki_handle(
            backend=None,
            uid='12345',
            user=None,
            details={'username': 'nonexistent_user'}
        )
        
        self.assertEqual(result, {})

    def test_associate_by_wiki_handle_already_authenticated(self):
        """Test when user is already authenticated."""
        result = associate_by_wiki_handle(
            backend=None,
            uid='12345',
            user=self.user,
            details={'username': 'any_username'}
        )
        
        self.assertEqual(result, {'user': self.user})

    def test_get_username_existing_user(self):
        """Test username resolution for existing user."""
        result = get_username(
            strategy=None,
            details={'username': 'new_username'},
            user=self.user
        )
        
        self.assertEqual(result['username'], 'existing_user')

    def test_get_username_new_user(self):
        """Test username resolution for new user."""
        result = get_username(
            strategy=None,
            details={'username': 'brand_new_user'},
            user=None
        )
        
        self.assertEqual(result['username'], 'brand_new_user')

    def test_get_username_conflict_resolution(self):
        """Test username conflict handling."""
        result = get_username(
            strategy=None,
            details={'username': 'existing_user'},
            user=None
        )
        
        # Should append _1 to resolve conflict
        self.assertEqual(result['username'], 'existing_user_1')

    def test_get_username_multiple_conflicts(self):
        """Test multiple username conflicts."""
        User.objects.create_user(username='existing_user_1')
        User.objects.create_user(username='existing_user_2')
        
        result = get_username(
            strategy=None,
            details={'username': 'existing_user'},
            user=None
        )
        
        # Should append _3 to resolve conflicts
        self.assertEqual(result['username'], 'existing_user_3')


class AuthenticationViewsTest(TestCase):
    """Test authentication views."""

    def setUp(self):
        """Set up test client and user."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_login_view_get(self):
        """Test login view displays correctly."""
        response = self.client.get(reverse('users:login'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_view_authenticated_redirect(self):
        """Test authenticated users are redirected from login."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:login'))
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))

    def test_logout_view(self):
        """Test logout functionality."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:logout'))
        
        self.assertEqual(response.status_code, 302)
        # User should be logged out
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_profile_view_requires_login(self):
        """Test profile view requires authentication."""
        response = self.client.get(reverse('users:profile'))
        
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('users:login'), response.url)

    def test_profile_view_authenticated(self):
        """Test profile view for authenticated user."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:profile'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_profile_detail_view(self):
        """Test viewing another user's profile."""
        self.client.login(username='testuser', password='testpass123')
        other_user = User.objects.create_user(username='otheruser')
        
        response = self.client.get(
            reverse('users:profile_detail', kwargs={'username': 'otheruser'})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'otheruser')

    def test_user_list_view_requires_permission(self):
        """Test user list view requires proper permissions."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:user_list'))
        
        # Should be forbidden without permission
        self.assertEqual(response.status_code, 403)

    def test_user_list_view_with_permission(self):
        """Test user list view with proper permissions."""
        self.user.is_staff = True
        self.user.save()
        
        from django.contrib.auth.models import Permission
        permission = Permission.objects.get(codename='view_user')
        self.user.user_permissions.add(permission)
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:user_list'))
        
        self.assertEqual(response.status_code, 200)


class HTMXViewsTest(TestCase):
    """Test HTMX-specific functionality."""

    def setUp(self):
        """Set up test client and user."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_profile_view_htmx_partial(self):
        """Test profile view returns partial for HTMX requests."""
        response = self.client.get(
            reverse('users:profile'),
            HTTP_HX_REQUEST='true'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/partials/profile_detail.html')

    def test_login_view_htmx_partial(self):
        """Test login view returns partial for HTMX requests."""
        self.client.logout()
        response = self.client.get(
            reverse('users:login'),
            HTTP_HX_REQUEST='true'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/partials/login_form.html')


class TeamAreaPositionTest(TestCase):
    """Test TeamArea and Position models."""

    def setUp(self):
        """Set up test data."""
        self.group = Group.objects.create(name='Test Group')
        self.team_area = TeamArea.objects.create(
            text='Engineering',
            code='ENG'
        )

    def test_team_area_creation(self):
        """Test TeamArea model creation."""
        self.assertEqual(str(self.team_area), 'Engineering')
        self.assertEqual(self.team_area.code, 'ENG')

    def test_position_creation(self):
        """Test Position model creation."""
        position = Position.objects.create(
            text='Senior Developer',
            type=self.group,
            area_associated=self.team_area
        )
        
        self.assertEqual(str(position), 'Senior Developer')
        self.assertEqual(position.area_associated, self.team_area)

    def test_position_unique_together(self):
        """Test Position unique_together constraint."""
        Position.objects.create(
            text='Developer',
            type=self.group,
            area_associated=self.team_area
        )
        
        # Creating another position with same text and area should fail
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Position.objects.create(
                text='Developer',
                type=self.group,
                area_associated=self.team_area
            )
