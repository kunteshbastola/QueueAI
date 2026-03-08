from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import status
from django.utils.timezone import now
from django.db.models import Count
from .models import Token, Service
from .serializers import TokenSerializer, ServiceSerializer

# token generation view
@api_view(['POST'])
def generate_token(request):

    user = request.user
    service_id = request.data.get("service")

    try:
        service = Service.objects.get(pk=service_id)
    except Service.DoesNotExist:
        return Response({"error": "Service not found"}, status=404)

    # Count tokens for this service today
    today_tokens = Token.objects.filter(
        service=service,
        created_at__date=now().date()
    ).count()

    # Generate token number
    token_number = f"{service.Service_name[:1].upper()}{today_tokens + 1}"

    # Predicted wait time
    predicted_wait = today_tokens * service.avg_service_time // 60

    token = Token.objects.create(
        user=user,
        service=service,
        token_number=token_number,
        predicted_wait_time=predicted_wait
    )

    serializer = TokenSerializer(token)

    return Response({
        "message": "Token generated successfully",
        "token": serializer.data
    }, status=status.HTTP_201_CREATED)



# Get all services
@api_view(['GET'])
def service_list(request):
    services = Service.objects.filter(is_active=True)
    serializer = ServiceSerializer(services, many=True)
    return Response(serializer.data)


# Get single service
@api_view(['GET'])
def service_detail(request, pk):
    try:
        service = Service.objects.get(pk=pk)
    except Service.DoesNotExist:
        return Response({"error": "Service not found"}, status=404)

    serializer = ServiceSerializer(service)
    return Response(serializer.data)


# Create service
@api_view(['POST'])
def service_create(request):
    serializer = ServiceSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Update service
@api_view(['PUT'])
def service_update(request, pk):
    try:
        service = Service.objects.get(pk=pk)
    except Service.DoesNotExist:
        return Response({"error": "Service not found"}, status=404)

    serializer = ServiceSerializer(service, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete service
@api_view(['DELETE'])
def service_delete(request, pk):
    try:
        service = Service.objects.get(pk=pk)
    except Service.DoesNotExist:
        return Response({"error": "Service not found"}, status=404)

    service.delete()
    return Response({"message": "Service deleted"})


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Counter
from .serializers import CounterSerializer


# Get all counters
@api_view(['GET'])
def counter_list(request):
    counters = Counter.objects.filter(is_active=True)
    serializer = CounterSerializer(counters, many=True)
    return Response(serializer.data)


# Get single counter
@api_view(['GET'])
def counter_detail(request, pk):
    try:
        counter = Counter.objects.get(pk=pk)
    except Counter.DoesNotExist:
        return Response({"error": "Counter not found"}, status=404)

    serializer = CounterSerializer(counter)
    return Response(serializer.data)


# Create counter
@api_view(['POST'])
def counter_create(request):
    serializer = CounterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Update counter
@api_view(['PUT'])
def counter_update(request, pk):
    try:
        counter = Counter.objects.get(pk=pk)
    except Counter.DoesNotExist:
        return Response({"error": "Counter not found"}, status=404)

    serializer = CounterSerializer(counter, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete counter
@api_view(['DELETE'])
def counter_delete(request, pk):
    try:
        counter = Counter.objects.get(pk=pk)
    except Counter.DoesNotExist:
        return Response({"error": "Counter not found"}, status=404)

    counter.delete()
    return Response({"message": "Counter deleted"})