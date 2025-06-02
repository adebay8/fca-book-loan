from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.utils import timezone

from catalog.models import BookItem
from rentals.models import Rental


def staff_required(view_func):
    return user_passes_test(lambda u: u.is_staff, login_url=None)(view_func)


@login_required
@staff_required
def borrow_book_item(request, item_id):
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST allowed")

    item = get_object_or_404(BookItem, pk=item_id)

    if not item.is_available:
        return JsonResponse({"error": "This item is already borrowed."}, status=400)

    Rental.objects.create(
        user=request.user,
        book_item=item,
    )

    item.is_available = False
    item.save(update_fields=["is_available"])

    return JsonResponse(
        {"message": f"BookItem #{item.id} (“{item.book.title}”) marked as borrowed."}
    )


@login_required
@staff_required
def return_book_item(request, item_id):
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST allowed")

    item = get_object_or_404(BookItem, pk=item_id)

    try:
        rental = Rental.objects.get(book_item=item, returned_at__isnull=True)
    except Rental.DoesNotExist:
        return JsonResponse(
            {"error": "No active rental found for this item."}, status=400
        )

    rental.returned_at = timezone.now()
    rental.save(update_fields=["returned_at"])

    item.is_available = True
    item.save(update_fields=["is_available"])

    return JsonResponse(
        {
            "message": f"BookItem #{item.id} (“{item.book.title}”) returned and marked available. Notifications enqueued."
        }
    )


# @user_passes_test(lambda u: u.is_staff)
# @login_required
def active_rental_report(request):
    """
    Returns a report of currently rented books and how long they’ve been rented.
    """
    active_rentals = Rental.objects.filter(returned_at__isnull=True).select_related(
        "book_item__book"
    )

    report = []
    for rental in active_rentals:
        book = rental.book_item.book
        days = (timezone.now() - rental.created_at).days

        report.append(
            {
                "book_title": book.title,
                "book_item_id": rental.book_item.id,
                "rented_by": rental.user.username,
                "rented_at": rental.created_at.strftime("%Y-%m-%d %H:%M"),
                "days_rented": days,
            }
        )

    summary = {"total_active_rentals": active_rentals.count(), "rentals": report}

    return JsonResponse(summary)
