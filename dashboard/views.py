from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .services import DashboardService
import json
import logging

logger = logging.getLogger('dashboard')

class DashboardView(View):
    def get(self, request):
        return render(request, 'dashboard/index.html')

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        try:
            data = json.loads(request.body)
            org_id = data.get('organization_id')
            public_key = data.get('public_key')
            private_key = data.get('private_key')
            
            if not org_id:
                return JsonResponse({'error': 'Organization ID is required'}, status=400)

            logger.info(f"Dashboard request for organization: {org_id}")
            
            # Create service with provided credentials
            dashboard_service = DashboardService(public_key, private_key)
            result = dashboard_service.get_organization_data(org_id)
            
            if 'error' in result:
                logger.error(f"Dashboard error: {result['error']}")
                return JsonResponse(result, status=400)
            
            return JsonResponse(result)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error in dashboard view: {e}")
            return JsonResponse({'error': str(e)}, status=500)
