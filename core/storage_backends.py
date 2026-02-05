from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    # All files collected by `collectstatic` will be stored under:
    #   s3://<bucket>/static/...
    # This keeps static assets separated from user uploads.
    location = "static"

    # IMPORTANT (modern S3 requirement):
    # New S3 buckets have "Object Ownership = Bucket owner enforced"
    # which completely disables ACLs.
    #
    # Older django-storages tutorials set:
    #   default_acl = "public-read"
    # which now causes S3 to reject uploads with:
    #   AccessControlListNotSupported
    #
    # Setting this to None tells django-storages:
    #   "Do NOT send any ACL header at all"
    # which is exactly what modern S3 expects.
    default_acl = None


class MediaStorage(S3Boto3Storage):
    # User-uploaded files will be stored under:
    #   s3://<bucket>/media/...
    # This keeps them separate from static files.
    location = "media"

    # We NEVER want user uploads to overwrite existing files
    # if two users upload files with the same name.
    # django-storages will automatically rename the new file instead.
    file_overwrite = False

    # Same ACL reasoning as StaticStorage.
    # Without this, uploads will fail in modern S3 buckets.
    default_acl = None
