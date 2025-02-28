import logging
from django.db.models.functions import TruncMonth, TruncWeek, TruncDay, TruncYear, TruncHour
from django.db.models import Count, Sum, Avg
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from masafa_app.models.masafa import Customer, Item, Invoice, Payment, Crossborder
from datetime import datetime, timedelta
from django.utils.timezone import now, make_aware

# Set up logging
logger = logging.getLogger(__name__)

class DetailedReportView(APIView):
    def get(self, request):
        try:
            filter_by = request.GET.get("filter", "month")  # Default to "month"
            selected_date = request.GET.get("date")

            if selected_date:
                selected_date = selected_date.rstrip("/") 
            if filter_by:
                filter_by = filter_by.rstrip("/") 
            
            # Handle different date formats (year, year-month, full date, ISO week date)
            if not selected_date:
                selected_date = now()  # Default: today
            else:
                try:
                    if len(selected_date) == 4:  # Year only (e.g., "2024")
                        selected_date = make_aware(datetime.strptime(selected_date, "%Y"))
                    elif len(selected_date) == 8 and selected_date[-3] == 'W':  # ISO week format (e.g., "2025-W06")
                        year, week = selected_date.split('-W')
                        # Find the first day of the specified ISO week
                        first_day_of_year = datetime.strptime(f"{year}-01-01", "%Y-%m-%d")
                        # ISO weeks are based on Monday, so we calculate the first Monday of the year
                        first_day_of_week = first_day_of_year + timedelta(days=(7 - first_day_of_year.weekday()) % 7)
                        selected_date = first_day_of_week + timedelta(weeks=int(week) - 1)
                        selected_date = make_aware(selected_date)  # Ensure it is timezone-aware
                    elif len(selected_date) == 7:  # Year and month (e.g., "2024-02")
                        selected_date = make_aware(datetime.strptime(selected_date, "%Y-%m"))
                    elif len(selected_date) == 10:  # Full date (e.g., "2024-02-17")
                        selected_date = make_aware(datetime.strptime(selected_date, "%Y-%m-%d"))
                    else:
                        logger.error(f"Invalid date format received: {selected_date}")
                        return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)
                except ValueError as e:
                    logger.exception(f"Error parsing date: {selected_date} - {e}")
                    return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)

            # Define time filters and expected time range
            date_filters = {}
            periods = []

            if filter_by == "day":
                start_time = selected_date.replace(hour=0, minute=0, second=0)
                end_time = start_time + timedelta(days=1)
                date_filters["created__range"] = [start_time, end_time]
                time_group = TruncHour("created")
                periods = [start_time + timedelta(hours=i) for i in range(24)]  # 24 hours

            elif filter_by == "week":
                start_time = selected_date - timedelta(days=selected_date.weekday())  # Start of week (Monday)
                end_time = start_time + timedelta(days=7)
                date_filters["created__range"] = [start_time, end_time]
                time_group = TruncDay("created")
                periods = [start_time + timedelta(days=i) for i in range(7)]  # 7 days

            elif filter_by == "month":
                start_time = selected_date.replace(day=1)  # Start of month
                next_month = (start_time.replace(month=start_time.month % 12 + 1, day=1)
                              if start_time.month < 12 else datetime(start_time.year + 1, 1, 1))
                date_filters["created__range"] = [start_time, next_month]
                time_group = TruncDay("created")
                periods = [start_time + timedelta(days=i) for i in range((next_month - start_time).days)]  # 30 days

            elif filter_by == "year":
                start_time = selected_date.replace(month=1, day=1)  # Start of year
                end_time = datetime(start_time.year + 1, 1, 1)  # Next year start
                date_filters["created__range"] = [start_time, end_time]
                time_group = TruncMonth("created")
                periods = [datetime(start_time.year, i, 1) for i in range(1, 13)]  # 12 months

            else:
                logger.error(f"Invalid filter type: {filter_by}")
                return Response({"error": "Invalid filter type"}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch filtered data
            filtered_invoices = Invoice.objects.filter(**date_filters)
            filtered_items = Item.objects.filter(**date_filters)

            # Aggregate invoice data
            invoice_analytics = (
                filtered_invoices
                .annotate(period=time_group)
                .values("period")
                .annotate(
                    total_invoices=Count("id"),
                    total_invoice_amount=Sum("total_amount"),
                )
            )

            # Aggregate item data
            item_analytics = (
                filtered_items
                .annotate(period=time_group)
                .values("period")
                .annotate(total_items=Count("id"))
            )

            # Merge analytics and fill missing periods
            analytics_data = {period.date(): {"period": period.date(), "total_invoices": 0, "total_invoice_amount": 0, "total_items": 0} for period in periods}

            for entry in invoice_analytics:
                period_key = entry["period"].date()  # Normalize to date
                if period_key in analytics_data:
                    analytics_data[period_key]["total_invoices"] = entry["total_invoices"]
                    analytics_data[period_key]["total_invoice_amount"] = entry["total_invoice_amount"] or 0

            for entry in item_analytics:
                period_key = entry["period"].date()  # Normalize to date
                if period_key in analytics_data:
                    analytics_data[period_key]["total_items"] = entry["total_items"]

            # Convert dictionary to sorted list
            analytics_list = sorted(analytics_data.values(), key=lambda x: x["period"])

            # Aggregate overall report data
            report_data = {
                "total_customers": Customer.objects.filter(**date_filters).count(),
                "total_items": filtered_items.count(),
                "total_invoices": filtered_invoices.count(),
                "total_payments": round(Payment.objects.filter(**date_filters).aggregate(total=Sum("amount"))["total"] or 0, 2),
                "avg_invoice_amount": round(filtered_invoices.aggregate(avg=Avg("total_amount"))["avg"] or 0, 2),
                "top_items": list(
                    filtered_items
                    .values("name")
                    .annotate(count=Count("id"))
                    .order_by("-count")[:6]
                ),
                "analytics": analytics_list,
            }


            return Response(report_data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception(f"Unexpected error in DetailedReportView: {e}")
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
