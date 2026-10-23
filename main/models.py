from django.db import models

class UserProfile(models.Model):
    """Stores personal and professional portfolio profile details."""
    full_name = models.CharField(max_length=100, default="Divyashree L")
    headline = models.CharField(max_length=200, default="Data Analyst & Power BI Developer")
    education = models.CharField(max_length=150, default="Master of Science in Data Science")
    experience_powerbi = models.CharField(max_length=100, default="4 Years (Power BI & DAX)")
    experience_sql = models.CharField(max_length=100, default="2 Years (SQL Server)")
    email = models.EmailField(default="shreedivya08996@gmail.com")
    phone = models.CharField(max_length=50, blank=True, default="+91 7676046225")
    location = models.CharField(max_length=100, default="Remote / Open to Relocation")
    linkedin_url = models.URLField(default="https://www.linkedin.com/in/divyashree-l/")
    github_url = models.URLField(default="https://github.com/Divyashree-08996")
    bio = models.TextField(
        default="Data Analyst and Analytics Specialist with a Master's degree in Data Science, 4 years of hands-on expertise building enterprise reporting architectures in Power BI, and 2 years in relational SQL. Currently upgrading core engineering capabilities in Microsoft Fabric (OneLake, Lakehouse Medallion, Delta Lake, PySpark, Direct Lake)."
    )
    is_public = models.BooleanField(default=True, help_text="Uncheck to hide public access (restricted to admin).")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Portfolio Profile: {self.full_name}"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profile"


class VisitorLog(models.Model):
    """Tracks visitors to your portfolio (IP, page, user agent, timestamp)."""
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    page_visited = models.CharField(max_length=255)
    referrer = models.CharField(max_length=500, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Visit to {self.page_visited} from {self.ip_address} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Visitor Log"
        verbose_name_plural = "Visitor Logs"


class ContactMessage(models.Model):
    """Stores inbound inquiries from recruiters and connections."""
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=255, blank=True, default="Portfolio Inbound Message")
    message = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name} ({self.email}) - {self.timestamp.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
