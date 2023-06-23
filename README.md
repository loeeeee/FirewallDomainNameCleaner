# DNS cleaning service utilizing GFWatch data

## GFWatch

GFWatch is a research that focus on the temporal change of the Great Firewall censoring behaviors. It continuous monitors the censored DNS records in mainland China, and publish their URL and censoring pattern. The detailed explanation can be found in the corresponding scholar paper.

## Overview

Given the detailed data from GFWatch, we could make a DNS service that only forward queries to foreign DNS server when necessary. Otherwise, it will use local DNS resolver. DNS forwarder, because it could utilize encryption, could mitigate DNS censorship, but comes with the cost of being slow, and expensive in data usage. DNS resolver, however, is prone to DNS poisoning in mainland China. But it could find the closest/fastest CDN, which is important for improving the network performance and useability for non-tech-savvy people in the family.

## How does it work

### Read the GFWatch data

### Listen for DNS query

### Lookup for the destination
