from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Booking
from .serializers import BookingSerializer


class BookingListAPIView(generics.ListAPIView):
    """
    Returns all bookings for the logged-in user.
    Uses select_related for query optimization.
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(
            user=self.request.user
        ).select_related('restaurant', 'table')


class BookingCreateAPIView(generics.CreateAPIView):
    """
    Creates a new booking for the logged-in user.
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BookingCancelAPIView(APIView):
    """
    Cancels a booking belonging to the logged-in user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, user=request.user)
            booking.status = 'cancelled'
            booking.save()
            return Response(
                {'message': 'Booking cancelled successfully.'},
                status=status.HTTP_200_OK
            )
        except Booking.DoesNotExist:
            return Response(
                {'error': 'Booking not found.'},
                status=status.HTTP_404_NOT_FOUND
            )