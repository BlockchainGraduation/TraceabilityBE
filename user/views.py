from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.views import APIView
from .serializers import (
    RegisterSerializer,
    RegisterRuleSerializer,
    ResponseUserSerializer,
    UpdateUserSerializer,
    MyTokenObtainPairSerializer,
    ConfirmOTPSerializer,
    ResetPasswordSerializer,
    ForgetSerializer,
    LogoutSerializer,
    ConfirmUserSerializer,
)
import stripe
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import User, PENDDING, NONE, MEMBER, FACTORY, DISTRIBUTER, RETAILER
from product.models import Product
from transaction.models import Transaction, REJECT, ACCEPT, DONE
from product.serializers import ProductSerializers, SimpleProductSerializers
from django_filters.rest_framework import DjangoFilterBackend
from .utils import generate_otp, send_otp_email
from eth_account import Account
from utils.blockchain.actor_provider import ActorProvider


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class StatisticalView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["user"],
        operation_summary="User Statistical",
    )
    def get(self, request):
        product_count = Product.objects.filter(create_by=request.user).count()
        public_product_count = Product.objects.filter(
            create_by=request.user, active=True
        ).count()
        private_product_count = Product.objects.filter(
            create_by=request.user, active=False
        ).count()

        # Transaction Buy
        transaction_count = Transaction.objects.filter(create_by=request.user).count()
        pendding_transaction_count = Transaction.objects.filter(
            create_by=request.user, status=PENDDING
        ).count()
        accept_transaction_count = Transaction.objects.filter(
            create_by=request.user, status=ACCEPT
        ).count()
        reject_transaction_count = Transaction.objects.filter(
            create_by=request.user, status=REJECT
        ).count()
        done_transaction_count = Transaction.objects.filter(
            create_by=request.user, status=DONE
        ).count()
        # Transaction sales
        transaction_sales_count = Transaction.objects.filter(
            product_id__create_by=request.user
        ).count()
        pendding_transaction_sales_count = Transaction.objects.filter(
            product_id__create_by=request.user, status=PENDDING
        ).count()
        accept_transaction_sales_count = Transaction.objects.filter(
            product_id__create_by=request.user, status=ACCEPT
        ).count()
        reject_transaction_sales_count = Transaction.objects.filter(
            product_id__create_by=request.user, status=REJECT
        ).count()
        done_transaction_sales_count = Transaction.objects.filter(
            product_id__create_by=request.user, status=DONE
        ).count()

        # Transaction mounh
        month_transaction = {}
        month_product = {}

        for i in range(1, 13):
            # print(type(str(i)))
            month_transaction[i] = Transaction.objects.filter(
                product_id__create_by=request.user, create_at__month=i
            ).count()
        for i in range(1, 13):
            month_product[i] = Product.objects.filter(
                create_by=request.user, create_at__month=i
            ).count()
        # result_json = json.dumps({"month": result_dict})
        return Response(
            {
                "detail": {
                    "product": {
                        "product_count": product_count,
                        "public_product_count": public_product_count,
                        "private_product_count": private_product_count,
                    },
                    "transaction": {
                        "transaction_count": transaction_count,
                        "pendding_transaction_count": pendding_transaction_count,
                        "accept_transaction_count": accept_transaction_count,
                        "reject_transaction_count": reject_transaction_count,
                        "done_transaction_count": done_transaction_count,
                    },
                    "sales": {
                        "transaction_sales_count": transaction_sales_count,
                        "accept_transaction_sales_count": accept_transaction_sales_count,
                        "pendding_transaction_sales_count": pendding_transaction_sales_count,
                        "reject_transaction_sales_count": reject_transaction_sales_count,
                        "done_transaction_sales_count": done_transaction_sales_count,
                    },
                    "month_transaction": month_transaction,
                    "month_product": month_product,
                }
            },
            status=status.HTTP_200_OK,
        )


class TotalUserView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=["user"],
        operation_summary="Total User Statistical",
    )
    def get(self, request):
        user_total = User.objects.filter(is_superuser=False).count()
        anonymous_user_total = User.objects.filter(confirm_status=NONE).count()
        factory_user_total = User.objects.filter(role=FACTORY).count()
        distributer_user_total = User.objects.filter(role=DISTRIBUTER).count()
        retailer_user_total = User.objects.filter(role=RETAILER).count()
        return Response(
            {
                "detail": {
                    "user": {
                        "user_total": user_total,
                        "anonymous_user_total": anonymous_user_total,
                        "factory_user_total": factory_user_total,
                        "distributer_user_total": distributer_user_total,
                        "retailer_user_total": retailer_user_total,
                    }
                }
            },
            status=status.HTTP_200_OK,
        )


