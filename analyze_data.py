import pandas as pd
import numpy as np
from collections import Counter
import json

# Read the CSV file
df = pd.read_csv(r'D:\cluade\csvdata-2.csv')

# Clean column names (remove extra spaces)
df.columns = df.columns.str.strip()

print("="*80)
print("DATA OVERVIEW")
print("="*80)
print(f"Total rows in dataset: {len(df):,}")
print(f"Total requests (weighted by COUNT): {df['COUNT'].sum():,}")
print(f"\nColumns: {list(df.columns)}")
print(f"\nData date range: {df['CREATED_AT'].unique()}")

# Status breakdown
print("\n" + "="*80)
print("1. OVERALL SUCCESS RATE ANALYSIS")
print("="*80)

status_counts = df.groupby('STATUS')['COUNT'].sum().sort_values(ascending=False)
total_requests = status_counts.sum()

print(f"\nStatus Distribution (Total requests: {total_requests:,}):")
print("-" * 60)
for status, count in status_counts.items():
    percentage = (count / total_requests) * 100
    print(f"{status:30s}: {count:6,} ({percentage:5.2f}%)")

# Calculate success rate
success_count = status_counts.get('Shared', 0)
failed_count = status_counts.get('Failed', 0)
rejected_count = status_counts.get('User Rejected', 0)
no_action_count = status_counts.get('No Action Taken', 0)
saved_later_count = status_counts.get('Saved For Later', 0)

terminal_states = success_count + failed_count + rejected_count
success_rate = (success_count / terminal_states) * 100 if terminal_states > 0 else 0

print(f"\n{'='*60}")
print(f"SUCCESS METRICS:")
print(f"{'='*60}")
print(f"Successful shares (Shared): {success_count:,} ({(success_count/total_requests)*100:.2f}% of all)")
print(f"Technical failures (Failed): {failed_count:,} ({(failed_count/total_requests)*100:.2f}% of all)")
print(f"User rejections: {rejected_count:,} ({(rejected_count/total_requests)*100:.2f}% of all)")
print(f"Abandoned (No Action Taken): {no_action_count:,} ({(no_action_count/total_requests)*100:.2f}% of all)")
print(f"Saved for later: {saved_later_count:,} ({(saved_later_count/total_requests)*100:.2f}% of all)")
print(f"\n>>> SUCCESS RATE (Shared / Terminal states): {success_rate:.2f}%")
print(f">>> CONVERSION RATE (Shared / All requests): {(success_count/total_requests)*100:.2f}%")

# Failure analysis
print("\n" + "="*80)
print("FAILURE POINT ANALYSIS")
print("="*80)

failed_df = df[df['STATUS'] == 'Failed']
if len(failed_df) > 0:
    failure_reasons = failed_df.groupby('FAILURE_REASON')['COUNT'].sum().sort_values(ascending=False)
    print(f"\nFailure Reasons (Total failures: {failed_df['COUNT'].sum():,}):")
    print("-" * 60)
    for reason, count in failure_reasons.items():
        percentage = (count / failed_df['COUNT'].sum()) * 100
        print(f"{str(reason):50s}: {count:5,} ({percentage:5.2f}%)")

    error_categories = failed_df.groupby('ERROR_CATEGORIZATION')['COUNT'].sum().sort_values(ascending=False)
    print(f"\nError Categories:")
    print("-" * 60)
    for category, count in error_categories.items():
        percentage = (count / failed_df['COUNT'].sum()) * 100
        print(f"{str(category):50s}: {count:5,} ({percentage:5.2f}%)")

# Document availability impact
print("\n" + "="*80)
print("2. DOCUMENT AVAILABILITY IMPACT")
print("="*80)

doc_avail_analysis = df.groupby('DOC_AVAILIBILITY').agg({
    'COUNT': 'sum',
    'STATUS': lambda x: pd.Series(x).value_counts().to_dict()
}).reset_index()

