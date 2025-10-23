from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from decimal import Decimal
from .models import Booking
from .serializers import BookingSerializer

class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        # Calculate platform fee (e.g., 10% of total amount)
        total_amount = serializer.validated_data.get('total_amount', Decimal('0'))
        platform_fee = total_amount * Decimal('0.10')  # 10% platform fee
        
        serializer.save(
            customer=self.request.user,
            platform_fee=platform_fee
        )

class BookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(customer=self.request.user).order_by('-created_at')

@api_view(['POST'])
def confirm_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, customer=request.user)
        booking.status = 'confirmed'
        booking.save()
        
        # Send notification to provider
        from notifications.utils import send_notification
        send_notification(
            booking.provider.user,
            'Booking Confirmed',
            f'Your booking for {booking.service.name} has been confirmed.'
        )
        
        return Response({'message': 'Booking confirmed successfully'})
    
    except Booking.DoesNotExist:
        return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_booking(request, booking_id):
    """
    Delete a booking. Only the customer who created the booking can delete it.
    Only allows deletion of pending bookings.
    """
    try:
        booking = Booking.objects.get(id=booking_id, customer=request.user)
        
        # Only allow deletion of pending bookings
        if booking.status != 'pending':
            return Response({
                'error': f'Cannot delete booking with status: {booking.status}. Only pending bookings can be deleted.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        booking.delete()
        
        return Response({
            'message': 'Booking deleted successfully',
            'deleted_booking_id': booking_id
        }, status=status.HTTP_200_OK)
    
    except Booking.DoesNotExist:
        return Response({
            'error': 'Booking not found or you do not have permission to delete this booking'
        }, status=status.HTTP_404_NOT_FOUND)
