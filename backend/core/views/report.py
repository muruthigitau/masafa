from django.db.models.functions import TruncMonth, TruncWeek, TruncDay, TruncYear
from django.db.models import Count, Sum, Avg
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from masafa_app.models.masafa import Customer, Item, Invoice, Payment, Crossborder
from datetime import datetime, timedelta
from django.utils.timezone import now


class DetailedReportSerializer(serializers.Serializer):
    total_customers = serializers.IntegerField()
    total_crossborders = serializers.IntegerField()
    total_items = serializers.IntegerField()
    total_invoices = serializers.IntegerField()
    total_payments = serializers.DecimalField(max_digits=10, decimal_places=2)
    avg_invoice_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    top_items = serializers.ListField()
    analytics = serializers.ListField()


class DetailedReportView(APIView):
    def get(self, request):
        filter_by = request.GET.get('filter_by', 'month')  # Default: month
        selected_date = request.GET.get('selected_date')

        if not selected_date:
            selected_date = now().date()
        else:
            try:
                selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
            except ValueError:
                return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)

        date_filters = {}
        if filter_by == "day":
            date_filters["created__date"] = selected_date
            time_group = TruncDay("created")

        elif filter_by == "week":
            start_week = selected_date - timedelta(days=6)
            date_filters["created__range"] = [start_week, selected_date]
            time_group = TruncWeek("created")

        elif filter_by == "month":
            start_month = selected_date - timedelta(days=30)
            date_filters["created__range"] = [start_month, selected_date]
            time_group = TruncMonth("created")

        elif filter_by == "year":
            start_year = selected_date.replace(month=1, day=1)
            date_filters["created__range"] = [start_year, selected_date]
            time_group = TruncYear("created")

        else:
            return Response({"error": "Invalid filter"}, status=status.HTTP_400_BAD_REQUEST)

        # Apply filters to both Invoices and Items
        filtered_invoices = Invoice.objects.filter(**date_filters)
        filtered_items = Item.objects.filter(**date_filters)

        # Aggregate analytics for invoices
        invoice_analytics = (
            filtered_invoices
            .annotate(period=time_group)
            .values("period")
            .annotate(
                total_invoices=Count("id"),
                total_invoice_amount=Sum("total_amount")
            )
        )

        # Aggregate analytics for items
        item_analytics = (
            filtered_items
            .annotate(period=time_group)
            .values("period")
            .annotate(
                total_items=Count("id")
            )
        )

        # Merge invoice and item analytics into a single list
        analytics_data = {}
        for entry in invoice_analytics:
            period = entry["period"]
            analytics_data[period] = {
                "period": period,
                "total_invoices": entry["total_invoices"],
                "total_invoice_amount": entry["total_invoice_amount"],
                "total_items": 0  # Default, to be updated
            }

        for entry in item_analytics:
            period = entry["period"]
            if period in analytics_data:
                analytics_data[period]["total_items"] = entry["total_items"]
            else:
                analytics_data[period] = {
                    "period": period,
                    "total_invoices": 0,  # Default, to be updated
                    "total_invoice_amount": 0,
                    "total_items": entry["total_items"]
                }

        # Convert dictionary to a sorted list
        analytics_list = sorted(analytics_data.values(), key=lambda x: x["period"])

        # Aggregate overall report data
        report_data = {
            "total_customers": Customer.objects.filter(**date_filters).count(),
            "total_crossborders": Crossborder.objects.filter(**date_filters).count(),
            "total_items": filtered_items.count(),
            "total_invoices": filtered_invoices.count(),
            "total_payments": Payment.objects.filter(**date_filters).aggregate(total=Sum("amount"))["total"] or 0,
            "avg_invoice_amount": filtered_invoices.aggregate(avg=Avg("total_amount"))["avg"] or 0,
            "top_items": list(
                filtered_items
                .values("name")
                .annotate(count=Count("id"))
                .order_by("-count")[:5]
            ),
            "analytics": analytics_list,
        }

        serializer = DetailedReportSerializer(report_data)
        return Response(serializer.data, status=status.HTTP_200_OK)