print("\nOverall Distribution:")
print("-" * 60)
for idx, row in doc_avail_analysis.iterrows():
    total = row['COUNT']
    percentage = (total / total_requests) * 100
    print(f"\n{row['DOC_AVAILIBILITY']}: {total:,} requests ({percentage:.2f}%)")

    status_dict = row['STATUS']
    for status, count_list in status_dict.items():
        status_pct = (count_list / total) * 100
        print(f"  - {status:25s}: {count_list:6,} ({status_pct:5.2f}%)")

# Success rate by document availability
print("\n" + "="*60)
print("SUCCESS RATE COMPARISON:")
print("="*60)

for doc_status in df['DOC_AVAILIBILITY'].unique():
    subset = df[df['DOC_AVAILIBILITY'] == doc_status]
    subset_total = subset['COUNT'].sum()
    subset_shared = subset[subset['STATUS'] == 'Shared']['COUNT'].sum()
    subset_failed = subset[subset['STATUS'] == 'Failed']['COUNT'].sum()
    subset_rejected = subset[subset['STATUS'] == 'User Rejected']['COUNT'].sum()

    terminal = subset_shared + subset_failed + subset_rejected
    if terminal > 0:
        success_rate_doc = (subset_shared / terminal) * 100
        conversion_rate_doc = (subset_shared / subset_total) * 100
        print(f"\n{doc_status}:")
        print(f"  Total requests: {subset_total:,}")
        print(f"  Shared: {subset_shared:,}")
        print(f"  Failed: {subset_failed:,}")
        print(f"  Rejected: {subset_rejected:,}")
        print(f"  >>> Success rate (Shared/Terminal): {success_rate_doc:.2f}%")
        print(f"  >>> Conversion rate (Shared/All): {conversion_rate_doc:.2f}%")

# Mandatory documents analysis
print("\n" + "="*80)
print("MANDATORY DOCUMENTS FULFILLMENT ANALYSIS")
print("="*80)

mand_fulfilled_analysis = df.groupby('MANDATORY_DOCS_FULFILLED').agg({
    'COUNT': 'sum',
    'STATUS': lambda x: pd.Series(x).value_counts().to_dict()
})

print("\nBy Mandatory Documents Fulfilled:")
print("-" * 60)
for fulfilled_status in df['MANDATORY_DOCS_FULFILLED'].unique():
    subset = df[df['MANDATORY_DOCS_FULFILLED'] == fulfilled_status]
    subset_total = subset['COUNT'].sum()
    subset_shared = subset[subset['STATUS'] == 'Shared']['COUNT'].sum()

    print(f"\nMandatory Docs Fulfilled = {fulfilled_status}:")
    print(f"  Total: {subset_total:,} ({(subset_total/total_requests)*100:.2f}%)")
    print(f"  Shared: {subset_shared:,} ({(subset_shared/subset_total)*100:.2f}% of segment)")

# Document types analysis
print("\n" + "="*80)
print("DOCUMENT TYPE ANALYSIS")
print("="*80)

doc_types_analysis = df.groupby('REQUIRED_DOC_NAMES').agg({
    'COUNT': 'sum',
    'STATUS': lambda x: pd.Series(x).value_counts().to_dict()
}).sort_values('COUNT', ascending=False).head(10)

print("\nTop 10 Document Combinations (by request volume):")
print("-" * 60)
for idx, (doc_name, row) in enumerate(doc_types_analysis.iterrows(), 1):
    total = row['COUNT']
    percentage = (total / total_requests) * 100
    print(f"\n{idx}. {doc_name}")
    print(f"   Total: {total:,} requests ({percentage:.2f}%)")

    status_dict = row['STATUS']
    for status, count_val in status_dict.items():
        status_pct = (count_val / total) * 100
        print(f"   - {status:20s}: {count_val:6,} ({status_pct:5.2f}%)")

# User behavior patterns
print("\n" + "="*80)
print("3. USER BEHAVIOR PATTERNS")
print("="*80)

# Consent analysis
consent_analysis = df.groupby('CONSENT_GIVEN')['COUNT'].sum()
print("\nConsent Given Distribution:")
print("-" * 60)
for consent_status, count in consent_analysis.items():
    percentage = (count / total_requests) * 100
    print(f"{str(consent_status):10s}: {count:,} ({percentage:.2f}%)")

