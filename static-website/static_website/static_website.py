#
# This file is part of the onema.io static_website Package.
# For the full copyright and license information,
# please view the LICENSE file that was distributed
# with this source code.
#
# @author Juan Manuel Torres <software@onema.io>
#
from aws_cdk import aws_route53, aws_s3, aws_cloudfront, aws_route53_targets, aws_s3_deployment
from aws_cdk.aws_certificatemanager import DnsValidatedCertificate
from aws_cdk.aws_cloudfront import AliasConfiguration, SourceConfiguration, CloudFrontWebDistribution
from aws_cdk.aws_route53 import HostedZone
from aws_cdk.core import Construct, CfnOutput, RemovalPolicy


class StaticWebsite(Construct):

    def __init__(self, scope: Construct, id: str, *, hosted_zone: HostedZone, site_domain: str, sources: str, website_index: str = "index.html", website_error: str = "error.html"):
        """
        This constructs creates:
            - S3 bucket
            - DNS Validated certificate
            - CloudFront web distribution
            - Route53 A record

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings. If the ID includes a path separator (``/``), then it will be replaced by double dash ``--``.
        :param hosted_zone: A route53 hosted zone
        :param site_domain: The domain or subdomain you want to use for the website
        :param sources: A path to the location of the code
        :param website_index: Name of the index page, defaults to "index.html"
        :param website_error: Name of the error page, defaults to "error.html"
        """
        super().__init__(scope, id)

        # Construct code goes here
        CfnOutput(self, "Site", value=f"https://{site_domain}")

        # Content bucket
        site_bucket = aws_s3.Bucket(self, "SiteBucket",
                                    bucket_name=site_domain,
                                    website_index_document=website_index,
                                    website_error_document=website_error,
                                    public_read_access=True,
                                    removal_policy=RemovalPolicy.DESTROY)
        CfnOutput(self, "BucketArn", value=site_bucket.bucket_arn)

        # Certificate
        cert = DnsValidatedCertificate(self, f"{id}-bucket", domain_name=site_domain, hosted_zone=hosted_zone)
        CfnOutput(self, 'CertificateArn', value=cert.certificate_arn)

        distr = CloudFrontWebDistribution(self, "SiteDistribution",
                                          alias_configuration=AliasConfiguration(
                                              acm_cert_ref=cert.certificate_arn,
                                              names=[site_domain],
                                              ssl_method=aws_cloudfront.SSLMethod.SNI,
                                              security_policy=aws_cloudfront.SecurityPolicyProtocol.TLS_V1_1_2016,
                                          ),
                                          origin_configs=[SourceConfiguration(
                                              s3_origin_source=aws_cloudfront.S3OriginConfig(s3_bucket_source=site_bucket),
                                              behaviors=[aws_cloudfront.Behavior(is_default_behavior=True)]
                                          )])
        CfnOutput(self, "DistributionId", value=distr.distribution_id)

        # Route 53 alias record for the cloudfront distribution
        aws_route53.ARecord(self, "SiteAliasRecord",
                            zone=hosted_zone,
                            target=aws_route53.AddressRecordTarget.from_alias(aws_route53_targets.CloudFrontTarget(distr)),
                            record_name=site_domain)

        aws_s3_deployment.BucketDeployment(self, "DeployWithInvalidation",
                                           sources=[aws_s3_deployment.Source.asset(sources)],
                                           destination_bucket=site_bucket,
                                           distribution=distr,
                                           distribution_paths=["/*"])
