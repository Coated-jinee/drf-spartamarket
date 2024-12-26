from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email: # 이메일이 없는 경우의 예외처리임 
            raise ValueError("이메일은 필수입니다")
        
        email = self.normalize_email(email) # 공백 제거, 소문자로 변환
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    # 관리자 계정 생성에 대한 메서드
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    


# Create your models here.
class User(AbstractUser):
    email = models.EmailField('이메일', unique=True)
    # username = None # 안쓰고 싶은 경우
    username = models.CharField('닉네임', max_length=150)
    profile_image = models.ImageField('프로필 이미지', upload_to ='profile_images/', blank=True, null=True)

    USERNAME_FIELD = 'email' # 로그인 시 필요한 필드
    REQUIRED_FIELDS = [] # 필수 필드 정의 (email필드 자동으로 필수가 됨)

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
