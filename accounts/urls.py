from django.urls import path
from .views import (  # ✅ Correct: import from the same app
    register_view,
    login_view,
    logout_view,
    forgot_password,
    change_password,
    change_password,
    
   
)
urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    # path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    # path('password_reset_done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('change_password/<int:user_id>/',change_password, name='change_password'),
    

]
