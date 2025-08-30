from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingSerializer

class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    
    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

class BookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    
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
