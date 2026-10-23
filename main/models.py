from django.db import models

class UserProfile(models.Model):
    """Stores personal and professional portfolio profile details."""
    full_name = models.CharField(max_length=100, default="Alex Rivera")
    headline = models.CharField(max_length=200, default="Data Analyst & Power BI / Microsoft Fabric Specialist")
    education = models.CharField(max_length=150, default="Master of Science in Data Science")
    experience_powerbi = models.CharField(max_length=100, default="4 Years (Power BI & DAX)")
    experience_sql = models.CharField(max_length=100, default="2 Years (SQL Server / PostgreSQL)")
    email = models.EmailField(default="analyst@example.com")
    phone = models.CharField(max_length=50, blank=True, default="+1 (555) 019-2834")
    location = models.CharField(max_length=100, default="Remote / Open to Relocation")
    linkedin_url = models.URLField(default="https://www.linkedin.com/in/your-linkedin-profile/")
    github_url = models.URLField(default="https://github.com/your-github-username")
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


class WorkExperience(models.Model):
    """Work experience timeline entries."""
    role_title = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150)
    location = models.CharField(max_length=100, blank=True, default="Remote")
    duration = models.CharField(max_length=100, help_text="e.g. 2023 - Present or Jan 2022 - Mar 2024")
    is_current = models.BooleanField(default=False)
    bullet_points = models.TextField(help_text="Enter achievements/responsibilities, one per line")
    technologies = models.CharField(max_length=255, help_text="Comma-separated: Power BI, DAX, SQL, SSIS")
    order = models.PositiveIntegerField(default=1)

    def get_bullet_list(self):
        return [b.strip() for b in self.bullet_points.split('\n') if b.strip()]

    def get_tech_list(self):
        return [t.strip() for t in self.technologies.split(',') if t.strip()]

    def __str__(self):
        return f"{self.role_title} at {self.company_name} ({self.duration})"

    class Meta:
        ordering = ['order', '-id']
        verbose_name = "Work Experience"
        verbose_name_plural = "Work Experiences"


class Education(models.Model):
    """Academic credentials and degrees."""
    degree = models.CharField(max_length=150)
    institution = models.CharField(max_length=150)
    year = models.CharField(max_length=50, help_text="e.g. 2022 - 2024")
    grade_or_honors = models.CharField(max_length=100, blank=True, default="First Class with Distinction")
    details = models.TextField(blank=True, help_text="Coursework, research, or thesis focus")
    order = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.degree} - {self.institution} ({self.year})"

    class Meta:
        ordering = ['order', '-id']
        verbose_name = "Education"
        verbose_name_plural = "Education"


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
