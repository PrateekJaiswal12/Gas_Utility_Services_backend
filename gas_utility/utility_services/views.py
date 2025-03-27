from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import ServiceRequest
from accounts.models import CustomUser
from django.utils import timezone

# Admin API endpoints
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_list_requests(request):
    requests = ServiceRequest.objects.all()
    data = [{
        'id': req.id,
        'customer': {
            'id': req.customer.id,
            'username': req.customer.username,
            'name': req.customer.name,
            'customer_id': req.customer.customer_id
        },
        'type_of_request': req.type_of_request,
        'details': req.details,
        'status': req.status,
        'date_submitted': req.date_submitted,
        'date_resolved': req.date_resolved
    } for req in requests]
    return Response(data)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def admin_request_detail(request, request_id):
    try:
        service_request = ServiceRequest.objects.get(id=request_id)
    except ServiceRequest.DoesNotExist:
        return Response({'error': 'Service request not found'}, status=404)

    if request.method == 'GET':
        data = {
            'id': service_request.id,
            'customer': {
                'id': service_request.customer.id,
                'username': service_request.customer.username,
                'name': service_request.customer.name,
                'customer_id': service_request.customer.customer_id
            },
            'type_of_request': service_request.type_of_request,
            'details': service_request.details,
            'status': service_request.status,
            'date_submitted': service_request.date_submitted,
            'date_resolved': service_request.date_resolved
        }
        return Response(data)

    elif request.method == 'PUT':
        data = request.data
        service_request.type_of_request = data.get('type_of_request', service_request.type_of_request)
        service_request.details = data.get('details', service_request.details)
        service_request.status = data.get('status', service_request.status)
        
        if data.get('status') == 'Completed' and not service_request.date_resolved:
            service_request.date_resolved = timezone.now()
        
        service_request.save()
        return Response({'message': 'Service request updated successfully'})

    elif request.method == 'DELETE':
        service_request.delete()
        return Response({'message': 'Service request deleted successfully'})

# Regular user endpoints
@ensure_csrf_cookie
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_request(request):
    if request.method == 'POST':
        try:
            service_request = ServiceRequest.objects.create(
                customer=request.user,
                type_of_request=request.data.get('type_of_request'),
                details=request.data.get('details'),
                status='Pending'
            )
            
            return Response({
                'message': 'Service request submitted successfully',
                'request': {
                    'id': service_request.id,
                    'type_of_request': service_request.type_of_request,
                    'status': service_request.status,
                    'date_submitted': service_request.date_submitted,
                    'details': service_request.details
                }
            }, status=201)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=400)
    
    return Response({'message': 'Method not allowed'}, status=405)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def track_requests(request):
    user = request.user
    user_requests = ServiceRequest.objects.filter(customer=user)
    data = [{
        'id': req.id,
        'type_of_request': req.type_of_request,
        'status': req.status,
        'date_submitted': req.date_submitted,
        'details': req.details
    } for req in user_requests]
    return Response(data)
