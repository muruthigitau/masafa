from rest_framework import generics, status
from rest_framework.response import Response
from .template import GenericViewSet
import random
from django.utils import timezone

import json
import requests
from core.utils import send_custom_email, send_sms
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from masafa_app.models.masafa import Crossborder, Item, Dispatch, Customer, Invoice
     
from masafa_app.serializers.masafa import InvoiceSerializer, ItemSerializer, DiscountSerializer, ServiceSerializer


class AddItemToDispatchAPIView(APIView):
    def post(self, request, *args, **kwargs):
        dispatch_id = request.data.get("dispatch_id")
        item_id = request.data.get("item_id")

        if not dispatch_id or not item_id:
            return Response(
                {"error": "dispatch_id and item_id are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            dispatch = Dispatch.objects.get(id=dispatch_id)
            item = Item.objects.get(id=item_id)
            if item.status != "Ready For Collection" or item.customer != dispatch.customer:
                return Response(
                    {"error": "Item not ready for dispatch"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            item.status="Dispatched"
            item.save()
        except Dispatch.DoesNotExist:
            return Response(
                {"error": "Dispatch not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Item.DoesNotExist:
            return Response(
                {"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Add the item to the many-to-many field
        dispatch.items.add(item)

        # Return a simple success message
        return Response(
            {"message": "Item added successfully"}, status=status.HTTP_200_OK
        )


class AddItemToCrossborderAPIView(APIView):
    def post(self, request, *args, **kwargs):
        crossborder_id = request.data.get("crossborder_id")
        item_id = request.data.get("item_id")
        action = request.data.get("action")
        next_status = "" 
        current_status = ""
        if action == "Load":
            next_status = "In Transit" 
            current_status = "Received"
        elif action == "Offload":
            next_status = "Ready For Collection" 
            current_status = "In Transit"        

        if not crossborder_id or not item_id:
            return Response(
                {"error": "crossborder_id and item_id are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            crossborder = Crossborder.objects.get(id=crossborder_id)
            item = Item.objects.get(id=item_id)
            if item.status != current_status:
                return Response(
                    {"error": "Item not ready for transit"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            item.status=next_status
            item.save()
        except Crossborder.DoesNotExist:
            return Response(
                {"error": "Crossborder not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Item.DoesNotExist:
            return Response(
                {"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Add the item to the many-to-many field
        crossborder.items.add(item)

        # Return a simple success message
        return Response(
            {"message": "Item added successfully"}, status=status.HTTP_200_OK
        )

          
class TransitCrossborderAPIView(APIView):
    def post(self, request, *args, **kwargs):
        crossborder_id = request.data.get("crossborder_id")
        action = request.data.get("action")

        if not crossborder_id:
            return Response(
                {"error": "crossborder_id required"},
                status=status.HTTP_400_BAD_REQUEST,
            ) 

        try:
            crossborder = Crossborder.objects.get(id=crossborder_id)
            items = crossborder.items.all()
             # Add the item to the many-to-many field
            if action == "Offload":
                scanned_items = items.filter(status="Ready For Collection")
                missing_items = items.exclude(id__in=scanned_items.values_list('id', flat=True))
                if missing_items.exists():
                    missing_item_ids = list(
                        missing_items.values('id', 'name')  
                    )
                    return Response(
                        {"error": "Some items are missing from crossborder", "data": missing_item_ids},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            
            if action == "Transit": 
                crossborder.loaded_at = timezone.now()
            if action == "Offload": 
                crossborder.offloaded_at = timezone.now()
            crossborder.save()
            customers = {}
            for item in items:
                if action == "Transit": 
                    item.status = "In Transit"
                if action == "Offload": 
                    item.status = "Ready For Collection"
                item.save()
                if item.customer:
                    customer = item.customer
                    if customer not in customers:
                        customers[customer] = []
                    customers[customer].append(item)
                    
            for customer, customer_items in customers.items():
                    item_names = ", ".join([item.name for item in customer_items])
                    item_ids = ", ".join([str(item.id) for item in customer_items])

                    if action == "Transit": 
                        message = (
                            f"Hi {customer.first_name}, your goods ({item_names}) are on their way. "
                            f"Use Item IDs ({item_ids}) for tracking: "
                            f"https://masafalogistics.com/tracking?phone={customer.phone}. "
                            "Thank you!"
                        ) 
                        sms_message = (
                            f"Hi {customer.first_name}, your ({len(customer_items)}) good(s) are on their way. "
                            f"https://masafalogistics.com/tracking?phone={customer.phone}. "
                            "Thank you!"
                        )

                    elif action == "Offload":
                        message = (
                            f"Hi {customer.first_name}, your goods ({item_names}) are ready for pickup. "
                            f"Details: https://masafalogistics.com/pickup?phone={customer.phone}. "
                            "Thank you!"
                        ) 
                        sms_message = (
                            f"Hi {customer.first_name}, your ({len(customer_items)}) good(s) are ready for pickup. "
                            f"Details: https://masafalogistics.com/pickup?phone={customer.phone}. "
                            "Thank you!"
                        ) 
                        
                    # Send SMS
                    send_sms(customer.phone, sms_message)

                    # Send email
                    context = {"message": message}
                    send_custom_email(
                        "Goods In Transit", "email/default.html", context, [customer.email]
                    )
                    
            if action == "Transit":
                # Step 1: Group items by unique customers

                # Step 2: Create an invoice for each customer
                for customer, customer_items in customers.items():
                    # Filter out items that are already included in other invoices
                    new_items = []
                    for item in customer_items:
                        if not Invoice.objects.filter(items=item).exists():  # Check if item exists in another invoice
                            new_items.append(item)

                    if new_items:  # Only create an invoice if there are new items to add
                        # Create a new invoice for the customer
                        invoice = Invoice.objects.create(customer=customer, type="Invoice")
                        invoice.items.set(new_items)  # Set the new items to the invoice
                        invoice.save()

                        # Send SMS notification
                        message = (
                            f"Hi {customer.first_name}, your invoice ({invoice.id}) has been generated. "
                            f"Track it here: https://masafalogistics.com/tracking?phone={customer.phone}&invoice={invoice.id}. "
                            "Thank you!"
                        )

                        send_sms(customer.phone, message)

                        # Send email notification
                        context = {
                            "message": message,
                        }
                        send_custom_email(
                            "Invoice", "email/default.html", context, [customer.email]
                        )

        except Crossborder.DoesNotExist:
            return Response(
                {"error": "Crossborder not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Item.DoesNotExist:
            return Response(
                {"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND
            )

       

        # Return a simple success message
        return Response(
            {"message": "Item added successfully"}, status=status.HTTP_200_OK
        )
 

class ItemDispatchAPIView(APIView):
    def post(self, request, *args, **kwargs):
        item_id = request.data.get("item_id")

        if not item_id:
            return Response(
                {"error": "item_id required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            dispatch = Dispatch.objects.get(id=item_id)
            customer = dispatch.customer

            # Get expected items for the customer (those with status "Ready For Collection")
            expected_items = Item.objects.filter(customer=customer, status="Ready For Collection")

            # Get the items already in the dispatch
            dispatched_items = dispatch.items.all()

            # Find items that are expected but not yet dispatched, comparing using 'id'
            missing_items = expected_items.exclude(id__in=dispatched_items.values_list('id', flat=True))

            # If there are missing items, return an error with the list of missing item IDs
            if missing_items.exists():
                missing_item_ids = list(
                    missing_items.values('id', 'name')  # Get both 'id' and 'name' fields
                )
                return Response(
                    {"error": "Some items are missing from dispatch", "data": missing_item_ids},
                    status=status.HTTP_400_BAD_REQUEST,
                )                

        except Dispatch.DoesNotExist:
            return Response(
                {"error": "Dispatch not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Item.DoesNotExist:
            return Response(
                {"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Return a success message if everything is fine
        return Response(
            {"message": "Items dispatched successfully"}, status=status.HTTP_200_OK
        )
   

class TrackItemsView(generics.GenericAPIView):
    serializer_class = ItemSerializer

    def get(self, request, *args, **kwargs):
        phone = request.GET.get('phone')
        item_id = request.GET.get('id', '').lstrip('/')
        invoice_id = request.GET.get('invoice', '').lstrip('/')

        if not phone or (not item_id and not invoice_id):
            return Response({'detail': 'Phone and either id or invoice are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Strip all spaces from the phone number
        phone = ''.join(phone.split())

        # Validate phone length
        if len(phone) <= 8:
            return Response({'detail': 'Phone number must be longer than 8 characters.'}, status=status.HTTP_400_BAD_REQUEST)

        # Use the last 9 characters
        phone = phone[-9:]

        # Retrieve items based on invoice or item id
        if invoice_id:
            return self._get_items_by_invoice(invoice_id, phone)
        else:
            return self._get_items_by_id(item_id, phone)

    def _get_items_by_invoice(self, invoice_id, phone):
        try:
            invoice_obj = Invoice.objects.get(id=invoice_id, customer__phone__icontains=phone)
            items = invoice_obj.items.all().order_by('-created_at')[:20]
            serializer = self.get_serializer(items, many=True)
            return Response(serializer.data)
        except Invoice.DoesNotExist:
            return Response({'detail': 'Invoice not found for the provided phone number.'}, status=status.HTTP_404_NOT_FOUND)

    def _get_items_by_id(self, item_id, phone):
        items = Item.objects.filter(id__icontains=item_id, customer__phone__icontains=phone).order_by('-created_at')[:20]
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)


class CreateInvoiceView(generics.CreateAPIView):
    serializer_class = InvoiceSerializer

    def post(self, request, *args, **kwargs):
        # Extracting data from the request
        document_data = request.data.get('document', {})
        items_data = request.data.get('items', [])
        services_data = request.data.get('services', [])
        discounts_data = request.data.get('discounts', [])
     
        customer_info = document_data.get('customer', '')
        if not customer_info:
            return Response({'detail': 'Customer information is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Extract customer ID from the provided customer info
        customer = self._get_customer(customer_info)
        if not customer:
            return Response({'detail': 'Customer not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Prepare invoice data
        invoice_data = document_data.copy()
        invoice_data['customer'] = customer.id
        if 'type' not in invoice_data:
            invoice_data['type'] = "Invoice"
        invoice_serializer = self.get_serializer(data=invoice_data)

        if invoice_serializer.is_valid():
            invoice = invoice_serializer.save()
            invoice.creater_user =request.user
            invoice.save()
            # Pass the operation type to create associations
            self._create_associations(request, invoice, items_data, services_data, discounts_data, customer, item_type=document_data["type"])
            return Response(invoice_serializer.data, status=status.HTTP_201_CREATED)

        return Response(invoice_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _get_customer(self, customer_info):
        # Assuming the customer_info contains a unique identifier such as a phone number
        try:
            return Customer.objects.get(pk=customer_info)
        except Customer.DoesNotExist:
            return None

    def _create_associations(self, request, invoice, items_data, services_data, discounts_data, customer, item_type):
        # Create items and associate them with the customer
        for item_data in items_data:
            item_data['id'] = f"ML#####"
            item_data['type'] = item_type  # Set the item type based on the operation type
            item_data['status'] = "Received"
            item_serializer = ItemSerializer(data=item_data)
            if item_serializer.is_valid():
                item = item_serializer.save(customer=customer) 
                item.creater_user = request.user 
                item.save()# Associate the item with the customer
                invoice.items.add(item)

        # Create services
        for service_data in services_data:
            service_serializer = ServiceSerializer(data=service_data)
            if service_serializer.is_valid():
                service = service_serializer.save()
                invoice.services.add(service)

        # Create discounts
        for discount_data in discounts_data:
            discount_serializer = DiscountSerializer(data=discount_data)
            if discount_serializer.is_valid():
                discount = discount_serializer.save()
                invoice.discounts.add(discount)