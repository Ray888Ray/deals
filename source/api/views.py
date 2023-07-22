import csv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Client, Deal, Gem
from django.db.models import Sum
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.db.models import Count


class DealsUploadView(APIView):

    def post(self, request):
        csv_file = request.FILES.get('deals', None)

        if not csv_file:
            return Response({'Error': 'No CSV file provided in the request.'}, status=status.HTTP_400_BAD_REQUEST)

        decoded_file = csv_file.read().decode('utf-8')
        reader = csv.reader(decoded_file.splitlines())
        next(reader)

        for row in reader:
            customer, item, total, quantity, date = row
            client, _ = Client.objects.get_or_create(username=customer)

            deal = Deal.objects.create(
                customer=client,
                item=item,
                total=total,
                quantity=quantity,
                date=date,
            )

            gem_names = [item.strip() for item in item.split(',')]

            for gem_name in gem_names:
                gem, _ = Gem.objects.get_or_create(name=gem_name)
                deal.gems.add(gem)

        return Response({'Status': 'OK'}, status=status.HTTP_201_CREATED)


class TopClientsView(APIView):
    @method_decorator(cache_page(60 * 15))
    def get(self, request):
        print("Executing the view method")
        top_clients = Client.objects.annotate(spent_money=Sum('deals__total')).order_by('-spent_money')[:5]
        top_client_ids = top_clients.values_list('id', flat=True)
        common_gems = Gem.objects.filter(deals__customer__in=top_client_ids).annotate(client_count=Count('deals__customer', distinct=True)).filter(client_count__gte=2)
        response_data = []

        for client in top_clients:
            client_gems = client.deals.filter(gems__in=common_gems).values_list('gems__name', flat=True).distinct()

            response_data.append({
                'username': client.username,
                'spent_money': client.spent_money,
                'gems': list(client_gems),
            })

        return Response({'response': response_data}, status=status.HTTP_200_OK)







