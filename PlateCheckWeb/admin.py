from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, DailyLog, MealEntry, FoodImage, ChatMessage


# ---------------------------------------------------------------------------
# Inlines — shown nested under their parent model
# ---------------------------------------------------------------------------

class UserProfileInline(admin.StackedInline):
    model         = UserProfile
    can_delete    = False
    verbose_name  = 'Profile'
    fields        = (
        'full_name', 'age', 'gender',
        'height_cm', 'weight_kg', 'target_weight_kg',
        'goal', 'diet_type', 'activity_level',
        'streak_days', 'profile_complete',
    )
    readonly_fields = ('streak_days',)


class MealEntryInline(admin.TabularInline):
    model           = MealEntry
    extra           = 0
    readonly_fields = ('name', 'calories', 'protein_g', 'carbs_g', 'fats_g', 'fiber_g', 'logged_at')
    can_delete      = False


class DailyLogInline(admin.TabularInline):
    model           = DailyLog
    extra           = 0
    readonly_fields = (
        'date',
        'cal_target', 'protein_target', 'carbs_target', 'fats_target', 'fiber_target',
        'cal_total',  'protein_total',  'carbs_total',  'fats_total',  'fiber_total',
    )
    can_delete      = False
    show_change_link = True


class FoodImageInline(admin.TabularInline):
    model           = FoodImage
    extra           = 0
    readonly_fields = ('image', 'uploaded_at', 'status', 'analysis_result')
    can_delete      = False


class ChatMessageInline(admin.TabularInline):
    model           = ChatMessage
    extra           = 0
    readonly_fields = ('role', 'content', 'timestamp')
    can_delete      = False
    ordering        = ('timestamp',)


# ---------------------------------------------------------------------------
# Extended User Admin — everything nested under the User
# ---------------------------------------------------------------------------

class UserAdmin(BaseUserAdmin):
    inlines = (
        UserProfileInline,
        DailyLogInline,
        FoodImageInline,
        ChatMessageInline,
    )
    list_display  = ('username', 'date_joined', 'last_login', 'is_active', 'get_goal', 'get_streak')
    list_filter   = ('is_active', 'is_staff', 'profile__goal', 'profile__diet_type')
    search_fields = ('username', 'profile__full_name')

    def get_goal(self, obj):
        try:
            return obj.profile.get_goal_display()
        except UserProfile.DoesNotExist:
            return '—'
    get_goal.short_description = 'Goal'

    def get_streak(self, obj):
        try:
            return f"{obj.profile.streak_days} days"
        except UserProfile.DoesNotExist:
            return '—'
    get_streak.short_description = 'Streak'


# Re-register User with extended admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# ---------------------------------------------------------------------------
# DailyLog Admin — with meals nested inside
# ---------------------------------------------------------------------------

@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    inlines       = (MealEntryInline,)
    list_display  = ('user', 'date', 'cal_total', 'cal_target', 'protein_total', 'carbs_total', 'fats_total', 'fiber_total')
    list_filter   = ('date',)
    search_fields = ('user__username',)
    readonly_fields = (
        'user', 'date',
        'cal_target', 'protein_target', 'carbs_target', 'fats_target', 'fiber_target',
        'cal_total',  'protein_total',  'carbs_total',  'fats_total',  'fiber_total',
    )
    ordering      = ('-date',)


# ---------------------------------------------------------------------------
# FoodImage Admin
# ---------------------------------------------------------------------------

@admin.register(FoodImage)
class FoodImageAdmin(admin.ModelAdmin):
    list_display  = ('user', 'uploaded_at', 'status')
    list_filter   = ('status',)
    search_fields = ('user__username',)
    readonly_fields = ('user', 'image', 'uploaded_at', 'status', 'analysis_result')
    ordering      = ('-uploaded_at',)


# ---------------------------------------------------------------------------
# ChatMessage Admin — full conversation view per user
# ---------------------------------------------------------------------------

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display  = ('user', 'role', 'short_content', 'timestamp')
    list_filter   = ('role',)
    search_fields = ('user__username', 'content')
    readonly_fields = ('user', 'role', 'content', 'timestamp')
    ordering      = ('user', 'timestamp')

    def short_content(self, obj):
        return obj.content[:80] + '...' if len(obj.content) > 80 else obj.content
    short_content.short_description = 'Message'
