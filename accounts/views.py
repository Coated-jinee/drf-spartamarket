from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import SignupSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        return Response({
            "message": "회원가입이 성공적으로 완료되었습니다."
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)


# 로그인 view 함수
@api_view(['POST'])
@authentication_classes([])      # 전역 인증 설정 무시
@permission_classes([AllowAny])  # 전역 IsAuthenticated 설정 무시
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # 사용자 인증
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # JWT 토큰 생성
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'message': '로그인 성공'
            }, status=200)
        else:
            return JsonResponse({'error': '이메일 또는 비밀번호가 올바르지 않습니다.'}, status=400)

@api_view(['POST'])
@authentication_classes([])      # 전역 인증 설정 무시
@permission_classes([AllowAny])  # 전역 IsAuthenticated 설정 무시
def logout(request):
    print('---')
    try:
        refresh_token = request.data.get("refresh")
        print(refresh_token)
        token = RefreshToken(refresh_token)
        print(token)
        token.blacklist()
        print('---')
        return Response({"message": "로그아웃 성공"})
    except Exception:
        return Response({"error": "로그아웃 실패"}, 
                      status=status.HTTP_400_BAD_REQUEST)
        