# Password Playground

This repository is a learning playground for experimenting with password safety concepts using Python.

It contains small scripts focused on understanding how password breach checking works, how privacy-preserving APIs are designed, and how to handle sensitive input responsibly during local execution. The goal is to learn security fundamentals and API usage patterns — not to build authentication systems or production password validators.

Some scripts are inspired by exercises from the **Zero To Mastery Python course**, but the implementations here reflect my own understanding, experimentation, and adaptation based on documentation and hands-on testing.

---

## Current Scripts

### Password Breach Lookup

A command-line script that checks whether a password has appeared in known data breaches using the **Have I Been Pwned** password API.

**What it demonstrates:**

* Hashing passwords locally using SHA-1
* Querying a public API using a privacy-preserving approach
* Using the API’s response to determine breach exposure
* Avoiding transmission of plaintext passwords
* Basic error handling for network and API failures

This script checks **only known breaches** and does not evaluate password strength or complexity.

---

## Privacy and Security Model

Passwords are **never sent over the network**.

Instead, this script uses the **k-anonymity** model provided by the Have I Been Pwned password API:

* The password is hashed locally
* Only the first five characters of the hash are sent to the API
* The API responds with a list of matching hash suffixes and breach counts
* The full hash comparison is performed locally

At no point is the original password or full hash transmitted.

This approach reduces exposure while still allowing effective breach checking.

---

## Input Handling

Passing passwords directly as command-line arguments can expose them through shell history or process listings. For this reason, safer input methods (such as reading from a local file) are preferred for demonstration purposes.

Any input files containing passwords should be treated as sensitive:

* They should not be committed to version control
* They should be deleted after use
* They should be added to `.gitignore`

---

## External Dependency

This script relies on the public password breach data provided by:

[https://haveibeenpwned.com](https://haveibeenpwned.com)

Results are limited to what is available in that dataset and depend on API availability.

---

## API Response Status Codes

The Have I Been Pwned password API responds with standard HTTP status codes.
This script uses these codes to determine whether a request was successful
and to report errors clearly.

Common status codes you may encounter:

* **200** — The request was successful and breach data was returned
* **400** — The request was malformed or invalid
* **403** — Access was denied (request not permitted)
* **429** — Too many requests were made in a short period of time
* **500** — A server-side error occurred

Non-success responses indicate that the request could not be completed as
expected. The script reports these cases but does not attempt automatic
recovery.

---

## Purpose of This Repository

* Learn how breach-checking APIs work
* Understand privacy-preserving design patterns
* Practice secure handling of sensitive input
* Explore real-world security concepts through small, focused scripts
* Build familiarity with hashing and API-based workflows

This repository is intended to grow as additional password- and security-related experiments are added.

---

## Requirements

* Python 3
* requests

---

## Notes

* This is a learning-focused repository
* Scripts prioritize clarity and security awareness over feature completeness
* No passwords or sensitive data should ever be committed
* Code is written to demonstrate concepts, not to serve as a production security tool
