from django.http import Http404  # Exception levée si un objet n'est pas trouvé
from django.shortcuts import render  # (Non utilisé ici) Pour rendre des templates HTML
from .models import Product ,Category # Importation du modèle Product
from rest_framework.views import APIView  # Classe de base pour créer des vues basées sur les API
from rest_framework.response import Response
from rest_framework.decorators import api_view  # Permet de retourner des réponses JSON
from .serializers import ProductSerializer,CategorySerializer
from django.db.models import Q  # Sérialiseur pour convertir les objets Product en JSON

# Vue pour afficher la liste des 4 derniers produits
class LatesProductList(APIView):  
    def get(self, request, format=None):
        """
        Gestion des requêtes GET pour récupérer les 4 derniers produits.
        """
        # Récupère les 4 premiers produits dans la base de données
        products = Product.objects.all()[0:4]
        
        # Sérialise les objets Product en JSON
        serializer = ProductSerializer(products, many=True)  # many=True car il y a plusieurs objets
        
        # Retourne une réponse JSON avec les données sérialisées
        return Response(serializer.data)


# Vue pour afficher les détails d'un produit spécifique
class ProductDetail(APIView):
    def get_object(self, category_slug, product_slug):
        """
        Récupère un produit spécifique à partir des slugs de catégorie et de produit.
        """
        try:
            # Filtre les produits par le slug de catégorie et récupère le produit correspondant au slug
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            # Si aucun produit correspondant n'est trouvé, lève une erreur 404
            raise Http404

    def get(self, request, category_slug, product_slug, format=None):
        """
        Gestion des requêtes GET pour récupérer les détails d'un produit.
        """
        # Récupère le produit en fonction des slugs
        product = self.get_object(category_slug, product_slug)
        
        # Sérialise l'objet Product en JSON
        serializer = ProductSerializer(product)
        
        # Retourne une réponse JSON avec les données sérialisées
        return Response(serializer.data)


class CategoryDetail(APIView):
    def get_object(self, category_slug):
        """
        Récupère un produit spécifique à partir des slugs de catégorie et de produit.
        """
        try:
            # Filtre les produits par le slug de catégorie et récupère le produit correspondant au slug
            return Category.objects.get(slug=category_slug)
        except Product.DoesNotExist:
            # Si aucun produit correspondant n'est trouvé, lève une erreur 404
            raise Http404

    def get(self, request, category_slug,  format=None):
        """
        Gestion des requêtes GET pour récupérer les détails d'un produit.
        """
        # Récupère le produit en fonction des slugs
        category = self.get_object(category_slug)
        
        # Sérialise l'objet Product en JSON
        serializer = CategorySerializer(category)
        
        # Retourne une réponse JSON avec les données sérialisées
        return Response(serializer.data)


@api_view(["POST"])
def search(request):
    query=request.data.get('query','')
    if query:
        products=Product.objects.filter(Q(name__icontains=query)| Q(description__icontains=query))
        serializer=ProductSerializer(products,many=True)
        return Response(serializer.data)
    else:
        return Response({"products":[]})