# Among those who gave consent, what happened?
consent_given_df = df[df['CONSENT_GIVEN'] == 'Yes']
if len(consent_given_df) > 0:
    consent_outcomes = consent_given_df.groupby('STATUS')['COUNT'].sum()
    consent_total = consent_outcomes.sum()
    print(f"\nOutcomes after Consent Given (Total: {consent_total:,}):")
    print("-" * 60)
    for status, count in consent_outcomes.items():
        percentage = (count / consent_total) * 100
        print(f"{status:25s}: {count:,} ({percentage:.2f}%)")

# Consent decline rate
rejected_df = df[df['STATUS'] == 'User Rejected']
rejection_total = rejected_df['COUNT'].sum()
print(f"\n>>> CONSENT DECLINE RATE: {(rejection_total/total_requests)*100:.2f}% of all requests")

# PIN analysis
pin_analysis = df.groupby('PIN_GIVEN')['COUNT'].sum()
print("\n" + "-"*60)
print("PIN Entry Distribution:")
print("-" * 60)
for pin_status, count in pin_analysis.items():
    percentage = (count / total_requests) * 100
    print(f"{str(pin_status):10s}: {count:,} ({percentage:.2f}%)")

# Among those who gave PIN, what happened?
pin_given_df = df[df['PIN_GIVEN'] == 'Yes']
if len(pin_given_df) > 0:
    pin_outcomes = pin_given_df.groupby('STATUS')['COUNT'].sum()
    pin_total = pin_outcomes.sum()
    print(f"\nOutcomes after PIN Given (Total: {pin_total:,}):")
    print("-" * 60)
    for status, count in pin_outcomes.items():
        percentage = (count / pin_total) * 100
        print(f"{status:25s}: {count:,} ({percentage:.2f}%)")

# Notification state analysis
print("\n" + "-"*60)
print("Notification State Distribution:")
print("-" * 60)
notif_analysis = df.groupby('NOTIFICATION_STATE')['COUNT'].sum().sort_values(ascending=False)
for notif_state, count in notif_analysis.items():
    percentage = (count / total_requests) * 100
    print(f"{str(notif_state):20s}: {count:,} ({percentage:.2f}%)")

# Abandonment patterns
print("\n" + "="*60)
print("ABANDONMENT PATTERN ANALYSIS")
print("="*60)

abandoned_df = df[df['STATUS'] == 'No Action Taken']
abandoned_total = abandoned_df['COUNT'].sum()
print(f"\nTotal Abandoned: {abandoned_total:,} ({(abandoned_total/total_requests)*100:.2f}%)")

# Breakdown by notification state
if len(abandoned_df) > 0:
    abandoned_by_notif = abandoned_df.groupby('NOTIFICATION_STATE')['COUNT'].sum()
    print(f"\nAbandonment by Notification State:")
    print("-" * 60)
    for notif_state, count in abandoned_by_notif.items():
        percentage = (count / abandoned_total) * 100
        print(f"{str(notif_state):20s}: {count:,} ({percentage:.2f}%)")

    # Abandonment by document availability
    abandoned_by_docs = abandoned_df.groupby('DOC_AVAILIBILITY')['COUNT'].sum()
    print(f"\nAbandonment by Document Availability:")
    print("-" * 60)
    for doc_status, count in abandoned_by_docs.items():
        percentage = (count / abandoned_total) * 100
        print(f"{doc_status:30s}: {count:,} ({percentage:.2f}%)")

    # Abandonment by consent given
    abandoned_by_consent = abandoned_df.groupby('CONSENT_GIVEN')['COUNT'].sum()
    print(f"\nAbandonment by Consent Status:")
    print("-" * 60)
    for consent_status, count in abandoned_by_consent.items():
        percentage = (count / abandoned_total) * 100
        print(f"{str(consent_status):10s}: {count:,} ({percentage:.2f}%)")

# Service performance
print("\n" + "="*80)
print("4. SERVICE PERFORMANCE METRICS")
print("="*80)