class AdminStatisticalView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        tags=["user"],
        operation_summary="Admin Statistical",
    )
    def get(self, request):
        user_total = User.objects.filter(is_superuser=False).count()
        anonymous_user_total = User.objects.filter(confirm_status=NONE).count()
        factory_user_total = User.objects.filter(role=FACTORY).count()
        distributer_user_total = User.objects.filter(role=DISTRIBUTER).count()
        retailer_user_total = User.objects.filter(role=RETAILER).count()

        # prouduct
        product_total = Product.objects.all().count()
        factory_product_total = Product.objects.filter(product_type=FACTORY).count()
        distributer_product_total = Product.objects.filter(
            product_type=DISTRIBUTER
        ).count()
        retailer_product_total = Product.objects.filter(product_type=RETAILER).count()

        month_user = {}
        month_product = {}

        for i in range(1, 13):
            month_user[i] = User.objects.filter(
                date_joined__month=i, is_superuser=False
            ).count()
        for i in range(1, 13):
            month_product[i] = Product.objects.filter(create_at__month=i).count()
        # for i in range(1, 13):
        #     month_product[i] = Product.objects.filter(
        #         create_by=request.user, create_at__month=i
        #     ).count()
        return Response(
            {
                "detail": {
                    "user": {
                        "user_total": user_total,
                        "anonymous_user_total": anonymous_user_total,
                        "factory_user_total": factory_user_total,
                        "distributer_user_total": distributer_user_total,
                        "retailer_user_total": retailer_user_total,
                        "month_user": month_user,
                    },
                    "product": {
                        "product_total": product_total,
                        "factory_product_total": factory_product_total,
                        "distributer_product_total": distributer_product_total,
                        "retailer_product_total": retailer_product_total,
                        "month_product": month_product,
                    },
                }
            },
            status=status.HTTP_200_OK,
        )


