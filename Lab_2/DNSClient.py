import dns.resolver

target_domain = "www.youtube.com"
output_log_file = "dns_log.txt"

with open(output_log_file, "w") as log_writer:
    log_writer.write(f"Let me analyze the DNS records for: {target_domain}\n")
    
    for dns_record_type in ['A', 'MX', 'CNAME']:
        try:
            query_results = dns.resolver.resolve(target_domain, dns_record_type)
            log_writer.write(f"\nFound these {dns_record_type} records:\n")
            for dns_record in query_results:
                log_writer.write(f"- {dns_record.to_text()}\n")
        except Exception as lookup_error:
            log_writer.write(f"\nCouldn't find {dns_record_type} records, got this error: {lookup_error}\n")

print(f"All done! I've saved the DNS lookup results to '{output_log_file}' for you to check out.")

