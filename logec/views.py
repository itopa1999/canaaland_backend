from django.urls import reverse
from rest_framework import status, generics
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
import requests as req
from rest_framework.permissions import IsAuthenticated
import secrets 
from django.conf import settings
from .serializers import  *
from .services import BRANCHES, DEPARTMENTS
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes
from django.core.mail import send_mail
# Create your views here.

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'

class LOGECCreateQuestionView(generics.GenericAPIView):
    serializer_class = LOGECCreateQuestionSerializer
    @swagger_auto_schema(tags=['LOGEC'])
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'message': 'Question submitted successfully!, you will be contacted.',
        }, status=status.HTTP_201_CREATED)
    

class LOGECListQuestionView(generics.ListAPIView):
    permission_classes =[IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    queryset = LOGECQuestion.objects.all()
    serializer_class = LOGECListQuestionSerializer

    @swagger_auto_schema(tags=['LOGEC'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        
        if search_query:
            queryset = queryset.filter(
                Q(email__icontains=search_query) |
                Q(name__icontains=search_query)
            )
        return queryset


class LOGECGetQuestionView(generics.RetrieveAPIView):
    permission_classes =[IsAuthenticated]
    queryset = LOGECQuestion.objects.all()
    serializer_class = LOGECCreateQuestionSerializer

    @swagger_auto_schema(tags=['LOGEC'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class LOGECRegisterMemberView(generics.GenericAPIView):
    permission_classes =[IsAuthenticated]
    serializer_class = LOGECRegisterMemberSerializer
    @swagger_auto_schema(tags=['LOGEC'])
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response({
            'message': f'Hi {instance.name}, your registration was successful',
        }, status=status.HTTP_201_CREATED)



class LOGECListMemberView(generics.ListAPIView):
    permission_classes =[IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    queryset = LOGECMember.objects.all()
    serializer_class = LOGECListMemberSerializer

    @swagger_auto_schema(tags=['LOGEC'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        department_query = self.request.query_params.get('department', None)
        branch_query = self.request.query_params.get('branch', None)
        
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(address__icontains=search_query) |
                Q(phone__icontains=search_query) | 
                Q(gender__icontains=search_query) 
            )
        if branch_query:
            queryset = queryset.filter(branch__icontains=branch_query)
        if department_query:
            queryset = queryset.filter(department__icontains=department_query)
        
        return queryset


class LOGECMemberDetailsView(generics.RetrieveAPIView):
    permission_classes =[IsAuthenticated]
    queryset = LOGECMember.objects.all()
    serializer_class = LOGECRegisterMemberSerializer

    @swagger_auto_schema(tags=['LOGEC'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    

class LOGECUpdateMemberView(generics.UpdateAPIView):
    permission_classes =[IsAuthenticated]
    queryset = LOGECMember.objects.all()
    serializer_class = LOGECRegisterMemberSerializer
    @swagger_auto_schema(tags=['LOGEC'])
    def put(self, request, *args, **kwargs):
        print(request)
        return super().update(request, *args, **kwargs)
    

class LOGECSermonCommentView(generics.GenericAPIView):
    serializer_class = LOGECSermonCommentSerializer
    @swagger_auto_schema(tags=['LOGEC'])
    def post(self, request,sermon_id):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try: 
            sermon = LOGECSermon.objects.get(id=sermon_id) 
        except LOGECSermon.DoesNotExist: 
            return Response({'error': 'Sermon not found'},status=status.HTTP_400_BAD_REQUEST)
        email = serializer.validated_data.get('email')
        name = serializer.validated_data.get('name')

        if LOGECSermonComment.objects.filter(Q(email=email) | Q(name=name), sermon = sermon).exists():
            return Response({'error': 'you have already commented.'},status=status.HTTP_400_BAD_REQUEST)

        serializer.save(sermon=sermon)
        return Response({
            'message': 'Thanks for the comment',
        }, status=status.HTTP_201_CREATED)


class LOGECDeleteCommentView(generics.DestroyAPIView):
    permission_classes =[IsAuthenticated]
    queryset = LOGECSermonComment.objects.all()
    @swagger_auto_schema(tags=['LOGEC'])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    

class LOGECSermonView(generics.GenericAPIView):
    serializer_class = LOGECSermonSerializer
    @swagger_auto_schema(tags=['LOGEC'])
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response({
            'message': 'Sermon added successfully.',
        }, status=status.HTTP_201_CREATED)
    

class LOGECDepartmentBranchListView(APIView):
    @swagger_auto_schema(tags=['LOGEC'])
    def get(self, request, *args, **kwargs):
        data = {
            "branches": BRANCHES,
            "departments": DEPARTMENTS
        }
        return Response(data, status=status.HTTP_200_OK)




class LOGECIndexView(APIView):
    @swagger_auto_schema(tags=['LOGEC'])
    def get(self, request):
        sermons = LOGECSermon.objects.all()[:3]
        sermons_serializer = LOGECSermonSerializer(sermons, many=True)
        return Response({"sermons":sermons_serializer.data})
    


class LOGECListSermonView(generics.ListAPIView):
    queryset = LOGECSermon.objects.all()
    serializer_class = LOGECListSermonSerializer

    @swagger_auto_schema(tags=['LOGEC'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(preacher__icontains=search_query)
            )
        
        return queryset



class LOGECSermonDetailView(generics.RetrieveAPIView):
    queryset = LOGECSermon.objects.all()
    serializer_class = LOGECSermonSerializer
    lookup_field = 'id'

    @swagger_auto_schema(tags=['LOGEC'])
    def get(self, request, *args, **kwargs):
        sermon = self.get_object()
        preacher_name = sermon.preacher
        comments = LOGECSermonComment.objects.filter(sermon__id=sermon.id)
        title = request.GET.get('search', None)
        if title:
            recent_sermons = LOGECSermon.objects.filter(preacher=preacher_name,title__icontains = title) \
                                             .exclude(id=sermon.id) \
                                             .order_by('-posted_at')[:5]
        else:
            recent_sermons = LOGECSermon.objects.filter(preacher=preacher_name) \
                                             .exclude(id=sermon.id) \
                                             .order_by('-posted_at')[:5]
        sermon_data = self.get_serializer(sermon).data
        comments = LOGECSermonCommentSerializer(comments, many=True).data
        recent_sermons_data = LOGECListSermonSerializer(recent_sermons, many=True).data
        return Response({
            'sermon': sermon_data,
            'recent_sermons': recent_sermons_data,
            "comments":comments
        })
    


class LOGECDeleteSermonView(generics.DestroyAPIView):
    permission_classes =[IsAuthenticated]
    queryset = LOGECSermon.objects.all()
    @swagger_auto_schema(tags=['LOGEC'])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    

class LOGECUpdateSermonView(generics.UpdateAPIView):
    permission_classes =[IsAuthenticated]
    queryset = LOGECSermon.objects.all()
    serializer_class = LOGECSermonSerializer
    @swagger_auto_schema(tags=['LOGEC'])
    def put(self, request, *args, **kwargs):
        print(request)
        return super().update(request, *args, **kwargs)



class LOGECListDonationView(generics.ListAPIView):
    permission_classes =[IsAuthenticated]
    queryset = LOGECDonation.objects.all()
    serializer_class = LOGECListDonationSerializer
    pagination_class = CustomPageNumberPagination

    @swagger_auto_schema(tags=['LOGEC'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(name__icontains=search_query) |
                Q(amount__icontains=search_query) 
            )
        
        return queryset
    

class LOGECDonationDetailsView(generics.RetrieveAPIView):
    permission_classes =[IsAuthenticated]
    queryset = LOGECDonation.objects.all()
    serializer_class = LOGECDonationSerializer

    @swagger_auto_schema(tags=['LOGEC'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)



class LOGECRegisterNewMemberView(generics.GenericAPIView):
    permission_classes =[IsAuthenticated]
    serializer_class = LOGECNewMemberSerializer
    @swagger_auto_schema(tags=['LOGEC'])
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response({
            'message': f'Hi {instance.name}, your registration was successful',
        }, status=status.HTTP_201_CREATED)
    


class LOGECListNewMemberView(generics.ListAPIView):
    permission_classes =[IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    queryset = LOGECNewMember.objects.all()
    serializer_class = LOGECListNewMemberSerializer

    @swagger_auto_schema(tags=['LOGEC'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        branch_query = self.request.query_params.get('branch', None)
        
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(address__icontains=search_query) |
                Q(phone__icontains=search_query)            )
        if branch_query:
            queryset = queryset.filter(branch__icontains=branch_query)

        return queryset



class LOGECNewMemberDetailsView(generics.RetrieveAPIView):
    permission_classes =[IsAuthenticated]
    queryset = LOGECNewMember.objects.all()
    serializer_class = LOGECNewMemberSerializer

    @swagger_auto_schema(tags=['LOGEC'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)



class LOGECPaystackCashDepositView(generics.GenericAPIView):
    serializer_class = DepositSerializer
    @swagger_auto_schema(tags=['LOGEC'])
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        title = serializer.validated_data.get('title')
        name = serializer.validated_data.get('name')
        amount = serializer.validated_data["amount"]
        percentage = 1.5 / 100
        additionalAmount = 100
        modifiedAmount = (amount * percentage) + amount + additionalAmount
        amount = int(modifiedAmount) * 100
        ref = secrets.token_urlsafe(15)
        if serializer.is_valid():
            url="https://api.paystack.co/transaction/initialize"
            headers = {
                    'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
                    'Content-Type': 'application/json',
                }
            redirect_url = request.build_absolute_uri(reverse('paystack-confirm-deposit', kwargs={"reference":ref}))
            data = { 
            "email": "LOGEC@gmail.com", 
            "amount": amount,
            "reference":ref,
            "metadata":{
                "name" : name,
                "title":title
            },
            "callback_url": redirect_url
            }
            print(data)
            response = req.post(url, headers=headers, json=data)
            if response.status_code == 200:
                response_data = response.json()
                return Response(
                    {
                        "link": response_data["data"]["authorization_url"],
                    },
                    status=response.status_code,
                )
            else:
                return Response({"details":response.json()}, status=response.status_code)
        else:
                return Response({"details":"Invalid Amount"}, status=response.status_code)




class LOGECPaystackConfirmDepositView(APIView):
    @swagger_auto_schema(tags=['LOGEC'])
    def get(self, request,reference, *args, **kwargs):
        if not reference:
            return Response({"error": "Transaction reference required."}, status=status.HTTP_400_BAD_REQUEST)
        
        verification_url = f"https://api.paystack.co/transaction/verify/{reference}"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        }
        response = req.get(verification_url, headers=headers)
        verification_data = response.json()
        if verification_data['status'] == True and verification_data['data']['status'] == 'success':
            amount = int(verification_data['data']['amount'])/100
            title = verification_data['data']['metadata']['title']
            name = verification_data['data']['metadata']['name']
            ref = reference

            try:
                offering = LOGECDonation.objects.create(
                    amount = amount,
                    title = title,
                    name = name,
                    ref = ref
                )
                return Response(status=status.HTTP_204_NO_CONTENT)
            except:
                return Response({"error": "Payment successful, but can not complete request."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Transaction verification failed."}, status=status.HTTP_400_BAD_REQUEST)


