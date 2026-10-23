from .models import VisitorLog

class VisitorTrackingMiddleware:
    """
    Lightweight middleware to track visitors, pages visited, referrers, and IPs.
    Skips tracking for static files, media, and internal admin asset polling.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        # Ignore static assets, favicon, and admin ajax
        ignored_prefixes = ['/static/', '/media/', '/favicon.ico']
        should_log = not any(path.startswith(prefix) for prefix in ignored_prefixes)

        if should_log and not path.startswith('/admin/jsi18n/'):
            try:
                # Resolve client IP (supporting reverse proxies / X-Forwarded-For)
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0].strip()
                else:
                    ip = request.META.get('REMOTE_ADDR')

                user_agent = request.META.get('HTTP_USER_AGENT', '')
                referrer = request.META.get('HTTP_REFERER', '')

                # Async or quick DB record creation
                VisitorLog.objects.create(
                    ip_address=ip,
                    page_visited=path,
                    referrer=referrer[:500] if referrer else None,
                    user_agent=user_agent[:1000] if user_agent else None
                )
            except Exception:
                # Fail silently so user navigation is never blocked
                pass

        response = self.get_response(request)
        return response
