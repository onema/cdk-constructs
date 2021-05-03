
# Simple static site CDK construct 

This constructs creates a static website hosted on S3.

## Requirements
- Hosted zone in Route53

## Usage
This constructs creates:
- S3 bucket
- DNS Validated certificate
- CloudFront web distribution
- Route53 A record 

 
```python
from aws_cdk.core import Stack, Construct
from static_website import StaticWebsite
from aws_cdk.aws_route53 import HostedZone

class WebSiteStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):

        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        
        zone = HostedZone.from_lookup(self, "HostedZone", 
                                      domain_name="mydomain.com", 
                                      private_zone=False)

        StaticWebsite(self, "serverlesslink-website",
                              hosted_zone=zone,
                              site_domain="blog.mydomain.com",
                              sources="../public",
                              website_error="404.html")
```

### Website without custom domain
```python
from aws_cdk.core import Stack, Construct
from static_website import StaticWebsite

class WebSiteStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):

        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        StaticWebsite(self, "serverlesslink-website",
                              sources="../public",
                              website_error="404.html")
```