class ConfirmOTP(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=ConfirmOTPSerializer,
        tags=["auth"],
        operation_summary="User ConfirmOTP",
    )
    def post(self, request):
        serializer = ConfirmOTPSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if serializer.data["password"] == serializer.data["re_password"]:
                user = User.objects.filter(
                    email=serializer.data["email"], otp=serializer.data["otp"]
                ).first()

                if user:
                    user.set_password(serializer.data["password"])
                    user.is_active = True
                    account = Account.create()
                    user.wallet_address = account.address
                    user.wallet_private_key = account.key.hex()

                    user.save()

                    return Response(
                        {
                            "user": ResponseUserSerializer(user).data,
                            "token": get_tokens_for_user(user),
                        },
                        status=status.HTTP_201_CREATED,
                    )
                # serializer.save()
                return Response(
                    {"detail": "WRONG_OTP"}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class ForgetView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=ForgetSerializer,
        tags=["auth"],
        operation_summary="User Forget Password",
    )
    def post(self, request):
        serializer = ForgetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.filter(email=serializer.data["email"]).first()
            if user:
                otp = generate_otp()
                user.otp = otp
                user.save()
                send_otp_email(user.email, otp)
                return Response(
                    {"detail": "SEND_EMAIL_SUCCESS"}, status=status.HTTP_202_ACCEPTED
                )
            else:
                return Response(
                    {"detail": "ACCOUNT_NOT_EXISTS"}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response({"detail": "DATA_INVALID"}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=ResetPasswordSerializer,
        tags=["auth"],
        operation_summary="User Reset Password",
    )
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print(serializer.data)
            if serializer.data["new_password"] != serializer.data["re_new_password"]:
                return Response(
                    {"detail": "DATA_INVALID"}, status=status.HTTP_400_BAD_REQUEST
                )
            user = User.objects.filter(email=request.user.email).first()
            if user.check_password(serializer.data["old_password"]):
                user.set_password(serializer.data["new_password"])
                user.save()
                return Response(
                    {"detail": "RESET_PASSWORD_SUCCESS"},
                    status=status.HTTP_202_ACCEPTED,
                )
            else:
                return Response(
                    {"detail": "PASSWORD_INVALID"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response({"detail": "DATA_INVALID"}, status=status.HTTP_400_BAD_REQUEST)


class RegisterRuleView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=RegisterRuleSerializer,
        tags=["user"],
        operation_summary="User Register Rule",
    )
    def post(self, request):
        serializer = RegisterRuleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(id=request.user.pk)
            user.confirm_status = PENDDING
            user.survey = serializer.data["survey"]
            user.save()
            return Response(
                {"detail": "REGISTER_RULE_SUCCESS"}, status=status.HTTP_201_CREATED
            )
        return Response({"detail": serializer.errors})


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        tags=["auth"],
        operation_summary="User Register",
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        print("OK")
        user = User.objects.filter(email=request.data["email"]).first()
        if user:
            if user.is_active is False:
                otp = generate_otp()
                send_otp_email(request.data["email"], otp)
                user.username = request.data["username"]
                user.otp = otp
                user.save()
                return Response(
                    {"detail": "ACCOUNT_CREATED"}, status=status.HTTP_201_CREATED
                )
            return Response(
                {"detail": "ACCOUNT_EXISTS"}, status=status.HTTP_400_BAD_REQUEST
            )

        else:
            if serializer.is_valid(raise_exception=True):
                otp = generate_otp()
                send_otp_email(serializer.data["email"], otp)
                User.objects.create(
                    **serializer.data, fullname=serializer.data["username"], otp=otp
                )
                # serializer.save()
                return Response(
                    {"detail": serializer.data}, status=status.HTTP_201_CREATED
                )
        return Response({"detail": serializer.errors})


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=["auth"], operation_summary="User Login")
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # access = response.data['access']
        # print(request.data["username"])
        user = User.objects.filter(
            username=request.data["username"], is_delete=False, is_active=True
        ).first()
        if user is None:
            response.data = {"BLACK_USER"}
            response.status_code = status.HTTP_423_LOCKED
            return response
        response.data = {
            "access": response.data["access"],
            "refresh": response.data["refresh"],
            "user": ResponseUserSerializer(user).data,
        }
        response.set_cookie("access", response.data["access"], httponly=False)
        response.set_cookie("refresh", response.data["refresh"], httponly=False)
        return response


class GetMeView(APIView):
    serializer_class = ResponseUserSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["user"], operation_summary="User Me")
    def get(self, request, *args, **kwargs):
        # response = super().post(request, *args, **kwargs)
        if request.user.is_delete:
            return Response(
                {"detail": "ACCOUNT_DELETED"},
                status=status.HTTP_423_LOCKED,
            )
        # user = User.objects.filter(username=request.data["username"]).first()
        return Response(
            {"user": ResponseUserSerializer(request.user).data},
            status=status.HTTP_202_ACCEPTED,
        )


class MyTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(tags=["auth"], operation_summary="User Refresh")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["auth"], request_body=LogoutSerializer, operation_summary="User Logout"
    )
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Blacklist the refresh token
                response = Response()
                response.data = {"detail": "Successfully logged out."}
                response.status_code = status.HTTP_200_OK
                response.delete_cookie("access")
                response.delete_cookie("refresh")
                return response
            except Exception as e:
                return Response(
                    {"detail": "Invalid refresh token."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"detail": "Refresh token not provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # serializer = RegisterSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()

        user = User.objects.get(id=request.user.pk)
        serializer = ResponseUserSerializer(user)
        content = {
            "user": str(request.user.pk),  # `django.contrib.auth.User` instance.
            "auth": str(request.auth),  # None
        }
        return Response(serializer.data)


class UpdateUserView(generics.RetrieveUpdateAPIView):
    # queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateUserSerializer

    @swagger_auto_schema(auto_schema=None)
    def put(self, request, *args, **kwargs):
        return

    @swagger_auto_schema(auto_schema=None)
    def get(self, request, *args, **kwargs):
        return

    def partial_update(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response({serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class GetUserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        # print(kwargs["pk"])
        user = User.objects.filter(pk=kwargs["pk"], is_delete=False).first()
        if user:
            product = Product.objects.filter(create_by=kwargs["pk"])
            return Response(
                {
                    "user": ResponseUserSerializer(user).data,
                    "products": SimpleProductSerializers(product, many=True).data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"detail": "USER_NOT_FOUND"}, status=status.HTTP_400_BAD_REQUEST
        )


class GetListUserView(generics.ListAPIView):
    queryset = User.objects.filter(is_delete=False, is_superuser=False)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["confirm_status", "id"]
    permission_classes = [IsAdminUser]
    serializer_class = ResponseUserSerializer

    @swagger_auto_schema(
        tags=["auth"],
        operation_summary="Get list user",
        manual_parameters=[
            openapi.Parameter(
                "confirm_status",
                in_=openapi.IN_QUERY,
                description="Lọc theo status",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "id",
                in_=openapi.IN_QUERY,
                description="Lọc theo create_by",
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    # def partial_update(self, request, *args, **kwargs):
    #     return super().partial_update(request, *args, **kwargs)


class ConfirmUserView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        request_body=ConfirmUserSerializer,
        tags=["auth"],
        operation_summary="Confirm user by admin",
    )
    def patch(self, request, *args, **kwargs):
        # try:
        serializes = ConfirmUserSerializer(data=request.data)
        serializes.is_valid(raise_exception=True)
        user = User.objects.filter(pk=serializes.data["user_id"]).first()
        if user:
            if serializes.data["status"] is True:
                user.confirm_status = DONE
                user.fullname = user.survey["name"]
                user.phone = user.survey["phone"] or None
                user.role = user.survey["user_role"]
                map_role = {"FACTORY": 1, "DISTRIBUTER": 2, "RETAILER": 3}
                tx_hash = ActorProvider().create_actor(
                    str(user.id),
                    address=user.wallet_address,
                    role=map_role[user.role],
                    hash_info="",
                )
                user.tx_hash = tx_hash
                user.save()
                return Response({"detail": "SUCCESS"}, status=status.HTTP_200_OK)
            else:
                user.confirm_status = NONE
                user.save()
                return Response({"detail": "SUCCESS"}, status=status.HTTP_200_OK)
        return Response(
            {"detail": "USER_NOT_EXISTS"}, status=status.HTTP_400_BAD_REQUEST
        )
        # except Exception as e:
        #     print(e)
        #     return Response(
        #         {"detail": "DATA_INVALID"}, status=status.HTTP_400_BAD_REQUEST
        #     )


class BlackUserView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        request_body=ConfirmUserSerializer,
        tags=["auth"],
        operation_summary="Block user by admin",
    )
    def patch(self, request, *args, **kwargs):
        serializes = ConfirmUserSerializer(data=request.data)
        serializes.is_valid(raise_exception=True)
        user = User.objects.filter(pk=serializes.data["user_id"]).first()
        if user:
            if serializes.data["status"] is True:
                user.is_active = True
                user.save()
                return Response({"detail": "SUCCESS"}, status=status.HTTP_200_OK)
            else:
                user.is_active = False
                user.save()
                return Response({"detail": "SUCCESS"}, status=status.HTTP_200_OK)
        return Response({"detail": "USER_NOT_EXISTS"}, status=status.HTTP_200_OK)


# Checkout
class create_checkout(APIView):
    @swagger_auto_schema(
        tags=["Payment"],
        operation_summary="Payment",
    )
    def post(self, request):
        YOUR_DOMAIN = "http://localhost:8000/"
        token = request.COOKIES["access"]
        stripe.api_key = "sk_test_51NpMKLFobSqgGAG31Vf7UDMarMp5Gg0a8umlS4xMZcKiTbGgmRXPhzQlKs5R5xHDA5FtalNIXs3fS4oWUKGRQBap00bWsM3LBr"

        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        "price": "price_1OHr16FobSqgGAG3srNqsz0V",
                        "quantity": 1,
                    },
                ],
                mode="payment",
                success_url=YOUR_DOMAIN
                + "api/user/done-checkout?session_id={CHECKOUT_SESSION_ID}&token="
                + token,
                cancel_url=YOUR_DOMAIN + "/cancel.html",
            )
        except Exception as e:
            raise AuthenticationFailed("Errr")

        return redirect(checkout_session.url, code=303)


class payment_successful(APIView):
    def get(self, request):
        checkout_session_id = request.GET.get("session_id", None)
        token = request.GET.get("token", None)
        valid_data = AccessToken(token)

        data = stripe.checkout.Session.retrieve(
            checkout_session_id,
        )
        user = User.objects.get(id=valid_data["user_id"])
        user.account_balance = user.account_balance + data.amount_total
        user.save()

        return redirect("http://localhost:3000/", code=200)
