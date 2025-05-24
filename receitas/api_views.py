# Import necessary modules from Django REST Framework and the project.
from rest_framework import status, views
from rest_framework.response import Response
import os
import re
# Import Django settings for accessing media paths.
from django.conf import settings
from django.core.exceptions import ValidationError
from .serializers import ReceitaSerializer
from .utils import extrair_texto_pdf, TesseractError, check_medicine_availability, clean_medicine_names, fuzzy_match_medicine_names
from .models import Receita


# Define the API view for uploading prescriptions.
class ReceitaUploadAPIView(views.APIView):
    # Define the POST method to handle file uploads.
    def post(self, request):
        try:
            # Initialize an empty list to store the medicine data.
            medicine_data = []
            # Serialize the request data using ReceitaSerializer.
            serializer = ReceitaSerializer(data=request.data)
            # Check if the serialized data is valid.
            if serializer.is_valid():
                # Save the valid prescription data.
                receita = serializer.save()
                # Construct the full path to the uploaded PDF file.
                caminho_pdf = os.path.join(settings.MEDIA_ROOT, receita.pdf.name)
                # Extract text from the PDF using the extrair_texto_pdf utility function.
                ocr_result = extrair_texto_pdf(caminho_pdf, psm=6)
                texto = ocr_result['text']
                confidence = ocr_result['confidence']
                
                # Use regex to extract medicine names from the text.
                # This part will be improved with the utils functions.
                # TODO: Extract dosage and quantity from the text.
                medicine_names = re.findall(r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*', texto)  

                # Clean the medicine names
                cleaned_medicine_names = clean_medicine_names(medicine_names)

                # Do fuzzy matching to find medicine names with mistakes
                fuzzy_matched_names = fuzzy_match_medicine_names(cleaned_medicine_names)

                # Check medicine availability
                medicine_availability = check_medicine_availability(fuzzy_matched_names)

                # Create a list of dictionaries with the medicine name and availability.
                for medicine in medicine_availability:
                    # Extract dosage and quantity if available.
                    dosage_match = re.search(r'(\d+\s?mg)', texto, re.IGNORECASE)
                    dosage = dosage_match.group(1) if dosage_match else None
                    quantity_match = re.search(r'(\d+)(?:\s?(comprimidos|capsulas|unidades))?', texto, re.IGNORECASE)
                    quantity = quantity_match.group(1) if quantity_match else None
                    
                    medicine_data.append({'medicine_name': medicine['nome'], 'available': medicine['disponivel'], 'confidence': confidence, 'dosage': dosage, 'quantity': quantity})

                # Store the extracted text in the receita object.
                receita.texto_extraido = texto
                # Save the updated prescription object.
                receita.save()

                # Add medicine data to response
                receita.medicine_data = medicine_data
                # Return the serialized prescription data with a 201 status.
                return Response(ReceitaSerializer(receita).data, status=status.HTTP_201_CREATED)
            # Return serializer errors with a 400 status if the data is invalid.
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            # Handle validation errors.
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except TesseractError as e:
            # Handle errors from the Tesseract OCR process.
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # Handle any other unexpected errors.
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
