from django.db import models
from django.contrib.auth.models import User


# ---------------------------------------------------------------------------
# User Profile
# Extends Django's built-in User with nutrition/health data from complete_profile.html
# ---------------------------------------------------------------------------

class UserProfile(models.Model):

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    GOAL_CHOICES = [
        ('lose_weight', 'Lose Weight'),
        ('gain_weight', 'Gain Weight'),
        ('build_muscle', 'Build Muscle'),
        ('maintain_weight', 'Maintain Weight'),
    ]

    DIET_CHOICES = [
        ('vegetarian', 'Vegetarian'),
        ('non_vegetarian', 'Non-Vegetarian'),
        ('vegan', 'Vegan'),
        ('eggetarian', 'Eggetarian'),
    ]

    ACTIVITY_CHOICES = [
        ('sedentary', 'Sedentary'),
        ('lightly_active', 'Lightly Active'),
        ('moderately_active', 'Moderately Active'),
        ('very_active', 'Very Active'),
    ]

    user            = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name       = models.CharField(max_length=150, blank=True)
    age             = models.PositiveIntegerField(null=True, blank=True)
    gender          = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    height_cm       = models.FloatField(null=True, blank=True)
    weight_kg       = models.FloatField(null=True, blank=True)
    target_weight_kg= models.FloatField(null=True, blank=True)
    goal            = models.CharField(max_length=20, choices=GOAL_CHOICES, blank=True)
    diet_type       = models.CharField(max_length=20, choices=DIET_CHOICES, blank=True)
    activity_level  = models.CharField(max_length=20, choices=ACTIVITY_CHOICES, blank=True)
    streak_days     = models.PositiveIntegerField(default=0)
    profile_complete= models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


# ---------------------------------------------------------------------------
# Daily Nutrition Log
# Tracks per-day totals shown on the dashboard (calories, protein, carbs, fats, fiber)
# ---------------------------------------------------------------------------

class DailyLog(models.Model):

    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_logs')
    date        = models.DateField()

    # Targets (copied from profile at time of log creation so history is preserved)
    cal_target      = models.PositiveIntegerField(default=0)
    protein_target  = models.PositiveIntegerField(default=0)
    carbs_target    = models.PositiveIntegerField(default=0)
    fats_target     = models.PositiveIntegerField(default=0)
    fiber_target    = models.PositiveIntegerField(default=0)

    # Running totals (updated each time a meal is logged)
    cal_total       = models.PositiveIntegerField(default=0)
    protein_total   = models.PositiveIntegerField(default=0)
    carbs_total     = models.PositiveIntegerField(default=0)
    fats_total      = models.PositiveIntegerField(default=0)
    fiber_total     = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} — {self.date}"


# ---------------------------------------------------------------------------
# Meal Entry
# Each individual meal logged during a day (shown in the meal journal)
# ---------------------------------------------------------------------------

class MealEntry(models.Model):

    daily_log   = models.ForeignKey(DailyLog, on_delete=models.CASCADE, related_name='meals')
    name        = models.CharField(max_length=200)
    logged_at   = models.DateTimeField(auto_now_add=True)

    calories    = models.PositiveIntegerField(default=0)
    protein_g   = models.PositiveIntegerField(default=0)
    carbs_g     = models.PositiveIntegerField(default=0)
    fats_g      = models.PositiveIntegerField(default=0)
    fiber_g     = models.PositiveIntegerField(default=0)

    # Optional: linked to an image upload if the meal came from the image analyser
    food_image  = models.ForeignKey('FoodImage', on_delete=models.SET_NULL, null=True, blank=True, related_name='meals')

    def __str__(self):
        return f"{self.name} ({self.calories} cal) — {self.daily_log.date}"


# ---------------------------------------------------------------------------
# Food Image Upload
# Stores uploaded meal photos for nutrition analysis
# ---------------------------------------------------------------------------

class FoodImage(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('analysed', 'Analysed'),
        ('failed', 'Failed'),
    ]

    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='food_images')
    image       = models.ImageField(upload_to='food_images/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    # Raw analysis result from the AI model (JSON string or plain text)
    analysis_result = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} — {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"


# ---------------------------------------------------------------------------
# Chatbot Message
# Stores per-user chat history — each message is one row
# ---------------------------------------------------------------------------

class ChatMessage(models.Model):

    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ]

    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    role        = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content     = models.TextField()
    timestamp   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"[{self.role}] {self.user.username} — {self.timestamp.strftime('%H:%M %d %b')}"