# Credential request analysis
cred_request_analysis = df.groupby('CREDENTIAL_REQUEST')['COUNT'].sum().sort_values(ascending=False)
print("\nCredential Request Distribution:")
print("-" * 60)
for cred_status, count in cred_request_analysis.items():
    percentage = (count / total_requests) * 100
    print(f"{str(cred_status):10s}: {count:,} ({percentage:.2f}%)")

# Credential status breakdown
cred_status_analysis = df.groupby('CREDENTIAL_STATUS')['COUNT'].sum().sort_values(ascending=False)
print("\nCredential Status Distribution:")
print("-" * 60)
for cred_status, count in cred_status_analysis.items():
    percentage = (count / total_requests) * 100
    print(f"{str(cred_status):10s}: {count:,} ({percentage:.2f}%)")

# Success vs Failed credential requests
cred_req_yes_df = df[df['CREDENTIAL_REQUEST'] == 'Yes']
if len(cred_req_yes_df) > 0:
    cred_req_total = cred_req_yes_df['COUNT'].sum()
    cred_success = cred_req_yes_df[cred_req_yes_df['CREDENTIAL_STATUS'] == 'Success']['COUNT'].sum()
    cred_failed = cred_req_yes_df[cred_req_yes_df['CREDENTIAL_STATUS'] == 'Failed']['COUNT'].sum()

    print(f"\n>>> Document Request Success Rate:")
    print(f"    Total credential requests: {cred_req_total:,}")
    print(f"    Success: {cred_success:,} ({(cred_success/cred_req_total)*100:.2f}%)")
    print(f"    Failed: {cred_failed:,} ({(cred_failed/cred_req_total)*100:.2f}%)")

# Platform analysis
print("\n" + "="*80)
print("PLATFORM & TECHNICAL BREAKDOWN")
print("="*80)

platform_analysis = df.groupby('USER_AGENT')['COUNT'].sum().sort_values(ascending=False)
print("\nBy Platform:")
print("-" * 60)
for platform, count in platform_analysis.items():
    percentage = (count / total_requests) * 100
    print(f"{str(platform):10s}: {count:,} ({percentage:.2f}%)")

# Success rate by platform
print("\nSuccess Rate by Platform:")
print("-" * 60)
for platform in df['USER_AGENT'].unique():
    platform_df = df[df['USER_AGENT'] == platform]
    platform_total = platform_df['COUNT'].sum()
    platform_shared = platform_df[platform_df['STATUS'] == 'Shared']['COUNT'].sum()

    if platform_total > 0:
        conversion = (platform_shared / platform_total) * 100
        print(f"{str(platform):10s}: {platform_shared:,}/{platform_total:,} ({conversion:.2f}%)")

# VIZ_TYPE analysis
viz_analysis = df.groupby('VIZ_TYPE')['COUNT'].sum().sort_values(ascending=False)
print("\nBy Visualization Type (Pull/Push):")
print("-" * 60)
for viz_type, count in viz_analysis.items():
    percentage = (count / total_requests) * 100
    print(f"{viz_type:10s}: {count:,} ({percentage:.2f}%)")

# Success rate by VIZ_TYPE
print("\nSuccess Rate by VIZ_TYPE:")
print("-" * 60)
for viz_type in df['VIZ_TYPE'].unique():
    viz_df = df[df['VIZ_TYPE'] == viz_type]
    viz_total = viz_df['COUNT'].sum()
    viz_shared = viz_df[viz_df['STATUS'] == 'Shared']['COUNT'].sum()

    if viz_total > 0:
        conversion = (viz_shared / viz_total) * 100
        print(f"{viz_type:10s}: {viz_shared:,}/{viz_total:,} ({conversion:.2f}%)")

# Service Provider analysis
print("\n" + "-"*60)
print("Top 10 Service Providers by Volume:")
print("-" * 60)
sp_analysis = df.groupby('ALIAS_NAME')['COUNT'].sum().sort_values(ascending=False).head(10)
for sp_name, count in sp_analysis.items():
    percentage = (count / total_requests) * 100
    print(f"{sp_name:30s}: {count:,} ({percentage:.2f}%)")

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
